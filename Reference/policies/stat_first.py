class StatFirstPolicy:
    """
    Priority-based heuristic.
    Always schedules STAT jobs first if available.
    """

    def select_action(self, env):
        if len(env.queue) == 0:
            return env.action_space.n - 1

        # Check for STAT jobs
        stat_jobs = [j for j in env.queue if j.is_stat]
        if stat_jobs:
            job = stat_jobs[0]
            env.queue.remove(job)
            env.queue.insert(0, job)

        for i, machine in enumerate(env.machines):
            if machine.is_idle():
                return i

        return env.action_space.n - 1
