from django.urls import path
from . import views
urlpatterns = [
    path('', views.hallo_name, name='first_app'),
]
