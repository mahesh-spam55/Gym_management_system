from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.views import View
from django.shortcuts import redirect
from django.db import transaction
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

    def form_valid(self, form):
        # assign next position at end
        last = Member.objects.order_by("-position").first()
        form.instance.position = (last.position + 1) if last else 1
        return super().form_valid(form)


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


class MemberMoveUpView(LoginRequiredMixin, View):
    def post(self, request, pk):
        # normalize positions to consecutive values starting from 1
        with transaction.atomic():
            ordered = list(Member.objects.select_for_update().order_by("position", "name"))
            for i, obj in enumerate(ordered, start=1):
                if obj.position != i:
                    obj.position = i
                    obj.save(update_fields=["position"])
        members = list(Member.objects.all())
        try:
            idx = next(i for i, m in enumerate(members) if m.pk == pk)
        except StopIteration:
            return redirect("members:list")
        if idx == 0:
            return redirect("members:list")
        current = members[idx]
        prev = members[idx - 1]
        with transaction.atomic():
            current.position, prev.position = prev.position, current.position
            current.save(update_fields=["position"])
            prev.save(update_fields=["position"])
        return redirect("members:list")


class MemberMoveDownView(LoginRequiredMixin, View):
    def post(self, request, pk):
        # normalize positions to consecutive values starting from 1
        with transaction.atomic():
            ordered = list(Member.objects.select_for_update().order_by("position", "name"))
            for i, obj in enumerate(ordered, start=1):
                if obj.position != i:
                    obj.position = i
                    obj.save(update_fields=["position"])
        members = list(Member.objects.all())
        try:
            idx = next(i for i, m in enumerate(members) if m.pk == pk)
        except StopIteration:
            return redirect("members:list")
        if idx == len(members) - 1:
            return redirect("members:list")
        current = members[idx]
        nxt = members[idx + 1]
        with transaction.atomic():
            current.position, nxt.position = nxt.position, current.position
            current.save(update_fields=["position"])
            nxt.save(update_fields=["position"])
        return redirect("members:list")
