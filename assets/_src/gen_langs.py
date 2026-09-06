# -*- coding: utf-8 -*-
"""Language-mix card, generated from the GitHub API rather than a third-party
badge service — the popular ones (github-readme-stats, activity-graph) were down
when this was built, and a self-generated card also matches the palette exactly.

Needs network. Re-run to refresh the numbers.
"""
import json
import subprocess
import collections

import os
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
USER = "rudtjr1106"
KR = "'Apple SD Gothic Neo','Pretendard','Noto Sans KR','Malgun Gothic',system-ui,sans-serif"

SCHEMES = {
    "light": dict(surface="#E9F3EB", on="#0D2015", var="#456150", track="#CBE3D3",
                  tones=["#00693C", "#6B4EA8", "#7A5300", "#00796B", "#A03E1E"]),
    "dark":  dict(surface="#0F2318", on="#DCE9DF", var="#A6C3AE", track="#1D3D2A",
                  tones=["#5CDD95", "#D2BBFF", "#FFD489", "#6FE3CD", "#FFA98A"]),
}


def api(path):
    out = subprocess.run(["curl", "-sL", f"https://api.github.com{path}"],
                         capture_output=True, text=True).stdout
    return json.loads(out)


def collect():
    repos = [r["name"] for r in api(f"/users/{USER}/repos?per_page=100") if not r["fork"]]
    tot = collections.Counter()
    for r in repos:
        for lang, n in api(f"/repos/{USER}/{r}/languages").items():
            tot[lang] += n
    return repos, tot


def card(c, rows, total, repo_count):
    W, PAD = 880, 30
    BAR_Y, BAR_H, BAR_W = 74, 22, W - PAD * 2
    H = 196
    o = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" '
         f'role="img" font-family="{KR}">',
         f'  <rect width="{W}" height="{H}" rx="28" fill="{c["surface"]}"/>',
         f'  <text x="{PAD}" y="44" font-size="15" font-weight="700" fill="{c["on"]}">'
         f'공개 저장소 {repo_count}개에 쓴 언어</text>',
         f'  <text x="{PAD}" y="62" font-size="12" fill="{c["var"]}">'
         f'GitHub API 기준, 총 {total // 1024:,} KB</text>',
         f'  <clipPath id="bar"><rect x="{PAD}" y="{BAR_Y}" width="{BAR_W}" height="{BAR_H}" '
         f'rx="{BAR_H // 2}"/></clipPath>',
         f'  <g clip-path="url(#bar)">']
    x = PAD
    for i, (name, share) in enumerate(rows):
        w = BAR_W * share
        fill = c["tones"][i] if i < len(c["tones"]) else c["track"]
        o.append(f'    <rect x="{x:.1f}" y="{BAR_Y}" width="{w + 1:.1f}" height="{BAR_H}" fill="{fill}"/>')
        x += w
    o.append(f'    <rect x="{x:.1f}" y="{BAR_Y}" width="{PAD + BAR_W - x + 1:.1f}" '
             f'height="{BAR_H}" fill="{c["track"]}"/>')
    o.append("  </g>")

    col_w = BAR_W / 3
    for i, (name, share) in enumerate(rows):
        cx = PAD + (i % 3) * col_w
        cy = 134 + (i // 3) * 30
        fill = c["tones"][i] if i < len(c["tones"]) else c["track"]
        o.append(f'  <circle cx="{cx + 6:.0f}" cy="{cy - 5}" r="6" fill="{fill}"/>')
        o.append(f'  <text x="{cx + 20:.0f}" y="{cy}" font-size="14" fill="{c["on"]}">{name}</text>')
        # fixed column keeps the percentages aligned whatever the name length
        o.append(f'  <text x="{cx + 124:.0f}" y="{cy}" font-size="13" '
                 f'font-weight="700" fill="{fill}">{share * 100:.1f}%</text>')
    o.append("</svg>")
    return "\n".join(o) + "\n"


repos, tot = collect()
total = sum(tot.values())
top = tot.most_common(5)
rows = [(n, v / total) for n, v in top]
print(f"{len(repos)} repos, {total:,} bytes")
for n, s in rows:
    print(f"  {n:12} {s * 100:5.1f}%")
for name, c in SCHEMES.items():
    open(f"{OUT}/langs-{name}.svg", "w", encoding="utf-8").write(card(c, rows, total, len(repos)))
print("langs cards written")
