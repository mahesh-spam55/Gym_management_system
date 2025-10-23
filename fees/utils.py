from datetime import date


def add_months(base: date, months: int) -> date:
    """Add months to a date, clamping the day to the end of the target month.
    Example: Jan 31 + 1 month -> Feb 28/29.
    """
    year = base.year + (base.month - 1 + months) // 12
    month = (base.month - 1 + months) % 12 + 1
    # Determine last day of target month
    if month in (1, 3, 5, 7, 8, 10, 12):
        last_day = 31
    elif month in (4, 6, 9, 11):
        last_day = 30
    else:
        # February, handle leap year
        y = year
        is_leap = (y % 4 == 0 and (y % 100 != 0 or y % 400 == 0))
        last_day = 29 if is_leap else 28
    day = min(base.day, last_day)
    return date(year, month, day)
