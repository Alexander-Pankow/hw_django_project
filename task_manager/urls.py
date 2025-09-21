
from django.urls import path
from task_manager.views import (task_create,task_list,task_detail,task_stats,task_update,task_delete,SubTaskListCreateView, SubTaskDetailUpdateDeleteView,
                                TaskListView,SubTaskListView,SubTaskFilterListView)

app_name = "task_manager"

urlpatterns = [
    # api for task
    # Задание 1 api for task
    path('tasks/create/', task_create, name='task-create'),

    # Задание 2
    #path('tasks/', task_list, name='task-list'),
    #path('tasks/<int:pk>/', task_detail, name='task-detail'),

    # Задание 3
    path('tasks/stats/', task_stats, name='task-stats'),

    #path("subtasks/", SubTaskListCreateView.as_view(), name="subtask-list-create"),
    #path("subtasks/<int:pk>/", SubTaskDetailUpdateDeleteView.as_view(), name="subtask-detail-update-delete"),

    # просто дополнительно сделал
    path('tasks/<int:pk>/update/', task_update, name='task-update'),
    path('tasks/<int:pk>/delete/', task_delete, name='task-delete'),

    # HW14 Задание 1 http://127.0.0.1:8000/api/v1/tasks/?deadline=4 запуск
    path('tasks/', TaskListView.as_view(), name='TaskListView'),

    #HW14 Задание 2 GET http://127.0.0.1:8000/api/v1/subtasks/ → вернёт первые 5 подзадач
    #               GET http://127.0.0.1:8000/api/v1/subtasks/?page=2 → вернёт следующие 5
    #               GET http://127.0.0.1:8000/api/v1/subtasks/?page_size=10 → изменит количество объектов на странице
    #path('subtasks/', SubTaskListView.as_view(), name='SubTaskListView'),

    # HW14 Задание 3 GET http://127.0.0.1:8000/api/v1/subtasks/ → вернёт первые 5 подзадач
    #               GET http://127.0.0.1:8000/api/v1/subtasks/?task_title=Домашнее задание, Подзадачи только для задачи "Домашнее задание":
    #               GET http://127.0.0.1:8000/api/v1/subtasks/?status=In progress, Подзадачи только со статусом "In progress":
    #               GET http://127.0.0.1:8000/api/v1/subtasks/?task_title=Проект&status=Done, Подзадачи для задачи "Проект" со статусом "Done":
    path('subtasks/', SubTaskFilterListView.as_view(), name='subtask-list'),
]
