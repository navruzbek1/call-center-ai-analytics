"""README uchun sxematik rasmlarni yaratadi. Haqiqiy ma'lumot ishlatilmaydi.

    PYTHONPATH=. python docs/make_images.py
"""

from datetime import date
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch

from callanalytics.periods import prev_week_range, share_pct, top_n, week_range

OUT = Path(__file__).parent / "img"
OUT.mkdir(exist_ok=True)

GREEN, AMBER, BLUE = "#16a34a", "#f59e0b", "#2563eb"
NAVY, GRAY, LIGHT = "#0f172a", "#64748b", "#eff6ff"


def arrow(ax, p1, p2):
    ax.add_patch(FancyArrowPatch(p1, p2, arrowstyle="-|>", mutation_scale=18, color=GRAY, lw=2))


def stage(ax, x, y, w, h, title, sub, tag):
    if tag == "desc":
        fc, ec, ls, tc, sc = "#f8fafc", "#94a3b8", "--", GRAY, "#94a3b8"
        label, lc = "faqat tavsif", "#94a3b8"
    else:
        fc, ec, ls, tc, sc = LIGHT, BLUE, "-", NAVY, GRAY
        label, lc = ("kodi repoda", GREEN) if tag == "code" else ("qisman kod", AMBER)
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.02,rounding_size=0.12", fc=fc, ec=ec, lw=2, ls=ls))
    ax.text(x + w / 2, y + h * 0.64, title, ha="center", va="center", fontsize=12, fontweight="bold", color=tc)
    ax.text(x + w / 2, y + h * 0.3, sub, ha="center", va="center", fontsize=9.3, color=sc)
    ax.text(x + w - 0.08, y + h + 0.02, label, ha="right", va="bottom", fontsize=8.5, fontweight="bold",
            color="white", bbox={"boxstyle": "round,pad=0.25", "fc": lc, "ec": "none"})


def pipeline():
    fig, ax = plt.subplots(figsize=(14, 6.4))
    ax.set_xlim(0, 14)
    ax.set_ylim(0, 6.4)
    ax.axis("off")
    ax.text(7, 6.0, "Tizim qanday ishlaydi", ha="center", fontsize=17, fontweight="bold", color=NAVY)
    w, h = 3.0, 1.35
    row1 = [
        ("CRM telefoniya", "qo'ng'iroq yozuvi, holat: new", "desc"),
        ("Navbat", "new > processing > success / error", "desc"),
        ("Gemini", "audio > JSON sxema, qayta urinish", "partial"),
        ("Tekshiruv", "modul-kategoriya, ishonch, AI baho", "code"),
    ]
    xs = [0.4 + i * 3.4 for i in range(4)]
    for (t, s, tag), x in zip(row1, xs, strict=True):
        stage(ax, x, 3.7, w, h, t, s, tag)
    for i in range(3):
        arrow(ax, (xs[i] + w + 0.03, 4.375), (xs[i + 1] - 0.03, 4.375))
    row2 = [
        ("PostgreSQL", "natija + token sarfi va narxi", "desc"),
        ("CRM'ga qaytarish", "natija maydonlarga yoziladi", "desc"),
        ("Telegram bot", "TOP-10, davr solishtirish, xarajat", "partial"),
    ]
    xs2 = [xs[3] - i * 3.4 for i in range(3)]
    for (t, s, tag), x in zip(row2, xs2, strict=True):
        stage(ax, x, 0.9, w, h, t, s, tag)
    for i in range(2):
        arrow(ax, (xs2[i] - 0.03, 1.575), (xs2[i + 1] + w + 0.03, 1.575))
    arrow(ax, (xs[3] + w / 2, 3.68), (xs2[0] + w / 2, 2.27))
    ax.text(7, 0.3, "Qo'ng'iroq yozuvlari va natijalar faqat ichki tizimda saqlanadi, bu repoda yo'q.",
            ha="center", fontsize=11, color=GRAY, style="italic")
    fig.savefig(OUT / "pipeline.png", dpi=150, bbox_inches="tight", facecolor="white")
    plt.close(fig)


def top_chart():
    today = date(2026, 11, 18)
    this_week = {"Kassa-Printer": 41, "Kassa-Smena yopilmayapti": 33, "Ombor-Kirim": 29, "Sinxronizatsiya": 22,
                 "Kassa-To'lov o'tmayapti": 18, "Ombor-Narx o'zgartirish": 14, "Login muammosi": 9,
                 "Noto'g'ri murojaat": 6}
    last_week = {"Kassa-Printer": 35, "Kassa-Smena yopilmayapti": 38, "Ombor-Kirim": 21, "Sinxronizatsiya": 30,
                 "Kassa-To'lov o'tmayapti": 11, "Ombor-Narx o'zgartirish": 16, "Login muammosi": 12,
                 "Noto'g'ri murojaat": 7}
    rows = top_n(this_week, 8)
    total = sum(this_week.values())
    names = [n for n, _ in rows][::-1]
    cur = [this_week[n] for n in names]
    prev = [last_week.get(n, 0) for n in names]
    (ws, we), (ps, pe) = week_range(today), prev_week_range(today)

    fig, ax = plt.subplots(figsize=(13, 6.2))
    y = range(len(names))
    ax.barh([i + 0.2 for i in y], cur, height=0.38, color=BLUE, label=f"Bu hafta ({ws:%d.%m}-{we:%d.%m})")
    ax.barh([i - 0.2 for i in y], prev, height=0.38, color="#cbd5e1",
            label=f"O'tgan haftaning shu kungacha qismi ({ps:%d.%m}-{pe:%d.%m})")
    for i, (c, p) in enumerate(zip(cur, prev, strict=True)):
        diff = c - p
        color = "#dc2626" if diff > 0 else GREEN
        ax.text(c + 0.6, i + 0.2, f"{c}  ({share_pct(c, total)})", va="center", fontsize=10, color=NAVY)
        ax.text(58, i, f"{'+' if diff > 0 else ''}{diff}", ha="right", va="center", fontsize=11, fontweight="bold",
                color=color)
    ax.set_yticks(list(y))
    ax.set_yticklabels(names, fontsize=11)
    ax.set_xlim(0, 60)
    for spine in ("top", "right"):
        ax.spines[spine].set_visible(False)
    ax.text(58, len(names) - 0.35, "farq", ha="right", va="center", fontsize=10, color=GRAY)
    ax.legend(loc="lower right", bbox_to_anchor=(0.93, 0), fontsize=10, frameon=False)
    ax.set_title("TOP sabab kategoriyalari: adolatli haftalik solishtirish (uydirma ma'lumot)", loc="left",
                 fontsize=15, fontweight="bold", color=NAVY, pad=14)
    fig.savefig(OUT / "top-categories.png", dpi=150, bbox_inches="tight", facecolor="white")
    plt.close(fig)


if __name__ == "__main__":
    pipeline()
    top_chart()
    print("Rasmlar yaratildi:", ", ".join(sorted(p.name for p in OUT.glob("*.png"))))
