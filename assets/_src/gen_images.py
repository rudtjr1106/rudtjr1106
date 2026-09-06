# -*- coding: utf-8 -*-
"""Builds the raster assets: adaptive-icon squircles and device-framed screenshots."""
from PIL import Image, ImageDraw, ImageFilter

SRC = "/Users/seok/Downloads/이력서/조경석_지원서/assets"
OUT = "/Users/seok/StudioProjects/rudtjr1106/assets"
SS = 4  # supersample factor for smooth edges


def squircle_mask(size, n=4.0):
    """Android's adaptive-icon mask is a superellipse, not a rounded rect."""
    d = size * SS
    m = Image.new("L", (d, d), 0)
    px = m.load()
    r = d / 2.0
    for y in range(d):
        ny = (y + 0.5 - r) / r
        ay = abs(ny) ** n
        if ay > 1:
            continue
        # |x|^n + |y|^n = 1  ->  solve for the row's half-width
        half = (1.0 - ay) ** (1.0 / n) * r
        x0, x1 = int(r - half), int(r + half)
        for x in range(max(0, x0), min(d, x1 + 1)):
            px[x, y] = 255
    return m.resize((size, size), Image.LANCZOS)


def icon(name, size=240, pad=18):
    src = Image.open(f"{SRC}/icon_{name}.png").convert("RGBA")
    inner = size - pad * 2
    src = src.resize((inner, inner), Image.LANCZOS)
    mask = squircle_mask(inner)

    canvas = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    # soft contact shadow so the tile sits on the page like a launcher icon
    shadow = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    shadow.paste((0, 0, 0, 70), (pad, pad + 6), mask)
    canvas = Image.alpha_composite(canvas, shadow.filter(ImageFilter.GaussianBlur(7)))

    tile = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    tile.paste(src, (pad, pad), mask)
    canvas = Image.alpha_composite(canvas, tile)

    # white-ground icons would otherwise dissolve into a light surface
    ring = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    ring.paste((0, 0, 0, 38), (pad, pad), mask)
    hole = Image.new("L", (size, size), 0)
    hole.paste(squircle_mask(inner - 3), (pad + 2, pad + 2))
    ring.putalpha(Image.composite(Image.new("L", (size, size), 0), ring.getchannel("A"), hole))
    canvas = Image.alpha_composite(canvas, ring)
    canvas.save(f"{OUT}/icon-{name}.png")
    return canvas.size


def cover(img, w, h):
    sw, sh = img.size
    scale = max(w / sw, h / sh)
    img = img.resize((round(sw * scale), round(sh * scale)), Image.LANCZOS)
    x = (img.width - w) // 2
    return img.crop((x, 0, x + w, h))


def phone(src_name, label, w=300, h=650, bezel=9, radius=36):
    shot = cover(Image.open(f"{SRC}/{src_name}").convert("RGB"), w, h)

    fw, fh = w + bezel * 2, h + bezel * 2
    frame = Image.new("RGBA", (fw * SS, fh * SS), (0, 0, 0, 0))
    d = ImageDraw.Draw(frame)
    d.rounded_rectangle([0, 0, fw * SS - 1, fh * SS - 1], radius=radius * SS, fill=(20, 22, 26, 255))
    frame = frame.resize((fw, fh), Image.LANCZOS)

    inner = Image.new("L", ((w) * SS, (h) * SS), 0)
    ImageDraw.Draw(inner).rounded_rectangle(
        [0, 0, w * SS - 1, h * SS - 1], radius=(radius - bezel) * SS, fill=255)
    inner = inner.resize((w, h), Image.LANCZOS)

    frame.paste(shot, (bezel, bezel), inner)
    # front camera
    ImageDraw.Draw(frame).ellipse(
        [fw // 2 - 4, bezel + 6, fw // 2 + 4, bezel + 14], fill=(38, 41, 46, 255))
    return frame


for n in ("pinup", "umc", "hugg", "damoim", "plub"):
    icon(n)
print("icons done")

SHOTS = [("pinup_map.png", "핀업 지도"), ("damoim_home.png", "다모임 홈"),
         ("hugg_home.png", "허그 홈"), ("pinup_article.png", "핀업 아티클")]
FRAMES = [phone(f, n) for f, n in SHOTS]
print("frames done")


def strip(frames, cols, out_name, tile_w=200, gap=24):
    """One image instead of N, so the row scales as a unit rather than reflowing
    into a very tall column on a phone."""
    tiles = [im.resize((tile_w, round(im.height * tile_w / im.width)), Image.LANCZOS)
             for im in frames]
    th = tiles[0].height
    rows = (len(tiles) + cols - 1) // cols
    W = cols * tile_w + (cols - 1) * gap
    H = rows * th + (rows - 1) * gap
    canvas = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    for i, t in enumerate(tiles):
        canvas.alpha_composite(t, ((i % cols) * (tile_w + gap), (i // cols) * (th + gap)))
    canvas.save(f"{OUT}/{out_name}.png")
    return canvas.size


print("wide  ", strip(FRAMES, 4, "screens-wide"))
print("narrow", strip(FRAMES, 2, "screens-narrow"))


def rounded(src_path, out_name, radius=20, max_w=620):
    """Rounds a plain screenshot so it sits with the M3 cards."""
    im = Image.open(src_path).convert("RGBA")
    if im.width > max_w:
        im = im.resize((max_w, round(im.height * max_w / im.width)), Image.LANCZOS)
    m = Image.new("L", (im.width * SS, im.height * SS), 0)
    ImageDraw.Draw(m).rounded_rectangle([0, 0, im.width * SS - 1, im.height * SS - 1],
                                        radius=radius * SS, fill=255)
    im.putalpha(m.resize(im.size, Image.LANCZOS))
    # a photo screenshot is the heaviest asset here; palette it down hard
    flat = im.convert("RGB").quantize(colors=192, method=Image.MEDIANCUT, dither=Image.FLOYDSTEINBERG)
    flat = flat.convert("RGBA")
    flat.putalpha(im.getchannel("A"))
    flat.save(f"{OUT}/{out_name}.png", optimize=True)
    return im.size


print("poket ", rounded("/Users/seok/StudioProjects/poketdesktop/docs/images/mac-desktop.png",
                        "poket-desktop"))
