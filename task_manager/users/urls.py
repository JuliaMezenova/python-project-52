from django.urls import path
from .views import IndexView, UserFormCreateView, UserFormUpdateView, UserFormDeleteView

urlpatterns = [
    path('', IndexView.as_view(), name='users_index'),
    path('create/', UserFormCreateView.as_view(), name='user_create'),
    path('<int:pk>/update/', UserFormUpdateView.as_view(), name='user_update'),
    path('<int:pk>/delete/', UserFormDeleteView.as_view(), name='user_delete'),
]
