"""
URL configuration for hw_django_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from task_manager import views as task_views
from hw_django_project import settings
from django.conf.urls.static import static
urlpatterns = [
    path("admin/", admin.site.urls),
    path('', include('first_app.urls')),

    #api for task
    # Задание 1
    path('tasks/create/', task_views.task_create, name='task-create'),

    # Задание 2
    path('tasks/', task_views.task_list, name='task-list'),
    path('tasks/<int:pk>/', task_views.task_detail, name='task-detail'),

    # Задание 3
    path('tasks/stats/', task_views.task_stats, name='task-stats'),
    # просто дополнительно сделал
    path('tasks/<int:pk>/update/', task_views.task_update, name='task-update'),
    path('tasks/<int:pk>/delete/', task_views.task_delete, name='task-delete'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
