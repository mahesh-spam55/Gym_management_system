from django.urls import path
from .views import PaymentListView, PaymentCreateView, PaymentDeleteView

app_name = "fees"

urlpatterns = [
    path("", PaymentListView.as_view(), name="list"),
    path("create/", PaymentCreateView.as_view(), name="create"),
    path("<int:pk>/delete/", PaymentDeleteView.as_view(), name="delete"),
]
