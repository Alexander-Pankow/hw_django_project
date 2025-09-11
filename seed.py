"""
Освоение основных операций CRUD (Create, Read, Update, Delete) на примере заданных моделей.
Выполните запросы:

1. Создание записей:
Task:
    title: "Prepare presentation".
description: "Prepare materials and slides for the presentation".
status: "New".
deadline: Today's date + 3 days.

SubTasks для "Prepare presentation":
    title: "Gather information".
description: "Find necessary information for the presentation".
status: "New".
deadline: Today's date + 2 days.
    title: "Create slides".
description: "Create presentation slides".
status: "New".
deadline: Today's date + 1 day.
"""
import django
import os
from django.utils import timezone
from datetime import timedelta
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_project.settings')
django.setup()
from task_manager.models import Task,SubTask
from django.db.models import Q


def create_task_and_subtasks():
    # создаём задачу
    task = Task.objects.create(
        title="Prepare presentation",
        description="Prepare materials and slides for the presentation",
        status="New",
        deadline=timezone.now() + timedelta(days=3)
    )

    # создаём подзадачи пачкой
    subtasks = [
        SubTask(
            task=task,
            title="Gather information",
            description="Find necessary information for the presentation",
            status="New",
            deadline=timezone.now() + timedelta(days=2)
        ),
        SubTask(
            task=task,
            title="Create slides",
            description="Create presentation slides",
            status="New",
            deadline=timezone.now() + timedelta(days=1)
        )
    ]
    SubTask.objects.bulk_create(subtasks)

    return task, subtasks
# from seed import create_task_and_subtasks
# create_task_and_subtasks()
# (<Task: Prepare presentation>, [<SubTask: Gather information (Prepare presentation)>, <SubTask: Create slides (Prepare presentation)>])
# from task_manager.models import Task, SubTask
# Task.objects.all()
# SubTask.objects.all()

"""
2. Чтение записей:
Tasks со статусом "New":
Вывести все задачи, у которых статус "New".
SubTasks с просроченным статусом "Done":
Вывести все подзадачи, у которых статус "Done", но срок выполнения истек.
"""

def read_tasks_and_subtasks():
    new_tasks = Task.objects.filter(status="New")
    expired_done_subtasks = SubTask.objects.filter(
        Q(status="Done") & Q(deadline__lt=timezone.now())
    )
    return new_tasks, expired_done_subtasks

# from seed import read_tasks_and_subtasks
# read_tasks_and_subtasks()
# (<QuerySet [<Task: Prepare presentation>, <Task: Grocery Shopping>]>, <QuerySet [<SubTask: Warm up (Morning Run)>, <SubTask: Implement models (Finish Django HW)>]>)

"""
3. Изменение записей:
Измените статус "Prepare presentation" на "In progress".
Измените срок выполнения для "Gather information" на два дня назад.
Измените описание для "Create slides" на "Create and format presentation slides".
"""

def update_tasks_and_subtasks():
    Task.objects.filter(title="Prepare presentation").update(status="In progress")

    subtask1 = SubTask.objects.get(title="Gather information")
    subtask1.deadline = timezone.now() - timedelta(days=2)
    subtask1.save()

    SubTask.objects.filter(title="Create slides").update(
        description="Create and format presentation slides"
    )

    updated_task = Task.objects.get(title="Prepare presentation")
    updated_subtasks = SubTask.objects.all()
    return updated_task, updated_subtasks

# from seed import update_tasks_and_subtasks
# update_tasks_and_subtasks()
# (<Task: Prepare presentation>, <QuerySet [<SubTask: Gather information (Prepare presentation)>, <SubTask: Create slides (Prepare presentation)>, <SubTask: Read chapters 1–3 (Read Book)>, <SubTask: Warm up (Morning Run)>, <SubTask: Buy vegetables (Grocery Shopping)>, <SubTask: Implement models (Finish Django HW)>]>)
#

"""
4. Удаление записей:
Удалите задачу "Prepare presentation" и все ее подзадачи.
"""

def delete_task_and_subtasks_cascade():
    task = Task.objects.get(title="Prepare presentation")
    task.delete()
    return True

# from seed import delete_task_and_subtasks_cascade
# delete_task_and_subtasks_cascade()
# True
# from task_manager.models import Task, SubTask
# Task.objects.all()
# <QuerySet [<Task: Read Book>, <Task: Morning Run>, <Task: Grocery Shopping>, <Task: Finish Django HW>]>
# SubTask.objects.all()
# <QuerySet [<SubTask: Read chapters 1–3 (Read Book)>, <SubTask: Warm up (Morning Run)>, <SubTask: Buy vegetables (Grocery Shopping)>, <SubTask: Implement models (Finish Django HW)>]>
