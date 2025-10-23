from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from datetime import date

from .models import Member
from .forms import MemberForm


class CustomerListView(LoginRequiredMixin, ListView):
    model = Member
    context_object_name = "members"
    template_name = "customers/list.html"

    def get_queryset(self):
        qs = super().get_queryset()
        joined_on = self.request.GET.get("joined_on")
        joined_month = self.request.GET.get("joined_month")
        if joined_on:
            try:
                d = date.fromisoformat(joined_on)
                qs = qs.filter(date_of_joining=d)
            except ValueError:
                pass
        elif joined_month:
            try:
                y, m = joined_month.split("-")
                y, m = int(y), int(m)
                month_start = date(y, m, 1)
                if m == 12:
                    next_month_start = date(y + 1, 1, 1)
                else:
                    next_month_start = date(y, m + 1, 1)
                qs = qs.filter(date_of_joining__gte=month_start, date_of_joining__lt=next_month_start)
            except Exception:
                pass
        return qs


class MemberDetailView(LoginRequiredMixin, DetailView):
    model = Member
    template_name = "customers/detail.html"


class MemberCreateView(LoginRequiredMixin, CreateView):
    model = Member
    form_class = MemberForm
    template_name = "customers/form.html"

    def get_success_url(self):
        return reverse("members:detail", args=[self.object.pk])


class MemberUpdateView(LoginRequiredMixin, UpdateView):
    model = Member
    form_class = MemberForm
    template_name = "customers/form.html"

    def get_success_url(self):
        return reverse("members:detail", args=[self.object.pk])


class MemberDeleteView(LoginRequiredMixin, DeleteView):
    model = Member
    template_name = "customers/confirm_delete.html"
    success_url = reverse_lazy("members:list")
