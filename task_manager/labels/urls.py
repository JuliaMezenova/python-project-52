from django.urls import path
from.views import IndexView, LabelFormCreateView, LabelFormUpdateView, LabelFormDeleteView


urlpatterns = [
    path('', IndexView.as_view(), name='labels_index'),
    path('create/', LabelFormCreateView.as_view(), name='label_create'),
    path('<int:pk>/update/', LabelFormUpdateView.as_view(), name='label_update'),
    path('<int:pk>/delete/', LabelFormDeleteView.as_view(), name='label_delete'),
]
