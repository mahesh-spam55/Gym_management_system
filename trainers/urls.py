from django.urls import path
from .views import (
    TrainerListView,
    TrainerDetailView,
    TrainerCreateView,
    TrainerUpdateView,
    TrainerDeleteView,
)

app_name = "trainers"

urlpatterns = [
    path("", TrainerListView.as_view(), name="list"),
    path("create/", TrainerCreateView.as_view(), name="create"),
    path("<int:pk>/", TrainerDetailView.as_view(), name="detail"),
    path("<int:pk>/edit/", TrainerUpdateView.as_view(), name="edit"),
    path("<int:pk>/delete/", TrainerDeleteView.as_view(), name="delete"),
]
