class StatFirstPolicy:
    """
    STAT-first priority heuristic.

    Rationale:
    - Widely used operational rule in healthcare labs
    - Prioritizes urgent samples aggressively
    - Locally optimal but globally myopic
    - Can induce severe congestion for routine jobs
    """

    def select_action(self, env):
        """
        If a STAT job exists in the queue, move the earliest STAT
        job to the front. Otherwise, preserve FIFO order.
        """
        if len(env.queue) == 0:
            return env.action_space.n - 1  # no-op

        # Find earliest STAT job (by arrival time)
        stat_index = None
        for idx, job in enumerate(env.queue):
            if job.is_stat:
                stat_index = idx
                break

        # Promote STAT job to front if found
        if stat_index is not None:
            stat_job = env.queue.pop(stat_index)
            env.queue.insert(0, stat_job)

        for i, machine in enumerate(env.machines):
            if machine.is_idle():
                return i

        return env.action_space.n - 1  # no-op
