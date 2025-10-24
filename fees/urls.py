from django.urls import path
from .views import PaymentListView, PaymentCreateView, PaymentDeleteView, PaymentUpdateView

app_name = "fees"

urlpatterns = [
    path("", PaymentListView.as_view(), name="list"),
    path("create/", PaymentCreateView.as_view(), name="create"),
    path("<int:pk>/edit/", PaymentUpdateView.as_view(), name="edit"),
    path("<int:pk>/delete/", PaymentDeleteView.as_view(), name="delete"),
]
