from django.urls import path
from . import views

urlpatterns = [
    path("dashboard/", views.dashboard, name="dashboard"),
    path("create/", views.create_task, name="create_task"),
    path("machine/<int:machine_id>/", views.machine_tasks, name="machine_tasks"),
    path("task/<int:task_id>/<str:new_status>/", views.update_task_status, name="update_task_status"),
    path("set_language/", views.set_language, name="set_language"),
]