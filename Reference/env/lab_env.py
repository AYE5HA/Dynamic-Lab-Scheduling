import gymnasium as gym
from gymnasium import spaces
import numpy as np

from .job import Job
from .machine import Machine


class LabSchedulingEnv(gym.Env):
    """
    Discrete-event laboratory scheduling environment with
    priority-aware job handling and limited capacity.

    Time advances in unit steps. At each step:
    - New jobs may arrive
    - The agent may assign a job to an idle machine
    - Machines process jobs
    - Completed jobs generate reward penalties
    """

    metadata = {"render_modes": []}

    def __init__(self, config: dict):
        super().__init__()

        self.cfg = config
        self.current_time = 0
        self.job_counter = 0

        # Machines
        self.machines = [
            Machine(i) for i in range(self.cfg["num_machines"])
        ]

        # Job queue
        self.queue = []

        # Observation:
        # [queue_length, fraction_STAT_in_queue, free_machine_count]
        self.observation_space = spaces.Box(
            low=0.0,
            high=np.inf,
            shape=(3,),
            dtype=np.float32
        )

        # Action:
        # 0..(num_machines-1) → assign next job to that machine
        # num_machines        → do nothing
        self.action_space = spaces.Discrete(
            self.cfg["num_machines"] + 1
        )

        self.np_random = None
        self.max_time = self.cfg["episode_length"]

    # --------------------------------------------------
    # Environment core
    # --------------------------------------------------

    def reset(self, seed=None, options=None):
        super().reset(seed=seed)

        self.current_time = 0
        self.job_counter = 0
        self.queue = []

        self.machines = [
            Machine(i) for i in range(self.cfg["num_machines"])
        ]

        self.np_random = np.random.default_rng(seed)
        return self._get_obs(), {}

    # --------------------------------------------------
    # Arrival process
    # --------------------------------------------------

    def _generate_arrivals(self):
        """
        Generate new jobs according to a Poisson process.
        """
        if self.np_random.random() < self.cfg["arrival_rate"]:
            is_stat = self.np_random.random() < self.cfg["stat_fraction"]

            if is_stat:
                deadline_offset = self.cfg["stat_deadline"]
                priority_weight = self.cfg["stat_priority_weight"]
            else:
                deadline_offset = self.cfg["routine_deadline"]
                priority_weight = self.cfg["routine_priority_weight"]

            service_time = max(
                1,
                int(
                    self.np_random.exponential(
                        self.cfg["service_time_mean"]
                    )
                )
            )

            job = Job(
                job_id=self.job_counter,
                arrival_time=self.current_time,
                service_time=service_time,
                deadline=self.current_time + deadline_offset,
                is_stat=is_stat
            )

            job.priority_weight = priority_weight
            self.queue.append(job)
            self.job_counter += 1

    # --------------------------------------------------
    # Observation
    # --------------------------------------------------

    def _get_obs(self):
        if len(self.queue) == 0:
            stat_fraction = 0.0
        else:
            stat_fraction = np.mean([j.is_stat for j in self.queue])

        free_machines = sum(m.is_idle() for m in self.machines)

        return np.array(
            [
                len(self.queue),
                stat_fraction,
                free_machines
            ],
            dtype=np.float32
        )

    # --------------------------------------------------
    # Step logic
    # --------------------------------------------------

    def step(self, action):
        reward = 0.0

        # 1. Agent assignment decision
        if action < len(self.machines):
            machine = self.machines[action]
            if machine.is_idle() and len(self.queue) > 0:
                job = self.queue.pop(0)
                machine.assign(job, self.current_time)

        # 2. Advance time
        self.current_time += 1

        # 3. New arrivals
        self._generate_arrivals()

        # 4. Machine processing
        for machine in self.machines:
            finished_job = machine.step(self.current_time)
            if finished_job is not None:
                tardiness = finished_job.tardiness
                penalty = tardiness * finished_job.priority_weight
                reward -= penalty

        # 5. Termination
        terminated = self.current_time >= self.max_time
        truncated = False

        return self._get_obs(), reward, terminated, truncated, {}
