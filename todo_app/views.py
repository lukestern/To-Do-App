from datetime import datetime
from typing import List
from todo_app.task import Task

class ViewModel:
    def __init__(self, tasks: List[Task]):
        self._tasks = tasks

    @property
    def tasks(self):
        return self._tasks

    @property
    def not_started_tasks(self) -> List[Task]:
        return [task for task in self._tasks if 'Not Started' in task.status]

    @property
    def in_progress_tasks(self) -> List[Task]:
        return [task for task in self._tasks if 'In Progress' in task.status]

    @property
    def more_than_5_complete_tasks(self) -> List[Task]:
        tasks =  [task for task in self._tasks if 'Complete' in task.status]
        return len(tasks) > 5

    @property
    def complete_tasks(self) -> List[Task]:
        tasks =  [task for task in self._tasks if 'Complete' in task.status]
        if self.more_than_5_complete_tasks:
            return self.tasks_completed_today()
        else:
            return tasks

    @property
    def older_tasks(self) -> List[Task]:
        result = []
        for task in self._tasks:
            if task.last_updated.date() < datetime.today().date() and 'Complete' in task.status:
                result.append(task)
        return result 

    def tasks_completed_today(self) -> List[Task]:
        result = []
        for task in self._tasks:
            if task.last_updated.date() == datetime.today().date() and 'Complete' in task.status:
                result.append(task)
        return result 
