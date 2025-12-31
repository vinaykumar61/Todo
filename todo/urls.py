# App-level URLs for the todo app, including both template pages and API endpoints.

from django.urls import path
from . import views

urlpatterns = [
    path('', views.task_list_page, name='task_list_page'),
    path('add/', views.add_task_page, name='add_task_page'),

    path('api_create_task/', views.api_create_task),
    path('api_get_tasks/', views.api_get_tasks),
    path('api_get_task/<int:task_id>/', views.api_get_task_by_id),
    path('api_update_task/<int:task_id>/', views.api_update_task),
    path('api_delete_task/<int:task_id>/', views.api_delete_task),
]
