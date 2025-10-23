from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.views.generic import ListView, CreateView, DeleteView
from django.urls import reverse_lazy
from datetime import date

from .models import Payment
from .forms import PaymentForm
from .utils import add_months


class PaymentListView(LoginRequiredMixin, ListView):
    model = Payment
    context_object_name = "payments"
    template_name = "fees/list.html"

    def get_queryset(self):
        qs = super().get_queryset()
        paid_on = self.request.GET.get("paid_on")
        paid_month = self.request.GET.get("paid_month")
        if paid_on:
            try:
                d = date.fromisoformat(paid_on)
                qs = qs.filter(paid_on=d)
            except ValueError:
                pass
        elif paid_month:
            try:
                y, m = paid_month.split("-")
                y, m = int(y), int(m)
                start = date(y, m, 1)
                # compute next month start
                if m == 12:
                    end = date(y + 1, 1, 1)
                else:
                    end = date(y, m + 1, 1)
                qs = qs.filter(paid_on__gte=start, paid_on__lt=end)
            except Exception:
                pass
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = PaymentForm()
        return context


class PaymentCreateView(LoginRequiredMixin, CreateView):
    model = Payment
    form_class = PaymentForm
    template_name = "fees/form.html"

    def get_success_url(self):
        return reverse("fees:list")

    def form_valid(self, form):
        response = super().form_valid(form)
        payment: Payment = self.object
        member = payment.member

        # Map membership_type to months
        type_to_months = {
            payment.MembershipType.THREE: 3,
            payment.MembershipType.SIX: 6,
            payment.MembershipType.NINE: 9,
            payment.MembershipType.TWELVE: 12,
        }
        months = type_to_months.get(payment.membership_type, 0)

        # Determine start base date
        candidates = [payment.paid_on]
        if member.membership_due_date:
            candidates.append(member.membership_due_date)
        if member.date_of_joining:
            candidates.append(member.date_of_joining)
        start_base = max(candidates)

        # Compute new due date and save on member
        if months > 0:
            member.membership_due_date = add_months(start_base, months)
            member.save(update_fields=["membership_due_date"])

        return response


class PaymentDeleteView(LoginRequiredMixin, DeleteView):
    model = Payment
    template_name = "fees/confirm_delete.html"
    success_url = reverse_lazy("fees:list")
