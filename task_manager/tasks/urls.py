from django.urls import path
from .views import (
    IndexView,
    TaskFormCreateView,
    TaskFormUpdateView,
    TaskFormDeleteView,
    TaskShowIndex
)


urlpatterns = [
    path('', IndexView.as_view(), name='tasks_index'),
    path('create/', TaskFormCreateView.as_view(), name='task_create'),
    path('<int:pk>/update/', TaskFormUpdateView.as_view(), name='task_update'),
    path('<int:pk>/delete/', TaskFormDeleteView.as_view(), name='task_delete'),
    path('<int:pk>/', TaskShowIndex.as_view(), name='task_show_index'),
]
