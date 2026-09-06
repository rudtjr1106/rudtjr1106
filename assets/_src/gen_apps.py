# -*- coding: utf-8 -*-
"""The app row, laid out like an Android launcher: adaptive-icon tiles with labels
on an M3 surface, wallpapered with the same shape family as the hero."""
import math
from PIL import Image, ImageDraw, ImageFont

OUT = "/Users/seok/StudioProjects/rudtjr1106/assets"
FONT = "/System/Library/Fonts/AppleSDGothicNeo.ttc"
SS = 2

APPS = [
    ("pinup",  "핀업",   "Play Store 운영 중"),
    ("umc",    "UMC",    "약 1,000명 사용"),
    ("hugg",   "허그",   "크래시 0건"),
    ("damoim", "다모임", "클라이언트 + 서버"),
    ("plub",   "PLUB",   "14인 협업"),
]

SCHEMES = {
    "light": dict(surface=(233, 243, 235), on=(13, 32, 21), var=(69, 97, 80),
                  deco=(203, 227, 211), deco2=(224, 214, 245)),
    "dark":  dict(surface=(15, 35, 24), on=(220, 233, 223), var=(166, 195, 174),
                  deco=(29, 61, 42), deco2=(58, 45, 92)),
}


def polar_pts(cx, cy, R, lobes, amp, steps=200):
    return [(cx + R * (1 + amp * math.cos(lobes * (2 * math.pi * i / steps))) * math.cos(2 * math.pi * i / steps),
             cy + R * (1 + amp * math.cos(lobes * (2 * math.pi * i / steps))) * math.sin(2 * math.pi * i / steps))
            for i in range(steps)]


def build(scheme_name, c):
    W, H = 880, 232
    img = Image.new("RGBA", (W * SS, H * SS), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    d.rounded_rectangle([0, 0, W * SS - 1, H * SS - 1], radius=28 * SS, fill=c["surface"] + (255,))

    f_name = ImageFont.truetype(FONT, 17 * SS, index=6)   # Bold
    f_sub = ImageFont.truetype(FONT, 12.5 * SS, index=2)  # Medium

    col = W / len(APPS)
    for i, (key, name, sub) in enumerate(APPS):
        cx = col * (i + 0.5)
        icon = Image.open(f"{OUT}/icon-{key}.png").convert("RGBA").resize((104 * SS, 104 * SS), Image.LANCZOS)
        img.alpha_composite(icon, (int(cx * SS - 52 * SS), int(28 * SS)))
        for text, font, y, fill in ((name, f_name, 148, c["on"]), (sub, f_sub, 174, c["var"])):
            w = d.textlength(text, font=font)
            d.text((cx * SS - w / 2, y * SS), text, font=font, fill=fill + (255,))

    img.resize((W, H), Image.LANCZOS).save(f"{OUT}/apps-{scheme_name}.png")


for n, c in SCHEMES.items():
    build(n, c)
print("apps panels written")
