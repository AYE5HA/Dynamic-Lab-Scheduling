import torch


class RolloutBuffer:
    """
    Stores a single episode rollout.

    This buffer is intentionally episode-scoped (not batched)
    to make delayed rewards, variance, and instability explicit.

    This mirrors the way learning dynamics were observed and
    debugged in the original project.
    """

    def __init__(self):
        self.observations = []
        self.actions = []
        self.rewards = []
        self.log_probs = []
        self.values = []

    def add(self, obs, action, reward, log_prob, value):
        self.observations.append(obs)
        self.actions.append(action)
        self.rewards.append(reward)
        self.log_probs.append(log_prob)
        self.values.append(value)

    def as_tensors(self):
        return (
            torch.tensor(self.observations, dtype=torch.float32),
            torch.tensor(self.actions, dtype=torch.int64),
            torch.stack(self.log_probs),
            torch.tensor(self.rewards, dtype=torch.float32),
            torch.stack(self.values).squeeze(),
        )

    def clear(self):
        self.__init__()
