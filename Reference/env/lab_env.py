import gymnasium as gym
from gymnasium import spaces
import numpy as np

from .job import Job
from .machine import Machine

class LabSchedulingEnv(gym.Env):
    """
    Discrete-event laboratory scheduling environment with
    priority-aware job handling and limited capacity.
    """

    metadata = {"render_modes": []}

    def __init__(self, config: dict):
        super().__init__()

        self.config = config
        self.current_time = 0
        self.job_counter = 0

        # Machines
        self.machines = [
            Machine(i) for i in range(config["num_machines"])
        ]

        # Job queue
        self.queue = []

        # Observation: defined explicitly later
        self.observation_space = spaces.Box(
            low=0,
            high=np.inf,
            shape=(3,),
            dtype=np.float32
        )

        # Action: assign to a machine or do nothing
        self.action_space = spaces.Discrete(
            config["num_machines"] + 1
        )

        self.np_random = None

    def reset(self, seed=None, options=None):
        self.current_time = 0
        self.job_counter = 0
        self.queue = []
        self.machines = [
            Machine(i) for i in range(len(self.machines))
        ]
        self.np_random = np.random.default_rng(seed)
        return self._get_obs(), {}

    def _get_obs(self):
        """
        Observation defined in next step.
        """
        raise NotImplementedError

    def step(self, action):
        """
        Core simulation step — implemented in next step.
        """
        raise NotImplementedError
