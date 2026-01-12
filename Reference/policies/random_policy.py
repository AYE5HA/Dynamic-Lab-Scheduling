import random

class RandomPolicy:
    """
    Random assignment policy.

    Purpose:
    - Acts as a statistical control
    - Verifies that learning-based policies capture
      meaningful structure beyond noise
    """

    def __init__(self, seed: int = 0):
        self.random = random.Random(seed)

    def select_action(self, env):
        """
        Randomly select an action from the valid action space.
        """
        return self.random.randrange(env.action_space.n)
