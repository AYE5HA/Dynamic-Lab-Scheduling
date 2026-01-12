import numpy as np
import gymnasium as gym
from gymnasium import spaces

class Job:
    def __init__(self, arrival, service, deadline, is_stat):
        self.arrival = arrival
        self.service = service
        self.deadline = deadline
        self.is_stat = is_stat
        self.remaining = service

class LabSchedulerEnv(gym.Env):
    def __init__(self, config):
        self.cfg = config
        self.num_machines = config["num_machines"]
        self.time = 0
        self.jobs = []
        self.machines = [None] * self.num_machines

        # state: [queue_len, stat_frac, free_machines]
        self.observation_space = spaces.Box(
            low=0, high=1000, shape=(3,), dtype=np.float32
        )

        self.action_space = spaces.Discrete(self.num_machines + 1)
        self.reset()

    def reset(self, seed=None, options=None):
        self.time = 0
        self.jobs = []
        self.machines = [None] * self.num_machines
        self.np_random = np.random.default_rng(seed)
        return self._get_obs(), {}

    def _get_obs(self):
        if len(self.jobs) == 0:
            stat_frac = 0.0
        else:
            stat_frac = np.mean([j.is_stat for j in self.jobs])

        free = sum(m is None for m in self.machines)
        return np.array([len(self.jobs), stat_frac, free], dtype=np.float32)

    def _arrival(self):
        if self.np_random.random() < self.cfg["arrival_rate"]:
            is_stat = self.np_random.random() < self.cfg["stat_fraction"]
            deadline = (
                self.cfg["stat_deadline"] if is_stat
                else self.cfg["routine_deadline"]
            )
            service = max(1, int(self.np_random.exponential(
                self.cfg["service_time_mean"]
            )))
            self.jobs.append(
                Job(self.time, service, self.time + deadline, is_stat)
            )

    def step(self, action):
        reward = 0.0

        # assign job if possible
        if action < self.num_machines:
            if self.machines[action] is None and self.jobs:
                job = self.jobs.pop(0)
                self.machines[action] = job

        # advance time
        self.time += 1
        self._arrival()

        for i in range(self.num_machines):
            job = self.machines[i]
            if job is not None:
                job.remaining -= 1
                if job.remaining <= 0:
                    tardiness = max(0, self.time - job.deadline)
                    penalty = tardiness * (5 if job.is_stat else 1)
                    reward -= penalty
                    self.machines[i] = None

        done = self.time >= self.cfg["episode_length"]
        return self._get_obs(), reward, done, False, {}
