import torch
import torch.nn as nn


class MLPPolicyNetwork(nn.Module):
    """
    Simple MLP used for both policy and value estimation.

    Design choice:
    - Small network to emphasize problem formulation
      over model capacity.
    - Keeps learning dynamics interpretable.
    """

    def __init__(self, input_dim: int, hidden_dims=(64, 64)):
        super().__init__()

        layers = []
        last_dim = input_dim

        for h in hidden_dims:
            layers.append(nn.Linear(last_dim, h))
            layers.append(nn.ReLU())
            last_dim = h

        self.shared = nn.Sequential(*layers)

        self.policy_head = nn.Linear(last_dim, 1)   # scalar action score
        self.value_head = nn.Linear(last_dim, 1)

    def forward(self, x):
        features = self.shared(x)
        policy_score = self.policy_head(features)
        value = self.value_head(features)
        return policy_score, value
