from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from django.utils import timezone
from django.db.models import Sum
import calendar
from datetime import date, timedelta

from customers.models import Member
from fees.models import Payment


class HomeView(LoginRequiredMixin, TemplateView):
    template_name = "accounts/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Dates for current month
        today = timezone.localdate()
        # Allow navigation via query params (?year=YYYY&month=MM)
        try:
            q_year = int(self.request.GET.get("year", today.year))
            q_month = int(self.request.GET.get("month", today.month))
            month_start = date(q_year, q_month, 1)
        except Exception:
            month_start = today.replace(day=1)
        # Next month start for range end
        if month_start.month == 12:
            next_month_start = month_start.replace(year=month_start.year + 1, month=1)
        else:
            next_month_start = month_start.replace(month=month_start.month + 1)

        # Metrics
        total_members = Member.objects.count()
        # Treat "new bookings" as members who joined this month
        current_month_bookings = Member.objects.filter(
            date_of_joining__gte=month_start,
            date_of_joining__lt=next_month_start,
        ).count()
        # Compute totals safely even if no rows
        total_revenue = Payment.objects.aggregate(total=Sum("amount")).get("total") or 0
        current_month_revenue = (
            Payment.objects.filter(paid_on__gte=month_start, paid_on__lt=next_month_start)
            .aggregate(total=Sum("amount"))
            .get("total")
            or 0
        )

        context.update(
            {
                "dash_total_members": total_members,
                "dash_current_month_bookings": current_month_bookings,
                "dash_total_revenue": total_revenue,
                "dash_current_month_revenue": current_month_revenue,
                "dash_month_label": month_start.strftime("%B %Y"),
                "today_date": today,
                "dash_month_param": f"{month_start.year}-{month_start.month:02d}",
            }
        )

        # Build calendar weeks for current month (Mon-Sun)
        cal = calendar.Calendar(firstweekday=6)  # Sunday=6
        month_dates = list(cal.itermonthdates(month_start.year, month_start.month))
        # Prefetch counts for payments and new members by date
        payments_by_day = (
            Payment.objects.filter(paid_on__gte=month_dates[0], paid_on__lte=month_dates[-1])
            .values_list("paid_on")
        )
        members_by_day = (
            Member.objects.filter(date_of_joining__gte=month_dates[0], date_of_joining__lte=month_dates[-1])
            .values_list("date_of_joining")
        )
        pay_count = {}
        for (d,) in payments_by_day:
            pay_count[d] = pay_count.get(d, 0) + 1
        mem_count = {}
        for (d,) in members_by_day:
            mem_count[d] = mem_count.get(d, 0) + 1

        weeks = []
        week = []
        for d in month_dates:
            day_info = {
                "date": d,
                "in_month": d.month == month_start.month,
                "payments": pay_count.get(d, 0),
                "new_members": mem_count.get(d, 0),
            }
            week.append(day_info)
            if len(week) == 7:
                weeks.append(week)
                week = []
        if week:
            weeks.append(week)

        context["calendar_weeks"] = weeks
        context["weekday_labels"] = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"]

        # Prev/Next month params for navigation
        if month_start.month == 1:
            prev_year, prev_month = month_start.year - 1, 12
        else:
            prev_year, prev_month = month_start.year, month_start.month - 1
        if month_start.month == 12:
            next_year, next_month = month_start.year + 1, 1
        else:
            next_year, next_month = month_start.year, month_start.month + 1

        # Earnings sparkline data (last 6 months, oldest -> newest)
        def month_add(y: int, m: int, delta: int):
            total = (y * 12 + (m - 1)) + delta
            ny, nm = divmod(total, 12)
            return ny, nm + 1

        months = []
        for i in range(-5, 1):
            y, m = month_add(month_start.year, month_start.month, i)
            months.append((y, m))

        values = []
        for (y, m) in months:
            start = date(y, m, 1)
            ny, nm = month_add(y, m, 1)
            end = date(ny, nm, 1)
            amt = (
                Payment.objects.filter(paid_on__gte=start, paid_on__lt=end)
                .aggregate(total=Sum("amount"))
                .get("total")
                or 0
            )
            values.append(float(amt))

        max_val = max(values) if values else 1.0
        if max_val == 0:
            max_val = 1.0
        # Build polyline points in viewBox 0 0 100 30
        n = len(values) if values else 1
        points = []
        for idx, v in enumerate(values):
            x = 0 if n == 1 else (idx * (100.0 / (n - 1)))
            y = 29.0 - (v / max_val) * 26.0  # top padding 3, bottom 1
            points.append(f"{x:.2f},{y:.2f}")

        month_labels = [f"{calendar.month_abbr[m]} {y}" for (y, m) in months]

        context.update(
            {
                "cal_year": month_start.year,
                "cal_month": month_start.month,
                "prev_year": prev_year,
                "prev_month": prev_month,
                "next_year": next_year,
                "next_month": next_month,
                "earnings_spark_points": " ".join(points),
                "earnings_spark_labels": month_labels,
                "earnings_spark_values": values,
            }
        )

        # Detailed chart data
        # 1) Calendar year totals (Jan -> Dec of the selected year)
        year = month_start.year
        months12 = [(year, m) for m in range(1, 13)]
        monthly_labels = [f"{calendar.month_abbr[m]} {y}" for (y, m) in months12]
        monthly_values = []
        for (y, m) in months12:
            start = date(y, m, 1)
            ny, nm = month_add(y, m, 1)
            end = date(ny, nm, 1)
            amt = (
                Payment.objects.filter(paid_on__gte=start, paid_on__lt=end)
                .aggregate(total=Sum("amount"))
                .get("total")
                or 0
            )
            monthly_values.append(float(amt))

        # 2) Daily totals for the selected month
        # Build days from month_start to next_month_start - 1
        day = month_start
        daily_labels = []
        daily_values = []
        while day < next_month_start:
            amt = (
                Payment.objects.filter(paid_on=day)
                .aggregate(total=Sum("amount"))
                .get("total")
                or 0
            )
            daily_labels.append(day.day)
            daily_values.append(float(amt))
            day = day.replace(day=day.day + 1) if day.day + 1 <= 28 else (day + timedelta(days=1))

        context.update(
            {
                "earnings_monthly_labels": monthly_labels,
                "earnings_monthly_values": monthly_values,
                "earnings_daily_labels": daily_labels,
                "earnings_daily_values": daily_values,
            }
        )
        return context
