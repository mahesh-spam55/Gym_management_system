from datetime import date
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

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
