from django.urls import path

from .views import StaffCreateView, StaffListView, StaffDetailView, StaffDeleteView, StaffUpdateView

app_name = "staff"

urlpatterns = [
    path("", StaffListView.as_view(), name="list"),
    path("create/", StaffCreateView.as_view(), name="create"),
    path("add/", StaffCreateView.as_view(), name="add"),
    path("<int:pk>/", StaffDetailView.as_view(), name="detail"),
    path("<int:pk>/edit/", StaffUpdateView.as_view(), name="edit"),
    path("<int:pk>/delete/", StaffDeleteView.as_view(), name="delete"),
]
