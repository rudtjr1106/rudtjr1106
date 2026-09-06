# -*- coding: utf-8 -*-
"""Material 3 Expressive hero banner. The shapes are the real M3 shape family,
generated as polar curves rather than pasted clip art."""
import math

OUT = "/Users/seok/StudioProjects/rudtjr1106/assets"

MONO = "ui-monospace, SFMono-Regular, Menlo, Consolas, DejaVu Sans Mono, monospace"
KR = "'Apple SD Gothic Neo','Pretendard','Noto Sans KR','Malgun Gothic',system-ui,sans-serif"

# expressive scheme: android green primary, violet tertiary, amber secondary
SURFACE   = "#06291A"
GREEN     = "#3DDC84"
GREEN_DIM = "#0E4A30"
VIOLET    = "#C9A6FF"
AMBER     = "#FFC24B"
ON_SURF   = "#EAFBF0"
ON_MUTED  = "#8FBFA6"


def polar(cx, cy, R, lobes, amp, phase=0.0, steps=280):
    """r(θ) = R(1 + amp·cos(lobes·θ)) — M3's cookie / clover / sunny family."""
    pts = []
    for i in range(steps):
        t = 2 * math.pi * i / steps
        r = R * (1 + amp * math.cos(lobes * t + phase))
        pts.append(f"{cx + r * math.cos(t):.1f} {cy + r * math.sin(t):.1f}")
    return "M" + "L".join(pts) + "Z"


def squircle(cx, cy, R, n=4.0, steps=240):
    """Android's adaptive-icon mask as a path, so the banner rhymes with the app tiles."""
    pts = []
    for i in range(steps):
        t = 2 * math.pi * i / steps
        c, s_ = math.cos(t), math.sin(t)
        r = R / (abs(c) ** n + abs(s_) ** n) ** (1.0 / n)
        pts.append(f"{cx + r * c:.1f} {cy + r * s_:.1f}")
    return "M" + "L".join(pts) + "Z"


def chip_width(text, fs):
    """Korean glyphs are roughly full-width, latin roughly 0.56em. Pad generously so a
    different system font can be wider without breaking out of the pill."""
    w = 0.0
    for ch in text:
        w += fs * (0.98 if ord(ch) > 0x1100 else 0.56)
    return w + fs * 2.6


# --- typed code line -------------------------------------------------------
PHRASES = [
    "val stack = Kotlin + Compose + KMP",
    "while (true) { measure(); improve() }",
    "ship(android); ship(ios); ship(server)",
]
CH = 9.0          # monospace advance at 15px
T_CHAR, T_HOLD, T_DEL = 0.055, 1.7, 0.028


def seq(points):
    """(keyTime, value) pairs -> SMIL keyTimes/values, merging duplicate times."""
    out = []
    for k, v in points:
        k = round(min(max(k, 0.0), 1.0), 5)
        if out and abs(out[-1][0] - k) < 1e-9:
            out[-1] = (k, v)
        else:
            out.append((k, v))
    return (";".join(f"{k:g}" for k, _ in out),
            ";".join(f"{v:g}" for _, v in out))


def typing(x, baseline):
    """Character-stepped typing built from SMIL keyframes. Monospace keeps the
    cursor exactly on the last glyph whatever font the viewer resolves."""
    spans, t = [], 0.0
    for ph in PHRASES:
        n = len(ph)
        type_end = t + n * T_CHAR
        hold_end = type_end + T_HOLD
        spans.append((t, type_end, hold_end, hold_end + n * T_DEL, n))
        t = spans[-1][3]
    total = t

    o = []
    for i, (span, ph) in enumerate(zip(spans, PHRASES)):
        s0, s1, s2, s3, n = span

        chars = [(s0, 0)]
        chars += [(s0 + c * T_CHAR, c) for c in range(n + 1)]
        chars += [(s1, n), (s2, n)]
        chars += [(s2 + (n - c) * T_DEL, c) for c in range(n, -1, -1)]
        chars += [(s3, 0)]
        pts = [(0.0, 0)] + [(tt / total, c) for tt, c in chars] + [(1.0, 0)]

        kt, widths = seq([(k, c * CH) for k, c in pts])
        _, cursor = seq([(k, x + c * CH) for k, c in pts])
        vis_k, vis_v = seq([(0.0, 0), (s0 / total, 1), (s3 / total, 0), (1.0, 0)])

        o.append('  <g opacity="0">')
        o.append(f'    <animate attributeName="opacity" dur="{total:g}s" repeatCount="indefinite" '
                 f'calcMode="discrete" values="{vis_v}" keyTimes="{vis_k}"/>')
        o.append(f'    <clipPath id="t{i}"><rect x="{x}" y="{baseline - 15}" width="0" height="23">'
                 f'<animate attributeName="width" dur="{total:g}s" repeatCount="indefinite" '
                 f'calcMode="discrete" values="{widths}" keyTimes="{kt}"/></rect></clipPath>')
        o.append(f'    <text x="{x}" y="{baseline}" font-family="{MONO}" font-size="15" '
                 f'fill="{ON_MUTED}" clip-path="url(#t{i})">{ph}</text>')
        o.append(f'    <rect x="{x}" y="{baseline - 13}" width="8" height="18" fill="{AMBER}" rx="1">'
                 f'<animate attributeName="x" dur="{total:g}s" repeatCount="indefinite" '
                 f'calcMode="discrete" values="{cursor}" keyTimes="{kt}"/>'
                 f'<animate attributeName="opacity" values="1;0" keyTimes="0;0.5" dur="1s" '
                 f'calcMode="discrete" repeatCount="indefinite"/></rect>')
        o.append('  </g>')
    return o, total


def build():
    W, H, R = 880, 320, 32
    o = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" '
         f'viewBox="0 0 {W} {H}" role="img" font-family="{KR}">']
    o.append('<style>.still{display:none}'
             '@media (prefers-reduced-motion: reduce){.type{display:none}.still{display:block}}</style>')
    o.append(f'<clipPath id="c"><rect width="{W}" height="{H}" rx="{R}"/></clipPath>')
    o.append('<g clip-path="url(#c)">')
    o.append(f'  <rect width="{W}" height="{H}" fill="{SURFACE}"/>')

    # a giant adaptive-icon squircle anchors the cluster and echoes the app tiles below
    o.append(f'  <path d="{squircle(768, 160, 208)}" fill="{GREEN_DIM}"/>')

    # the M3 shape family, crisp and each fully readable
    o.append(f'  <path d="{polar(672, 112, 80, 12, 0.105)}" fill="{GREEN}"/>')
    o.append(f'  <path d="{polar(790, 202, 66, 4, 0.215, math.pi / 4)}" fill="{VIOLET}"/>')
    o.append(f'  <path d="{polar(652, 244, 44, 8, 0.155)}" fill="{AMBER}"/>')
    o.append(f'  <path d="{polar(802, 90, 36, 12, 0.16)}" fill="none" '
             f'stroke="{GREEN}" stroke-width="2.5" opacity=".75"/>')
    o.append(f'  <path d="{squircle(838, 262, 22)}" fill="{VIOLET}" opacity=".9"/>')

    # type
    o.append(f'  <text x="60" y="150" font-size="68" font-weight="700" fill="{ON_SURF}" '
             f'letter-spacing="-1.5">조경석</text>')
    o.append(f'  <text x="63" y="196" font-size="24" font-weight="600" fill="{GREEN}">'
             f'Android Engineer</text>')
    o.append('  <g class="type">')
    typed, _ = typing(63, 228)
    o += typed
    o.append('  </g>')
    o.append(f'  <text class="still" x="63" y="228" font-family="{MONO}" font-size="15" '
             f'fill="{ON_MUTED}">{PHRASES[-1]}</text>')

    x, fs = 60, 13.5
    for label, ink in (("Play Store 운영 중", GREEN), ("Android + iOS", VIOLET),
                       ("사용자 1,000+", AMBER)):
        w = chip_width(label, fs)
        o.append(f'  <rect x="{x:.0f}" y="256" width="{w:.0f}" height="34" rx="17" '
                 f'fill="none" stroke="{ink}" stroke-width="1.4" opacity=".8"/>')
        o.append(f'  <text x="{x + w / 2:.0f}" y="278" font-size="{fs}" fill="{ink}" '
                 f'text-anchor="middle">{label}</text>')
        x += w + 10
    o.append('</g></svg>')
    return "\n".join(o) + "\n"


open(f"{OUT}/hero.svg", "w", encoding="utf-8").write(build())
print("hero.svg written")
