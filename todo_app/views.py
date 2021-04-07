

class ViewModel:
    def __init__(self, tasks) -> None:
        self._tasks = tasks

    @property
    def tasks(self):
        return self._tasks

    @property
    def not_started_tasks(self):
        return [task for task in self._tasks if 'Not Started' in task.status]

    @property
    def in_progress_tasks(self):
        return [task for task in self._tasks if 'In Progress' in task.status]

    @property
    def complete_tasks(self):
        return [task for task in self._tasks if 'Complete' in task.status]
