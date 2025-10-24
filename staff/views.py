from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.views.generic import CreateView, ListView, DetailView, DeleteView, UpdateView
from django.urls import reverse_lazy
from django.views import View
from django.shortcuts import redirect, get_object_or_404
from django.db import transaction

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

    def form_valid(self, form):
        # Assign next position at the end of the list
        last = Staff.objects.order_by("-position").first()
        form.instance.position = (last.position + 1) if last else 1
        return super().form_valid(form)


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


class StaffMoveUpView(LoginRequiredMixin, View):
    def post(self, request, pk):
        # Normalize positions to be consecutive starting at 1
        with transaction.atomic():
            ordered = list(Staff.objects.select_for_update().order_by("position", "name"))
            for i, obj in enumerate(ordered, start=1):
                if obj.position != i:
                    obj.position = i
                    obj.save(update_fields=["position"])
        staff_qs = list(Staff.objects.all())
        try:
            idx = next(i for i, s in enumerate(staff_qs) if s.pk == pk)
        except StopIteration:
            return redirect("staff:list")
        if idx == 0:
            return redirect("staff:list")
        current = staff_qs[idx]
        prev = staff_qs[idx - 1]
        with transaction.atomic():
            current.position, prev.position = prev.position, current.position
            current.save(update_fields=["position"])
            prev.save(update_fields=["position"])
        return redirect("staff:list")


class StaffMoveDownView(LoginRequiredMixin, View):
    def post(self, request, pk):
        # Normalize positions to be consecutive starting at 1
        with transaction.atomic():
            ordered = list(Staff.objects.select_for_update().order_by("position", "name"))
            for i, obj in enumerate(ordered, start=1):
                if obj.position != i:
                    obj.position = i
                    obj.save(update_fields=["position"])
        staff_qs = list(Staff.objects.all())
        try:
            idx = next(i for i, s in enumerate(staff_qs) if s.pk == pk)
        except StopIteration:
            return redirect("staff:list")
        if idx == len(staff_qs) - 1:
            return redirect("staff:list")
        current = staff_qs[idx]
        nxt = staff_qs[idx + 1]
        with transaction.atomic():
            current.position, nxt.position = nxt.position, current.position
            current.save(update_fields=["position"])
            nxt.save(update_fields=["position"])
        return redirect("staff:list")

