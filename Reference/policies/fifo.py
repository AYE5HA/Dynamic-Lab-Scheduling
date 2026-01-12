class FIFOPolicy:
    """
    First-In-First-Out (FIFO) scheduling policy.

    Rationale:
    - Common default in laboratory operations
    - Simple and interpretable
    - Performs reasonably well under low load
    - Known to fail under congestion and priority pressure
    """

    def select_action(self, env):
        """
        Assign the oldest job in the queue to the first idle machine.
        If no machine is idle or the queue is empty, do nothing.
        """
        if len(env.queue) == 0:
            return env.action_space.n - 1  # no-op

        for i, machine in enumerate(env.machines):
            if machine.is_idle():
                return i

        return env.action_space.n - 1  # no-op
