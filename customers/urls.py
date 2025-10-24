from django.urls import path
from .views import (
    CustomerListView,
    MemberDetailView,
    MemberCreateView,
    MemberUpdateView,
    MemberDeleteView,
    MemberMoveUpView,
    MemberMoveDownView,
)

app_name = "members"

urlpatterns = [
    path("", CustomerListView.as_view(), name="list"),
    path("create/", MemberCreateView.as_view(), name="create"),
    path("<int:pk>/", MemberDetailView.as_view(), name="detail"),
    path("<int:pk>/edit/", MemberUpdateView.as_view(), name="edit"),
    path("<int:pk>/delete/", MemberDeleteView.as_view(), name="delete"),
    path("<int:pk>/move-up/", MemberMoveUpView.as_view(), name="move_up"),
    path("<int:pk>/move-down/", MemberMoveDownView.as_view(), name="move_down"),
]
