
from django.urls import path
from task_manager.views import task_create,task_list,task_detail,task_stats,task_update,task_delete,SubTaskListCreateView, SubTaskDetailUpdateDeleteView

app_name = "task_manager"

urlpatterns = [
    # api for task
    # Задание 1 api for task
    path('tasks/create/', task_create, name='task-create'),

    # Задание 2
    path('tasks/', task_list, name='task-list'),
    path('tasks/<int:pk>/', task_detail, name='task-detail'),

    # Задание 3
    path('tasks/stats/', task_stats, name='task-stats'),
    # просто дополнительно сделал
    path('tasks/<int:pk>/update/', task_update, name='task-update'),
    path('tasks/<int:pk>/delete/', task_delete, name='task-delete'),

    path("subtasks/", SubTaskListCreateView.as_view(), name="subtask-list-create"),
    path("subtasks/<int:pk>/", SubTaskDetailUpdateDeleteView.as_view(), name="subtask-detail-update-delete"),
]