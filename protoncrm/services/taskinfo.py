from dataclasses import dataclass
from crmproton.models import *
from django.db.models.fields.files import ImageFieldFile


@dataclass
class TaskInfo:
    task: Tasks
    task_level: TasksLevels | None = None
    task_time: TasksTime | None = None
    task_state: TasksStates | None = None
    task_workers: TasksUsers | None = None
    task_state_photo: ImageFieldFile | None = None


class TaskInfoStart:
    def __init__(self, task: Tasks):
        self.task = task
        task_level = TasksLevels.objects.filter(task=task)
        self.task_level = None if not task_level else \
            list(task_level)[-1].level
        task_time = TasksTime.objects.filter(task=task)
        self.task_time = None if not task_time else\
            list(task_time)[-1]
        task_state = TasksStates.objects.filter(task=task)
        self.task_state = None if not task_state else list(task_state)[-1]\
            .state
        self.task_state_photo = None if not task_state else\
            list(task_state)[-1].photo
        task_workers = TasksUsers.objects.filter(task=task, is_active=True)
        self.task_workers = [worker.user for worker in task_workers]

    def generate_obj(self):
        return TaskInfo(task=self.task,
                        task_time=self.task_time,
                        task_level=self.task_level,
                        task_state=self.task_state,
                        task_workers=self.task_workers,
                        task_state_photo=self.task_state_photo,
                        )
