import torch
import torch.nn as nn


class MLPPolicyValueNetwork(nn.Module):
    """
    Simple shared-backbone MLP for policy and value estimation.

    Design rationale:
    - Small network capacity to emphasize problem formulation
      over architectural complexity.
    - Shared representation to mirror standard PPO setups.
    - Intentionally avoids attention or deep stacks to keep
      learning behavior interpretable.

    This reflects empirical findings from the full project:
    increasing model complexity alone does not resolve
    instability under delayed rewards.
    """

    def __init__(self, input_dim: int, hidden_dims=(64, 64)):
        super().__init__()

        layers = []
        last_dim = input_dim

        for h in hidden_dims:
            layers.append(nn.Linear(last_dim, h))
            layers.append(nn.ReLU())
            last_dim = h

        self.backbone = nn.Sequential(*layers)

        self.policy_head = nn.Linear(last_dim, 1)
        self.value_head = nn.Linear(last_dim, 1)

    def forward(self, x: torch.Tensor):
        """
        Forward pass.

        Returns:
            policy_score: unnormalized scalar score
            value: state value estimate
        """
        features = self.backbone(x)
        policy_score = self.policy_head(features)
        value = self.value_head(features)
        return policy_score, value
