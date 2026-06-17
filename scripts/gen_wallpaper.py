#!/usr/bin/env python3
"""
SenOS desktop wallpaper generator.

Produces an elegant lotus wallpaper (rose/plum gradient + soft glow + white
lotus + SenOS wordmark) and writes it to the real background files. Crucially
it writes default.png as a REAL PNG (it used to be a broken symlink -> black
desktop).

Run from repo root:  python scripts/gen_wallpaper.py   (requires Pillow)
"""
import math, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import gen_brand_assets as g
from PIL import Image, ImageDraw, ImageFilter

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

TOP = (31, 10, 24)     # deep plum
MID = (120, 18, 70)    # rose-plum
BOT = (200, 30, 96)    # rose


def vgrad3(w, h, c0, c1, c2):
    col = Image.new("RGB", (1, h))
    for y in range(h):
        t = y / max(1, h - 1)
        if t < 0.5:
            u = t / 0.5; a, b = c0, c1
        else:
            u = (t - 0.5) / 0.5; a, b = c1, c2
        col.putpixel((0, y), tuple(round(a[i] + (b[i] - a[i]) * u) for i in range(3)))
    return col.resize((w, h))


def radial_glow(diam, color, strength=150):
    """Soft circular glow as an RGBA tile."""
    t = 600
    m = Image.new("L", (t, t), 0)
    px = m.load()
    c = t / 2
    for y in range(t):
        for x in range(t):
            d = math.hypot(x - c, y - c) / c
            px[x, y] = max(0, int(strength * (1 - min(1, d)) ** 1.8))
    glow = Image.new("RGBA", (t, t), color + (0,))
    glow.putalpha(m)
    return glow.resize((diam, diam), Image.LANCZOS)


def make_wallpaper(w, h, with_text=True):
    bg = vgrad3(w, h, TOP, MID, BOT).convert("RGBA")
    # soft glow behind the lotus
    gd = int(h * 1.15)
    glow = radial_glow(gd, (255, 180, 215), strength=120)
    bg.alpha_composite(glow, (int(w/2 - gd/2), int(h*0.42 - gd/2)))
    # lotus (rendered big on its own layer for crisp edges)
    D = int(h * 0.40)
    layer = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    g.draw_lotus(ImageDraw.Draw(layer), w/2, h*0.42, D)
    bg.alpha_composite(layer)
    if with_text:
        d = ImageDraw.Draw(bg)
        d.text((w/2, h*0.70), "SenOS", font=g.font(int(h*0.058)),
               fill=(255, 255, 255, 255), anchor="mm")
        d.text((w/2, h*0.70 + int(h*0.052)), "Simple Vietnamese Linux",
               font=g.font(int(h*0.020), heavy=False), fill=(255, 220, 235, 230), anchor="mm")
    return bg.convert("RGB")


def save(img, rel):
    p = os.path.join(ROOT, rel)
    os.makedirs(os.path.dirname(p), exist_ok=True)
    if p.lower().endswith((".jpg", ".jpeg")):
        img.save(p, quality=92)
    else:
        img.save(p)
    print("  ", rel)


def main():
    wp = make_wallpaper(3840, 2160)
    B = "config/includes.chroot/usr/share/backgrounds/senos"
    # default.png MUST be a real image (was a broken symlink -> black desktop)
    save(wp, f"{B}/default.png")
    save(wp, f"{B}/default.jpg")
    save(wp, f"{B}/senos-wallpaper.png")
    save(wp, f"{B}/wallpaper.jpg")
    save(wp, f"{B}/senos-dark.png")
    # a lighter variant
    save(make_wallpaper(3840, 2160).point(lambda p: min(255, int(p*1.0))), f"{B}/senos-light.png")
    # repo asset copies
    save(wp, "assets/wallpaper.jpg")
    save(make_wallpaper(2560, 1440), "assets/Wallpaper 4K/senos_lotus.png")
    print("done.")


if __name__ == "__main__":
    main()
