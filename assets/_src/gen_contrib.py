# -*- coding: utf-8 -*-
"""Contribution grid, drawn from GitHub's public contributions endpoint.

ghchart only takes a single base colour, so its empty cells stay near-white and
look wrong on a dark page. Drawing it here gives a proper tonal ramp per theme.
Re-run (or let the weekly workflow run) to refresh.
"""
import re
import subprocess
from datetime import date

import os
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
USER = "rudtjr1106"
KR = "'Apple SD Gothic Neo','Pretendard','Noto Sans KR','Malgun Gothic',system-ui,sans-serif"

SCHEMES = {
    "light": dict(surface="#E9F3EB", on="#0D2015", var="#456150",
                  ramp=["#D3E6D9", "#A7E5C2", "#6FD79C", "#2FA96A", "#00693C"]),
    "dark":  dict(surface="#0F2318", on="#DCE9DF", var="#A6C3AE",
                  ramp=["#1D3D2A", "#216B46", "#2E9E63", "#45C783", "#7BF0AE"]),
}

CELL, GAP = 11, 3
PITCH = CELL + GAP
MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
          "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]


def fetch():
    html = subprocess.run(
        ["curl", "-sL", f"https://github.com/users/{USER}/contributions"],
        capture_output=True, text=True).stdout
    pat = re.compile(
        r'data-date="(\d{4})-(\d{2})-(\d{2})"[^>]*'
        r'id="contribution-day-component-(\d+)-(\d+)"[^>]*data-level="(\d)"')
    days = []
    for y, m, d, row, col, lvl in pat.findall(html):
        days.append((date(int(y), int(m), int(d)), int(row), int(col), int(lvl)))
    if not days:
        raise SystemExit("contribution grid could not be parsed")
    return days


def card(c, days):
    cols = max(d[2] for d in days) + 1
    LEFT, TOP, PAD = 34, 52, 26
    grid_w = cols * PITCH - GAP
    W = PAD * 2 + LEFT + grid_w
    H = TOP + 7 * PITCH + 44

    o = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" '
         f'role="img" font-family="{KR}">',
         f'  <rect width="{W}" height="{H}" rx="28" fill="{c["surface"]}"/>']

    first_of_col = {}
    for dt, row, col, lvl in days:
        first_of_col.setdefault(col, dt)
    prev = None
    for col in sorted(first_of_col):
        m = first_of_col[col].month
        if m != prev:
            o.append(f'  <text x="{PAD + LEFT + col * PITCH}" y="{TOP - 10}" font-size="11" '
                     f'fill="{c["var"]}">{MONTHS[m - 1]}</text>')
            prev = m

    for i, label in ((1, "Mon"), (3, "Wed"), (5, "Fri")):
        o.append(f'  <text x="{PAD}" y="{TOP + i * PITCH + 10}" font-size="10" '
                 f'fill="{c["var"]}">{label}</text>')

    for dt, row, col, lvl in days:
        o.append(f'  <rect x="{PAD + LEFT + col * PITCH}" y="{TOP + row * PITCH}" '
                 f'width="{CELL}" height="{CELL}" rx="2.5" fill="{c["ramp"][lvl]}"/>')

    lx = PAD + LEFT + grid_w - 128
    ly = TOP + 7 * PITCH + 20
    o.append(f'  <text x="{lx - 6}" y="{ly + 9}" font-size="10.5" fill="{c["var"]}" '
             f'text-anchor="end">적음</text>')
    for i in range(5):
        o.append(f'  <rect x="{lx + i * 15}" y="{ly}" width="{CELL}" height="{CELL}" rx="2.5" '
                 f'fill="{c["ramp"][i]}"/>')
    o.append(f'  <text x="{lx + 5 * 15 + 2}" y="{ly + 9}" font-size="10.5" fill="{c["var"]}">많음</text>')

    o.append("</svg>")
    return "\n".join(o) + "\n"


days = fetch()
print(f"{len(days)}일, {days[0][0]} ~ {max(d[0] for d in days)}")
for name, c in SCHEMES.items():
    open(f"{OUT}/contrib-{name}.svg", "w", encoding="utf-8").write(card(c, days))
print("contrib cards written")
