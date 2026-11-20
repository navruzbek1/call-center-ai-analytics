from datetime import date

from callanalytics.periods import (
    last_days_range,
    last_months_range,
    month_range,
    prev_month_range,
    prev_week_range,
    share_pct,
    top_n,
    week_range,
)

WED = date(2026, 11, 18)  # chorshanba


def test_week_range_starts_on_monday():
    assert week_range(WED) == (date(2026, 11, 16), WED)


def test_prev_week_is_cut_to_the_same_weekday():
    assert prev_week_range(WED) == (date(2026, 11, 9), date(2026, 11, 11))


def test_month_range():
    assert month_range(WED) == (date(2026, 11, 1), WED)


def test_prev_month_same_day():
    assert prev_month_range(WED) == (date(2026, 10, 1), date(2026, 10, 18))


def test_prev_month_is_clamped_to_shorter_month():
    assert prev_month_range(date(2026, 3, 31)) == (date(2026, 2, 1), date(2026, 2, 28))


def test_last_days_includes_target():
    assert last_days_range(WED, 7) == (date(2026, 11, 12), WED)


def test_last_months_example_from_docstring():
    assert last_months_range(date(2026, 10, 5), 1) == (date(2026, 9, 6), date(2026, 10, 5))


def test_last_months_across_year_boundary():
    assert last_months_range(date(2026, 1, 15), 2) == (date(2025, 11, 16), date(2026, 1, 15))


def test_top_n_and_share():
    counts = {"a": 5, "b": 9, "c": 1}
    assert top_n(counts, 2) == [("b", 9), ("a", 5)]
    assert share_pct(1, 4) == "25.0%"
    assert share_pct(3, 0) == "0%"
