"""Hisobot davrlari va adolatli solishtirish (bu hafta va o'tgan haftaning AYNAN shu kungacha qismi)."""

from datetime import date, timedelta


def week_range(target: date) -> tuple[date, date]:
    """Dushanbadan target sanagacha (shu hafta, hozirgacha)."""
    monday = target - timedelta(days=target.weekday())
    return monday, target


def prev_week_range(target: date) -> tuple[date, date]:
    """O'tgan haftaning aynan shu kungacha bo'lgan qismi (adolatli solishtirish uchun)."""
    this_monday = target - timedelta(days=target.weekday())
    last_monday = this_monday - timedelta(days=7)
    days_in = (target - this_monday).days
    return last_monday, last_monday + timedelta(days=days_in)


def month_range(target: date) -> tuple[date, date]:
    """Oyning 1-sanasidan target sanagacha (shu oy, hozirgacha)."""
    return target.replace(day=1), target


def prev_month_range(target: date) -> tuple[date, date]:
    """O'tgan oyning aynan shu kungacha bo'lgan qismi (adolatli solishtirish uchun)."""
    first_this = target.replace(day=1)
    last_day_prev_month = first_this - timedelta(days=1)
    first_prev = last_day_prev_month.replace(day=1)
    day_offset = target.day - 1
    end_prev = min(first_prev + timedelta(days=day_offset), last_day_prev_month)
    return first_prev, end_prev


def last_days_range(target: date, days: int) -> tuple[date, date]:
    """target sanani ham qo'shib, oxirgi `days` kun (masalan 7 -> 7 kunlik oyna)."""
    return target - timedelta(days=days - 1), target


def last_months_range(target: date, months: int) -> tuple[date, date]:
    """target sanani ham qo'shib, oxirgi `months` oy (masalan 5-okt, 1 oy -> 6-sen..5-okt)."""
    month_index = target.year * 12 + target.month - 1 - months
    year, month0 = divmod(month_index, 12)
    month = month0 + 1
    next_month_first = date(year + month // 12, month % 12 + 1, 1)
    last_day = (next_month_first - timedelta(days=1)).day
    start = date(year, month, min(target.day, last_day)) + timedelta(days=1)
    return start, target


def top_n(counts: dict[str, int], n: int = 10) -> list[tuple[str, int]]:
    return sorted(counts.items(), key=lambda kv: kv[1], reverse=True)[:n]


def share_pct(cnt: int, total: int) -> str:
    return f"{100 * cnt / total:.1f}%" if total else "0%"
