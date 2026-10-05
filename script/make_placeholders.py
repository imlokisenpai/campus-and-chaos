#!/usr/bin/env python3
"""
Generates warm, film-toned SVG placeholder "photos" for the
Campus & Chaos yearbook.

These exist so a fresh clone of the repo looks like a real, finished
yearbook instead of a grid of broken images. When friends upload real
photos into assets/memories/, these quietly stop being referenced.

Run:  python3 script/make_placeholders.py
"""

import os
import random

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "assets", "memories")

W, H = 900, 1125

# Warm film palette — dusty, faded, slightly overexposed
SKY_TOP = ["#e8b98a", "#d99a72", "#c9836a", "#e6c79b", "#cf9a78"]
SKY_BOT = ["#f2ddbe", "#f0d5b0", "#e9c9a4", "#f5e4c8", "#ecd0aa"]
GROUND = ["#8a7355", "#7b6549", "#94795a", "#6f5c44", "#8f7857"]
HAZE = "#f6e6c8"
INK = "#4a3a28"


def grain(op=0.11):
    return (
        '<filter id="g" x="0" y="0">'
        '<feTurbulence type="fractalNoise" baseFrequency="0.9" numOctaves="4" stitchTiles="stitch"/>'
        f'<feColorMatrix type="saturate" values="0"/><feComponentTransfer><feFuncA type="linear" slope="{op}"/></feComponentTransfer>'
        '</filter>'
    )


def grain_rect(h, w, op=0.11):
    return f'<rect width="{w}" height="{h}" filter="url(#g)" opacity="{op}"/>'


def sky(i, w, h):
    top = SKY_TOP[i % len(SKY_TOP)]
    bot = SKY_BOT[i % len(SKY_BOT)]
    return f'<rect width="{w}" height="{h}" fill="url(#sky{i%5})"/>', (
        f'<linearGradient id="sky{i%5}" x1="0" y1="0" x2="0" y2="1">'
        f'<stop offset="0" stop-color="{top}"/><stop offset="0.62" stop-color="{bot}"/>'
        f'<stop offset="1" stop-color="{HAZE}"/></linearGradient>'
    )


def sun(cx, cy, r, color="#fdf0cf", op=0.85):
    return f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{color}" opacity="{op}"/>'


def hill(y, w, h, color, bumps=7, seed=1):
    rnd = random.Random(seed)
    pts = [f"M0 {h} L0 {y}"]
    step = w / bumps
    for i in range(bumps):
        x = i * step
        cy = y + rnd.uniform(-26, 26)
        cx = x + step / 2
        nx = x + step
        pts.append(f"Q {cx:.0f} {cy:.0f} {nx:.0f} {y + rnd.uniform(-16, 16):.0f}")
    pts.append(f"L{w} {h} Z")
    return f'<path d="{" ".join(pts)}" fill="{color}"/>'


def building(x, y, w, h, color, windows=True, seed=3):
    rnd = random.Random(seed)
    out = [f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{color}"/>']
    if not windows:
        return "".join(out)
    cols = max(2, int(w // 46))
    rows = max(2, int(h // 52))
    gx = w / cols
    gy = h / rows
    for r in range(rows):
        for c in range(cols):
            if rnd.random() < 0.42:
                continue
            wx = x + gx * c + gx * 0.26
            wy = y + gy * r + gy * 0.24
            ww = gx * 0.46
            wh = gy * 0.44
            fill = "#f3dcae" if rnd.random() < 0.7 else "#e0bd80"
            out.append(f'<rect x="{wx:.0f}" y="{wy:.0f}" width="{ww:.0f}" height="{wh:.0f}" fill="{fill}" opacity="0.62"/>')
    return "".join(out)


def tree(x, base_y, hgt, color, seed=5):
    rnd = random.Random(seed)
    out = [f'<rect x="{x - 4:.0f}" y="{base_y - hgt * 0.42:.0f}" width="8" height="{hgt * 0.45:.0f}" fill="{INK}" opacity="0.75"/>']
    for _ in range(5):
        cx = x + rnd.uniform(-hgt * 0.24, hgt * 0.24)
        cy = base_y - hgt * rnd.uniform(0.45, 0.95)
        r = rnd.uniform(hgt * 0.14, hgt * 0.26)
        out.append(f'<circle cx="{cx:.0f}" cy="{cy:.0f}" r="{r:.0f}" fill="{color}" opacity="0.9"/>')
    return "".join(out)


def person(x, base_y, hgt, color, seed=7):
    """Simple standing silhouette."""
    hd = hgt * 0.17
    bw = hgt * 0.26
    return (
        f'<g fill="{color}" opacity="0.92">'
        f'<circle cx="{x:.0f}" cy="{base_y - hgt + hd * 0.6:.0f}" r="{hd * 0.6:.0f}"/>'
        f'<path d="M{x - bw/2:.0f} {base_y:.0f} L{x - bw/2 + bw*0.12:.0f} {base_y - hgt + hd*1.1:.0f} '
        f'L{x + bw/2 - bw*0.12:.0f} {base_y - hgt + hd*1.1:.0f} L{x + bw/2:.0f} {base_y:.0f} Z"/>'
        f'</g>'
    )


def crowd(base_y, count, spread, hgt, color, seed=11):
    rnd = random.Random(seed)
    out = []
    for _ in range(count):
        x = rnd.uniform(spread[0], spread[1])
        h = hgt * rnd.uniform(0.88, 1.08)
        out.append(person(x, base_y, h, color, seed=rnd.randint(1, 999)))
    return "".join(out)


def lightleak(w, h):
    return (
        f'<radialGradient id="leak" cx="0.06" cy="0.02" r="0.72">'
        f'<stop offset="0" stop-color="#ffb054" stop-opacity="0.30"/>'
        f'<stop offset="1" stop-color="#ffb054" stop-opacity="0"/></radialGradient>'
        f'<rect width="{w}" height="{h}" fill="url(#leak)"/>'
    )


def svg(name, body, defs):
    doc = (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" '
        f'width="{W}" height="{H}" role="img" aria-label="Placeholder memory photo">'
        f"<defs>{grain()}{''.join(defs)}</defs>{body}"
        f'{grain_rect(H, W, 0.13)}{lightleak(W, H)}</svg>'
    )
    with open(os.path.join(OUT, name), "w", encoding="utf-8") as f:
        f.write(doc)
    print("  wrote", name)


# ── Scenes ──────────────────────────────────────────────────────────

def scene_quad(i):
    """Golden hour over the quad, college buildings behind."""
    g, gd = sky(i, W, H)
    g += sun(660, 430, 128)
    g += building(40, 560, 300, 300, "#6d5741", seed=i)
    g += building(360, 505, 240, 355, "#5f4b38", seed=i + 4)
    g += building(640, 585, 220, 275, "#75604a", seed=i + 9)
    g += f'<rect width="{W}" height="{H}" fill="{HAZE}" opacity="0.16"/>'
    g += hill(880, W, H, "#7d6647", bumps=5, seed=i)
    g += tree(120, 905, 300, "#5f4d36", seed=i)
    g += tree(760, 930, 250, "#6a5740", seed=i + 3)
    g += crowd(1010, 7, (170, 740), 250, INK, seed=i)
    return g, [gd]


def scene_hostel(i):
    """Corridor / room interior, warm lamplight, a window."""
    g = f'<rect width="{W}" height="{H}" fill="#4e3d2c"/>'
    g += f'<rect width="{W}" height="{H}" fill="url(#wall{i%5})"/>'
    gd = (
        f'<linearGradient id="wall{i%5}" x1="0" y1="0" x2="0.4" y2="1">'
        f'<stop offset="0" stop-color="#a4825c"/>'
        f'<stop offset="0.55" stop-color="#7d6042"/>'
        f'<stop offset="1" stop-color="#4a3a28"/></linearGradient>'
        '<radialGradient id="lamp" cx="0.78" cy="0.24" r="0.5">'
        '<stop offset="0" stop-color="#ffe0a8" stop-opacity="0.95"/>'
        '<stop offset="1" stop-color="#ffe0a8" stop-opacity="0"/></radialGradient>'
        f'<linearGradient id="win{i%5}" x1="0" y1="0" x2="0" y2="1">'
        f'<stop offset="0" stop-color="#f7e6c4"/><stop offset="1" stop-color="#e3c191"/></linearGradient>'
    )
    g += f'<rect x="96" y="120" width="330" height="430" fill="url(#win{i%5})" opacity="0.9"/>'
    for k in range(1, 3):
        g += f'<rect x="{96 + 110 * k}" y="120" width="9" height="430" fill="#4a3a28" opacity="0.75"/>'
    g += f'<rect x="96" y="360" width="330" height="9" fill="#4a3a28" opacity="0.75"/>'
    g += f'<rect width="{W}" height="{H}" fill="url(#lamp)"/>'
    g += f'<rect y="880" width="{W}" height="{H - 880}" fill="#3a2d20"/>'
    g += f'<rect x="520" y="700" width="300" height="200" fill="#5b462f" opacity="0.9"/>'
    g += f'<circle cx="700" cy="250" r="70" fill="#ffe6b4" opacity="0.55"/>'
    g += person(300, 1080, 420, "#332619", seed=i)
    return g, [gd]


def scene_trip(i):
    """Day trip — hills, sky, a distant road."""
    g, gd = sky(i + 1, W, H)
    g += sun(250, 380, 96, color="#fbeec9")
    g += hill(620, W, H, "#8a7455", bumps=4, seed=i)
    g += hill(740, W, H, "#6d5b41", bumps=6, seed=i + 2)
    g += hill(880, W, H, "#514232", bumps=8, seed=i + 5)
    g += f'<path d="M380 {H} L430 890 L470 890 L640 {H} Z" fill="#b9a17c" opacity="0.85"/>'
    g += tree(180, 900, 210, "#4e4030", seed=i + 7)
    g += tree(760, 930, 190, "#4a3d2e", seed=i + 8)
    g += person(452, 905, 130, "#3d3025", seed=i)
    return g, [gd]


def scene_canteen(i):
    """Night canteen — dark, warm lamp pools, steam."""
    g = f'<rect width="{W}" height="{H}" fill="#3b2e21"/>'
    gd = (
        f'<radialGradient id="pool{i%5}" cx="0.34" cy="0.46" r="0.42">'
        f'<stop offset="0" stop-color="#ffcf85" stop-opacity="0.92"/>'
        f'<stop offset="1" stop-color="#ffcf85" stop-opacity="0"/></radialGradient>'
        f'<radialGradient id="pool2" cx="0.78" cy="0.38" r="0.38">'
        f'<stop offset="0" stop-color="#ffb765" stop-opacity="0.8"/>'
        f'<stop offset="1" stop-color="#ffb765" stop-opacity="0"/></radialGradient>'
    )
    g += f'<rect width="{W}" height="{H}" fill="url(#pool{i%5})"/>'
    g += f'<rect width="{W}" height="{H}" fill="url(#pool2)"/>'
    g += f'<rect y="720" width="{W}" height="{H-720}" fill="#2b2119"/>'
    g += f'<rect x="80" y="700" width="740" height="26" fill="#4d3b2a"/>'
    for k, cx in enumerate((180, 400, 660)):
        g += f'<circle cx="{cx}" cy="{660 - k * 12}" r="{16 - k * 3}" fill="#f2dfba" opacity="0.5"/>'
    g += crowd(700, 4, (140, 780), 300, "#2a1f16", seed=i + 3)
    return g, [gd]


def scene_library(i):
    """Stacked books, a desk lamp, papers."""
    g = f'<rect width="{W}" height="{H}" fill="#6b543a"/>'
    gd = (
        f'<linearGradient id="desk{i%5}" x1="0" y1="0" x2="0" y2="1">'
        f'<stop offset="0" stop-color="#8a6c47"/><stop offset="1" stop-color="#5d4a32"/></linearGradient>'
        '<radialGradient id="dl" cx="0.68" cy="0.3" r="0.44">'
        '<stop offset="0" stop-color="#ffe1ad" stop-opacity="0.9"/>'
        '<stop offset="1" stop-color="#ffe1ad" stop-opacity="0"/></radialGradient>'
    )
    g += f'<rect y="420" width="{W}" height="{H-420}" fill="url(#desk{i%5})"/>'
    g += f'<rect width="{W}" height="{H}" fill="url(#dl)"/>'
    cols = ["#8f4a3a", "#5f6d48", "#a97b3c", "#4a5a70", "#7a4a62", "#5c5140"]
    rnd = random.Random(i)
    bx, by = 110, 420
    for k in range(11):
        bw = rnd.randint(26, 44)
        bh = rnd.randint(54, 92)
        c = cols[k % len(cols)]
        g += f'<rect x="{bx}" y="{by - bh}" width="{bw}" height="{bh}" fill="{c}" opacity="0.92"/>'
        g += f'<rect x="{bx}" y="{by - bh + bh*0.14:.0f}" width="{bw}" height="5" fill="#f2e2c2" opacity="0.55"/>'
        bx += bw + 2
        if bx > 470:
            by -= 96
            bx = 120
    g += f'<rect x="560" y="700" width="300" height="200" fill="#efe6d2" transform="rotate(-4 710 800)" opacity="0.9"/>'
    for k in range(6):
        g += f'<rect x="586" y="{730 + k * 28}" width="{210 - k * 22}" height="5" fill="#8d7c60" opacity="0.5" transform="rotate(-4 710 800)"/>'
    g += f'<circle cx="640" cy="330" r="66" fill="#ffe8bc" opacity="0.75"/>'
    return g, [gd]


def scene_road(i):
    """Night highway, headlights, chai stop energy."""
    g = f'<rect width="{W}" height="{H}" fill="#2a2c33"/>'
    gd = (
        f'<linearGradient id="sky{i%5}" x1="0" y1="0" x2="0" y2="1">'
        f'<stop offset="0" stop-color="#2f323c"/><stop offset="1" stop-color="#8a6a4c"/></linearGradient>'
        '<radialGradient id="head" cx="0.5" cy="0.55" r="0.34">'
        '<stop offset="0" stop-color="#fff3d2" stop-opacity="0.95"/>'
        '<stop offset="1" stop-color="#fff3d2" stop-opacity="0"/></radialGradient>'
    )
    g += f'<rect width="{W}" height="120" fill="url(#sky{i%5})"/>'
    g += f'<rect width="{W}" height="{H}" fill="url(#head)"/>'
    g += f'<path d="M0 {H} L330 620 L570 620 L900 {H} Z" fill="#3c3a38"/>'
    g += f'<rect x="436" y="640" width="28" height="180" fill="#efe3c4" opacity="0.5"/>'
    g += f'<rect x="440" y="880" width="20" height="120" fill="#efe3c4" opacity="0.35"/>'
    for k in range(7):
        x = 90 + k * 118
        g += f'<rect x="{x}" y="{430 + k * 12}" width="10" height="200" fill="#25262b"/>'
        g += f'<circle cx="{x + 5}" cy="{420 + k * 12}" r="7" fill="#ffd08a" opacity="0.8"/>'
    g += hill(690, W, H, "#20211f", bumps=5, seed=i)
    return g, [gd]


def scene_porch(i):
    """Sunset from a hostel balcony / window."""
    g, gd = sky(i + 2, W, H)
    g += sun(420, 520, 150, color="#fdeed0")
    g += f'<rect width="{W}" height="{H}" fill="{HAZE}" opacity="0.2"/>'
    g += building(560, 470, 340, 420, "#5c4936", seed=i + 2)
    g += tree(150, 1085, 420, "#4f4231", seed=i)
    g += tree(330, 1105, 350, "#5b4c38", seed=i + 6)
    g += f'<rect x="0" y="1085" width="{W}" height="18" fill="#3f3427" opacity="0.9"/>'
    for k in range(7):
        x = 40 + k * 130
        g += f'<rect x="{x}" y="{1010 - (k % 3) * 26}" width="9" height="90" fill="#3f3427" opacity="0.75"/>'
    return g, [gd]


def scene_walk(i):
    """Campus path at dusk, lamps just on."""
    g, gd = sky(i + 3, W, H)
    g += f'<rect width="{W}" height="{H}" fill="#7a6244" opacity="0.14"/>'
    g += building(60, 520, 280, 340, "#5b4835", seed=i)
    g += building(620, 490, 250, 370, "#66513b", seed=i + 3)
    g += hill(880, W, H, "#6b5a41", bumps=6, seed=i)
    g += f'<path d="M300 {H} L420 880 L520 880 L660 {H} Z" fill="#a89170" opacity="0.8"/>'
    for k, lx in enumerate((330, 470, 640)):
        g += f'<rect x="{lx}" y="{770 - k * 20}" width="9" height="{130 + k * 20}" fill="#3b3226"/>'
        g += f'<circle cx="{lx + 4}" cy="{762 - k * 20}" r="15" fill="#ffd894" opacity="0.9"/>'
        g += f'<circle cx="{lx + 4}" cy="{762 - k * 20}" r="46" fill="#ffd894" opacity="0.16"/>'
    g += crowd(1090, 5, (250, 700), 250, "#3d3225", seed=i + 1)
    return g, [gd]


SCENES = [
    ("quad-2019.svg", scene_quad),
    ("hostel-night.svg", scene_hostel),
    ("hill-trip.svg", scene_trip),
    ("canteen.svg", scene_canteen),
    ("library-stack.svg", scene_library),
    ("road-trip.svg", scene_road),
    ("balcony-sunset.svg", scene_porch),
    ("campus-walk.svg", scene_walk),
    ("quad-2021.svg", scene_quad),
    ("field-day.svg", scene_walk),
    ("farewell.svg", scene_porch),
    ("reunion.svg", scene_canteen),
]


def main():
    os.makedirs(OUT, exist_ok=True)
    print(f"Generating {len(SCENES)} placeholders into {OUT}")
    for idx, (name, fn) in enumerate(SCENES):
        body, defs = fn(idx + 1)
        svg(name, body, defs)
    print("Done.")


if __name__ == "__main__":
    main()