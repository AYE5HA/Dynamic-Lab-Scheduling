class Machine:
    """
    Represents a single laboratory machine/server.
    """
    def __init__(self, machine_id: int):
        self.machine_id = machine_id
        self.current_job = None

    def is_idle(self) -> bool:
        return self.current_job is None

    def assign(self, job, current_time: int):
        job.start_time = current_time
        self.current_job = job

    def step(self, current_time: int):
        """
        Advance processing by one time unit.
        """
        if self.current_job is None:
            return None

        self.current_job.remaining_time -= 1

        if self.current_job.remaining_time <= 0:
            finished_job = self.current_job
            finished_job.completion_time = current_time
            self.current_job = None
            return finished_job

        return None
