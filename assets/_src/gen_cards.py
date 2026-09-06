# -*- coding: utf-8 -*-
"""M3 card: the tech-stack chip set, in a light and a dark Material 3 scheme."""
OUT = "/Users/seok/StudioProjects/rudtjr1106/assets"
KR = "'Apple SD Gothic Neo','Pretendard','Noto Sans KR','Malgun Gothic',system-ui,sans-serif"
MONO = "ui-monospace, SFMono-Regular, Menlo, Consolas, monospace"

SCHEMES = {
    "light": dict(surface="#E9F3EB", onSurface="#0D2015", onVar="#456150", outline="#BCD0C2",
                  primary="#00693C", track="#CBE3D3", tertiary="#6B4EA8", tertBg="#E9DDFF",
                  secondary="#7A5300", secBg="#FFDF9E", primBg="#8CF3B8"),
    "dark":  dict(surface="#0F2318", onSurface="#DCE9DF", onVar="#A6C3AE", outline="#38513F",
                  primary="#5CDD95", track="#1D3D2A", tertiary="#D2BBFF", tertBg="#4A3579",
                  secondary="#FFD489", secBg="#6B4E0F", primBg="#00532B"),
}

STACK = [
    ("언어",     "p", ["Kotlin", "Swift"]),
    ("UI",       "t", ["Jetpack Compose", "Compose Multiplatform", "XML View"]),
    ("아키텍처", "s", ["Clean Architecture", "MVVM / MVI", "Multi-Module"]),
    ("비동기·DI", "p", ["Coroutines", "Flow", "Hilt", "Koin"]),
    ("네트워크", "t", ["Retrofit", "OkHttp", "Ktor", "Ktorfit"]),
    ("온디바이스", "s", ["ML Kit GenAI", "DataStore", "Security Crypto"]),
    ("품질",     "p", ["Custom Lint", "Macrobenchmark", "R8"]),
    ("운영·서버", "t", ["Firebase FCM", "GitHub Actions", "Spring Boot", "PostgreSQL"]),
]


def text_w(text, fs):
    return sum(fs * (0.98 if ord(c) > 0x1100 else 0.56) for c in text)


def stack(c):
    W, ROW_H, PAD, LABEL_W = 880, 46, 26, 108
    H = PAD * 2 + ROW_H * len(STACK) - 8
    tone = {"p": (c["primBg"], c["primary"]), "t": (c["tertBg"], c["tertiary"]),
            "s": (c["secBg"], c["secondary"])}
    o = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" '
         f'role="img" font-family="{KR}">',
         f'  <rect width="{W}" height="{H}" rx="28" fill="{c["surface"]}"/>']
    for i, (cat, key, items) in enumerate(STACK):
        top = PAD + i * ROW_H
        bg, ink = tone[key]
        o.append(f'  <text x="{PAD}" y="{top + 22}" font-size="13" fill="{c["onVar"]}">{cat}</text>')
        x = PAD + LABEL_W
        for it in items:
            w = text_w(it, 13) + 30
            o.append(f'  <rect x="{x:.0f}" y="{top + 2}" width="{w:.0f}" height="30" rx="9" fill="{bg}"/>')
            o.append(f'  <text x="{x + w / 2:.0f}" y="{top + 22}" font-size="13" font-weight="600" '
                     f'fill="{ink}" text-anchor="middle">{it}</text>')
            x += w + 8
    o.append("</svg>")
    return "\n".join(o) + "\n"


for name, c in SCHEMES.items():
    open(f"{OUT}/stack-{name}.svg", "w", encoding="utf-8").write(stack(c))
print("cards written")
