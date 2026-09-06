# -*- coding: utf-8 -*-
"""포스크탑이 쓰는 걷는 도트를 README 띠로 만든다.

시트는 PMDCollab/SpriteCollab (CC BY-NC 4.0). 가로=프레임, 세로=8방향이고
rowmap 의 'right' 행만 잘라 쓴다. 프레임 지속시간은 앱과 같은 규칙으로
1틱 = 1/60초 로 환산한다(client/poketdesktop/sprites.py).

원본 시트는 포스크탑 캐시에서 읽는다. 다른 종으로 바꾸려면 WALKERS 를 고치고
포스크탑을 한 번 돌려 해당 종을 캐시에 받아두면 된다.
"""
import base64
import io
import json
import os

from PIL import Image

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
CACHE = os.path.expanduser("~/Library/Application Support/poketdesktop/walk")

# (도감번호, 이름, 걷는 속도(초/한 바퀴), 시작 지연)
WALKERS = [
    ("0001", "이상해씨", 19, 0.0),
    ("0004", "파이리",   15, 3.4),
    ("0104", "탕구리",   24, 7.2),
    ("0116", "쏘드라",   17, 11.0),
    ("0403", "꼬링크",   21, 14.6),
]
SCALE, GROUND, W, H = 1.5, 74, 880, 88
GRASS = "#2E9E63"


def load(num):
    flat_png, flat_json = os.path.join(CACHE, num + ".png"), os.path.join(CACHE, num + ".json")
    if os.path.exists(flat_png):
        return Image.open(flat_png).convert("RGBA"), json.load(open(flat_json))
    d = os.path.join(CACHE, num)
    return (Image.open(os.path.join(d, "Walk.png")).convert("RGBA"),
            json.load(open(os.path.join(d, "Walk.json"))))


def right_strip(num):
    sheet, meta = load(num)
    fw, fh = meta["frameW"], meta["frameH"]
    row = meta["rowmap"]["right"]
    n = meta["frames"]
    strip = sheet.crop((0, row * fh, n * fw, row * fh + fh))
    # PMD 프레임은 위아래로 여백이 있다. 세로만 잘라내 발이 지면에 닿게 한다.
    # 가로는 건드리면 프레임 격자가 깨지므로 그대로 둔다.
    box = strip.getbbox()
    if box:
        strip = strip.crop((0, box[1], n * fw, box[3]))
        fh = box[3] - box[1]
    buf = io.BytesIO()
    strip.save(buf, format="PNG", optimize=True)
    return base64.b64encode(buf.getvalue()).decode(), fw, fh, n, meta["durations"]


def frame_anim(fw, n, durations):
    ticks = list(durations)[:n] or [8] * n
    total = sum(ticks)
    keys, vals, acc = ["0"], ["0"], 0
    for i, t in enumerate(ticks):
        acc += t
        keys.append(f"{acc / total:.5g}")
        vals.append(f"{-fw * ((i + 1) % n)}")
    return ";".join(keys), ";".join(vals), total / 60.0


def grass(x, y, px=4):
    blades = ["..d..d..", ".ddd.dd.", ".d.d.d.d"]
    return "".join(
        f'<rect x="{x + gx * px}" y="{y + gy * px}" width="{px}" height="{px}" fill="{GRASS}"/>'
        for gy, row in enumerate(blades) for gx, c in enumerate(row) if c == "d")


def build():
    o = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" '
         f'role="img" shape-rendering="crispEdges">',
         '<!-- 걷는 도트: PMDCollab/SpriteCollab, CC BY-NC 4.0. 포켓몬은 닌텐도/Game Freak/'
         '포켓몬 컴퍼니 저작물. 비상업 팬 프로젝트. -->',
         '<style>.still{display:none}'
         '@media (prefers-reduced-motion: reduce){.walk{display:none}.still{display:block}}</style>']

    for gx in (56, 204, 352, 500, 648, 796):
        o.append(f'<g opacity=".55">{grass(gx, GROUND - 8)}</g>')

    o.append('<g class="walk">')
    for i, (num, name, dur, delay) in enumerate(WALKERS):
        b64, fw, fh, n, durations = right_strip(num)
        keys, vals, cycle = frame_anim(fw, n, durations)
        y = GROUND - fh * SCALE
        o.append(f'  <clipPath id="w{i}"><rect width="{fw}" height="{fh}"/></clipPath>')
        o.append(f'  <g transform="translate(-90,{y:.1f})">')
        o.append(f'    <animateTransform attributeName="transform" type="translate" '
                 f'from="-90 {y:.1f}" to="{W + 70} {y:.1f}" dur="{dur}s" begin="-{delay}s" '
                 f'repeatCount="indefinite"/>')
        o.append(f'    <g transform="scale({SCALE})" clip-path="url(#w{i})">')
        o.append(f'      <image href="data:image/png;base64,{b64}" x="0" y="0" '
                 f'width="{fw * n}" height="{fh}" image-rendering="pixelated">'
                 f'<animate attributeName="x" values="{vals}" keyTimes="{keys}" '
                 f'calcMode="discrete" dur="{cycle:.3f}s" repeatCount="indefinite"/></image>')
        o.append('    </g>')
        o.append(f'    <title>{name}</title>')
        o.append('  </g>')
    o.append('</g>')

    o.append('<g class="still">')
    for i, (num, name, _, _) in enumerate(WALKERS):
        b64, fw, fh, n, _d = right_strip(num)
        y = GROUND - fh * SCALE
        o.append(f'  <clipPath id="s{i}"><rect width="{fw}" height="{fh}"/></clipPath>')
        o.append(f'  <g transform="translate({90 + i * 160},{y:.1f}) scale({SCALE})" '
                 f'clip-path="url(#s{i})">'
                 f'<image href="data:image/png;base64,{b64}" width="{fw * n}" height="{fh}" '
                 f'image-rendering="pixelated"/></g>')
    o.append('</g>')

    o.append('</svg>')
    return "\n".join(o) + "\n"


open(os.path.join(OUT, "walkers.svg"), "w", encoding="utf-8").write(build())
print("walkers.svg written", os.path.getsize(os.path.join(OUT, "walkers.svg")) // 1024, "KB")
