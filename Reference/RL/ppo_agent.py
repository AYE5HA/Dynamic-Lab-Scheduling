"""
Reference PPO implementation for priority-aware lab scheduling.

IMPORTANT NOTE ON SCOPE AND DESIGN:

This PPO agent is intentionally minimal and explicit.

It reflects empirical observations from the full project:
- Rewards are delayed (tardiness only observed on completion)
- Learning is slow and unstable under low pressure
- PPO only differentiates from heuristics under sustained congestion
- Problem formulation matters more than model complexity

Accordingly, this implementation:
- Uses episode-based rollouts (no large batch magic)
- Avoids GAE, entropy bonuses, and aggressive tuning
- Prioritizes transparency over performance

This is a reference implementation, not a production trainer.
"""

import torch
import torch.nn.functional as F
from torch.distributions import Categorical

from .networks import MLPPolicyValueNetwork
from .rollout_buffer import RolloutBuffer


class PPOAgent:
    def __init__(
        self,
        obs_dim: int,
        action_dim: int,
        learning_rate: float = 3e-4,
        gamma: float = 0.99,
        clip_eps: float = 0.2,
        seed: int = 0,
    ):
        torch.manual_seed(seed)

        self.gamma = gamma
        self.clip_eps = clip_eps
        self.action_dim = action_dim

        self.network = MLPPolicyValueNetwork(obs_dim)
        self.optimizer = torch.optim.Adam(
            self.network.parameters(), lr=learning_rate
        )

    # --------------------------------------------------
    # Action selection
    # --------------------------------------------------

    def select_action(self, observation):
        """
        Select an action given the current observation.

        Returns:
            action (int)
            log_prob (Tensor)
            value (Tensor)
        """
        obs_tensor = torch.tensor(
            observation, dtype=torch.float32
        ).unsqueeze(0)

        policy_score, value = self.network(obs_tensor)

        # Convert scalar score into categorical distribution
        logits = policy_score.repeat(1, self.action_dim)
        probs = torch.softmax(logits, dim=1)

        dist = Categorical(probs)
        action = dist.sample()

        return (
            action.item(),
            dist.log_prob(action),
            value.squeeze(),
        )

    # --------------------------------------------------
    # Return computation
    # --------------------------------------------------

    def compute_returns(self, rewards):
        """
        Compute discounted returns for one episode.

        Delayed penalties mean returns are sparse and high-variance,
        which is a key contributor to learning instability.
        """
        returns = []
        G = 0.0

        for r in reversed(rewards):
            G = r + self.gamma * G
            returns.insert(0, G)

        return torch.tensor(returns, dtype=torch.float32)

    # --------------------------------------------------
    # PPO update (episode-based)
    # --------------------------------------------------

    def update_from_episode(self, buffer: RolloutBuffer):
        """
        Perform a single PPO update using one episode rollout.

        This makes learning dynamics and variance explicit.
        """
        (
            observations,
            actions,
            old_log_probs,
            rewards,
            values,
        ) = buffer.as_tensors()

        returns = self.compute_returns(rewards)
        advantages = returns - values.detach()

        policy_scores, new_values = self.network(observations)
        logits = policy_scores.repeat(1, self.action_dim)
        probs = torch.softmax(logits, dim=1)

        dist = Categorical(probs)
        new_log_probs = dist.log_prob(actions)

        ratio = torch.exp(new_log_probs - old_log_probs)

        clipped_ratio = torch.clamp(
            ratio, 1 - self.clip_eps, 1 + self.clip_eps
        )

        policy_loss = -torch.min(
            ratio * advantages, clipped_ratio * advantages
        ).mean()

        value_loss = F.mse_loss(new_values.squeeze(), returns)

        loss = policy_loss + 0.5 * value_loss

        self.optimizer.zero_grad()
        loss.backward()
        self.optimizer.step()
