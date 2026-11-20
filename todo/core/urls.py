from django.urls import path
from . import views

urlpatterns =[
    path('',views.index_view, name='index'),
    path('task/<int:task_id>/complete', views.is_completed_view, name='is_completed'),
    path('task/add_task', views.add_task_view, name='add_task'),
    path('task/<int:task_id>/update', views.update_view, name='update'),
    path('task/<int:task_id>/delete', views.delete_view, name='delete'),
]