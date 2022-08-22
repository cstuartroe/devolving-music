import time


class TaskTimer:
    timers_by_name: dict[str, "TaskTimer"] = {}

    @classmethod
    def get(cls, name: str) -> "TaskTimer":
        cls.timers_by_name[name] = cls.timers_by_name.get(name, cls())
        return cls.timers_by_name[name]

    def __init__(self):
        self.task_stack = []
        self.start_time = None
        self.task_timings = {}

        self.start_subtask('startup')

    def log_task(self):
        if self.task_stack:
            current_task = '/'.join(self.task_stack)

            self.task_timings[current_task] = (
                self.task_timings.get(current_task, 0) + time.time() - self.start_time
            )
            self.start_time = None

    def _start_task(self, task: str):
        self.task_stack.append(task)
        self.start_time = time.time()

    def start_subtask(self, task: str):
        self.log_task()
        self._start_task(task)

    def switch_task(self, task: str):
        self.end_task()
        self._start_task(task)

    def end_task(self):
        self.log_task()

        self.task_stack.pop()
        self.start_time = time.time()

    def close(self):
        while self.task_stack:
            self.end_task()

    def __str__(self):
        tasks = sorted(list(self.task_timings.items()), key=lambda p: p[1], reverse=True)

        out = "TaskTimer:\n"
        for task_name, time_taken in tasks:
            out += f"  {task_name}: {time_taken}\n"

        return out
