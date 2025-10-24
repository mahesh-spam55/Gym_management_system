from datetime import date
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.views import View
from django.shortcuts import redirect
from django.db import transaction

from .models import Trainer
from .forms import TrainerForm


class TrainerListView(LoginRequiredMixin, ListView):
    model = Trainer
    context_object_name = "trainers"
    template_name = "trainers/list.html"


class TrainerDetailView(LoginRequiredMixin, DetailView):
    model = Trainer
    template_name = "trainers/detail.html"


class TrainerCreateView(LoginRequiredMixin, CreateView):
    model = Trainer
    form_class = TrainerForm
    template_name = "trainers/form.html"

    def get_success_url(self):
        return reverse("trainers:detail", args=[self.object.pk])

    def form_valid(self, form):
        # Ensure date_of_joining has a value even though it's not on the form
        if not form.instance.date_of_joining:
            form.instance.date_of_joining = date.today()
        # Assign next position at end
        last = Trainer.objects.order_by("-position").first()
        form.instance.position = (last.position + 1) if last else 1
        return super().form_valid(form)


class TrainerUpdateView(LoginRequiredMixin, UpdateView):
    model = Trainer
    form_class = TrainerForm
    template_name = "trainers/form.html"

    def get_success_url(self):
        return reverse("trainers:detail", args=[self.object.pk])


class TrainerDeleteView(LoginRequiredMixin, DeleteView):
    model = Trainer
    template_name = "trainers/confirm_delete.html"
    success_url = reverse_lazy("trainers:list")


class TrainerMoveUpView(LoginRequiredMixin, View):
    def post(self, request, pk):
        # Normalize positions to consecutive values starting from 1
        with transaction.atomic():
            ordered = list(Trainer.objects.select_for_update().order_by("position", "first_name", "last_name"))
            for i, obj in enumerate(ordered, start=1):
                if obj.position != i:
                    obj.position = i
                    obj.save(update_fields=["position"])
        trainers = list(Trainer.objects.all())
        try:
            idx = next(i for i, t in enumerate(trainers) if t.pk == pk)
        except StopIteration:
            return redirect("trainers:list")
        if idx == 0:
            return redirect("trainers:list")
        current = trainers[idx]
        prev = trainers[idx - 1]
        with transaction.atomic():
            current.position, prev.position = prev.position, current.position
            current.save(update_fields=["position"])
            prev.save(update_fields=["position"])
        return redirect("trainers:list")


class TrainerMoveDownView(LoginRequiredMixin, View):
    def post(self, request, pk):
        # Normalize positions to consecutive values starting from 1
        with transaction.atomic():
            ordered = list(Trainer.objects.select_for_update().order_by("position", "first_name", "last_name"))
            for i, obj in enumerate(ordered, start=1):
                if obj.position != i:
                    obj.position = i
                    obj.save(update_fields=["position"])
        trainers = list(Trainer.objects.all())
        try:
            idx = next(i for i, t in enumerate(trainers) if t.pk == pk)
        except StopIteration:
            return redirect("trainers:list")
        if idx == len(trainers) - 1:
            return redirect("trainers:list")
        current = trainers[idx]
        nxt = trainers[idx + 1]
        with transaction.atomic():
            current.position, nxt.position = nxt.position, current.position
            current.save(update_fields=["position"])
            nxt.save(update_fields=["position"])
        return redirect("trainers:list")
