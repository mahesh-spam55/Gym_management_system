from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.views.generic import CreateView, ListView, DetailView, DeleteView, UpdateView
from django.urls import reverse_lazy

from .models import Staff


class StaffListView(LoginRequiredMixin, ListView):
    model = Staff
    context_object_name = "staff"
    template_name = "staff/list.html"


class StaffDetailView(LoginRequiredMixin, DetailView):
    model = Staff
    template_name = "staff/detail.html"


class StaffCreateView(LoginRequiredMixin, CreateView):
    model = Staff
    fields = [
        "staff_id",
        "name",
        "contact",
        "role",
    ]
    template_name = "staff/form.html"

    def get_success_url(self):
        return reverse("staff:detail", args=[self.object.pk])


class StaffDeleteView(LoginRequiredMixin, DeleteView):
    model = Staff
    template_name = "staff/confirm_delete.html"
    success_url = reverse_lazy("staff:list")


class StaffUpdateView(LoginRequiredMixin, UpdateView):
    model = Staff
    fields = [
        "staff_id",
        "name",
        "contact",
        "role",
    ]
    template_name = "staff/form.html"

    def get_success_url(self):
        return reverse("staff:detail", args=[self.object.pk])
