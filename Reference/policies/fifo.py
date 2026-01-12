class FIFOPolicy:
    """
    First-In-First-Out scheduling.
    Assigns the oldest job in the queue to the first available machine.
    """

    def select_action(self, env):
        for i, machine in enumerate(env.machines):
            if machine.is_idle() and len(env.queue) > 0:
                return i
        return env.action_space.n - 1  # no-op
