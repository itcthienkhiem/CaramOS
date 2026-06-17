#!/usr/bin/env python3
"""
SenOS brand asset generator.

Generates the SenOS visual identity from code so a rebrand is reproducible.

Identity:
  - Mark: a stylised LOTUS flower (hoa sen) — a white, layered bloom on a
    rounded "squircle" badge with a pink->rose gradient.
  - Wordmark: the lotus mark + "SenOS" set in a heavy sans.

Run from the repo root:  python scripts/gen_brand_assets.py
Requires: Pillow.  (PNGs only — SVGs are authored separately.)
"""
import math
import os
from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# ---- lotus palette -----------------------------------------------------
PINK   = (244, 114, 182)   # #F472B6  gradient top
ROSE   = (219, 39, 119)    # #DB2777  gradient bottom
PLUM   = (131, 24, 67)     # #831843  dark text / dark bg
WHITE  = (255, 255, 255)
SYMBOL = (95, 95, 95)       # symbolic icon base color (theme recolors it)

FONT_BLACK = "C:/Windows/Fonts/seguibl.ttf"   # Segoe UI Black
FONT_BOLD  = "C:/Windows/Fonts/arialbd.ttf"
SS = 4  # supersample factor


def font(size, heavy=True):
    try:
        return ImageFont.truetype(FONT_BLACK if heavy else FONT_BOLD, size)
    except OSError:
        return ImageFont.truetype(FONT_BOLD, size)


def vgrad(w, h, c0, c1):
    col = Image.new("RGB", (1, h))
    for y in range(h):
        t = y / max(1, h - 1)
        col.putpixel((0, y), tuple(round(c0[i] + (c1[i] - c0[i]) * t) for i in range(3)))
    return col.resize((w, h))


def squircle_mask(size, radius_ratio=0.235):
    m = Image.new("L", (size, size), 0)
    ImageDraw.Draw(m).rounded_rectangle([0, 0, size - 1, size - 1],
                                        radius=int(size * radius_ratio), fill=255)
    return m


# ---- lotus geometry ----------------------------------------------------
def _cubic(p0, p1, p2, p3, n):
    pts = []
    for i in range(n + 1):
        t = i / n
        mt = 1 - t
        x = mt**3*p0[0] + 3*mt*mt*t*p1[0] + 3*mt*t*t*p2[0] + t**3*p3[0]
        y = mt**3*p0[1] + 3*mt*mt*t*p1[1] + 3*mt*t*t*p2[1] + t**3*p3[1]
        pts.append((x, y))
    return pts

# Normalised petal outline: base at (0,0), tip pointing up at (0,-1).
_PETAL = (_cubic((0, 0), (0.30, -0.18), (0.36, -0.64), (0, -1.0), 16)
          + _cubic((0, -1.0), (-0.36, -0.64), (-0.30, -0.18), (0, 0), 16))


def _petal_points(pivot, angle_deg, L, W):
    a = math.radians(angle_deg)
    ca, sa = math.cos(a), math.sin(a)
    out = []
    for x, y in _PETAL:
        x2, y2 = x * W, y * L
        rx = x2 * ca - y2 * sa
        ry = x2 * sa + y2 * ca
        out.append((pivot[0] + rx, pivot[1] + ry))
    return out


def draw_lotus(draw, cx, cy, D, mode="color"):
    """Draw a lotus centred near (cx, cy) with footprint ~D."""
    pivot = (cx, cy + 0.34 * D)
    back_ang  = [-60, -30, 0, 30, 60]
    front_ang = [-44, -15, 15, 44]
    Lb, Lf = 0.82 * D, 0.62 * D

    if mode == "symbolic":
        for ang in back_ang:
            draw.polygon(_petal_points(pivot, ang, Lb, 0.40 * Lb), fill=SYMBOL + (255,))
        for ang in front_ang:
            draw.polygon(_petal_points(pivot, ang, Lf, 0.42 * Lf), fill=SYMBOL + (255,))
        return

    edge = (219, 39, 119, 110)   # faint rose separator
    ew = max(1, int(D * 0.012))
    # back layer: translucent white (rose shows through -> soft pink)
    for ang in back_ang:
        draw.polygon(_petal_points(pivot, ang, Lb, 0.40 * Lb),
                     fill=(255, 255, 255, 150), outline=edge, width=ew)
    # front layer: solid white
    for ang in front_ang:
        draw.polygon(_petal_points(pivot, ang, Lf, 0.42 * Lf),
                     fill=WHITE + (255,), outline=edge, width=ew)
    # centre dot
    r = D * 0.05
    draw.ellipse([cx - r, pivot[1] - r*1.4, cx + r, pivot[1] + r*0.6], fill=(255, 226, 240, 255))


def make_icon(size, mode="color"):
    S = size * SS
    if mode == "symbolic":
        img = Image.new("RGBA", (S, S), (0, 0, 0, 0))
        draw_lotus(ImageDraw.Draw(img), S/2, S*0.52, S*0.74, mode="symbolic")
        return img.resize((size, size), Image.LANCZOS)
    grad = vgrad(S, S, PINK, ROSE).convert("RGBA")
    grad.putalpha(squircle_mask(S))
    draw_lotus(ImageDraw.Draw(grad), S/2, S*0.50, S*0.62)
    return grad.resize((size, size), Image.LANCZOS)


def lotus_glyph(size, color="rose"):
    """Standalone coloured lotus on transparent (for watermarks/wordmark accents)."""
    S = size * SS
    img = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    return img  # (unused placeholder kept for clarity)


def wordmark_stacked(size, dark_text=True):
    S = size
    img = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    icon = make_icon(int(S * 0.5))
    img.alpha_composite(icon, (int((S - icon.width) / 2), int(S * 0.12)))
    d = ImageDraw.Draw(img)
    d.text((S/2, int(S*0.82)), "SenOS", font=font(int(S*0.17)),
           fill=(PLUM if dark_text else WHITE) + (255,), anchor="mm")
    return img


def lockup(w, h, dark_text=True):
    img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    icon_s = int(h * 0.86)
    icon = make_icon(icon_s)
    pad = int(h * 0.07)
    img.alpha_composite(icon, (pad, int((h - icon_s) / 2)))
    d = ImageDraw.Draw(img)
    d.text((pad + icon_s + int(h*0.16), h/2), "SenOS", font=font(int(h*0.46)),
           fill=(PLUM if dark_text else WHITE) + (255,), anchor="lm")
    return img


def paste_centered(bg, overlay, dy=0):
    bg = bg.convert("RGBA")
    bg.alpha_composite(overlay, (int((bg.width-overlay.width)/2),
                                 int((bg.height-overlay.height)/2)+dy))
    return bg


def watermark(bg_rgb, light_logo, scale=0.30, opacity=235, dy=0):
    bg = bg_rgb.convert("RGBA")
    lw = int(bg.width * scale); lh = int(lw * 0.28)
    lk = lockup(lw, lh, dark_text=not light_logo)
    if opacity < 255:
        lk.putalpha(lk.split()[3].point(lambda p: int(p * opacity / 255)))
    return paste_centered(bg, lk, dy)


def save(img, relpath):
    path = os.path.join(ROOT, relpath)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    if path.lower().endswith((".jpg", ".jpeg")):
        img.convert("RGB").save(path, quality=92)
    else:
        img.save(path)
    print("  ", relpath)


def main():
    print("== brand logo assets ==")
    save(wordmark_stacked(512, True),  "assets/Logo + Name/SenOS_logo.png")
    save(wordmark_stacked(512, True),  "assets/Logo + Name/SenOS_logo.jpg")
    save(wordmark_stacked(512, False), "assets/Logo + Name/SenOS_logo_dark.png")
    save(wordmark_stacked(512, False), "assets/Logo + Name/SenOS_logo_dark.jpg")
    save(wordmark_stacked(512, True),  "assets/SenOS_logo.png")
    save(wordmark_stacked(512, False), "assets/SenOS_logo_dark.png")
    save(make_icon(512),               "assets/Logo/SenOS_only_icon.png")
    save(lockup(770, 160, True),       "assets/Horizontal Lockup/senos-lockup.png")

    print("== pixmaps ==")
    save(make_icon(512),            "config/includes.chroot/usr/share/pixmaps/senos-logo.png")
    save(make_icon(512),            "config/includes.chroot/usr/share/pixmaps/senos.png")
    save(wordmark_stacked(512, True), "config/includes.chroot/usr/share/pixmaps/senos-logo-full.png")
    save(make_icon(512, "symbolic"),  "config/includes.chroot/usr/share/pixmaps/senos-logo-symbolic.png")
    save(lockup(770, 160, True),      "config/includes.chroot/usr/share/pixmaps/senos-lockup.png")

    print("== hicolor icon theme (raster) ==")
    for s in [16, 22, 24, 32, 48, 64, 96, 128, 256, 512]:
        for kind in ("apps", "places"):
            base = f"config/includes.chroot/usr/share/icons/hicolor/{s}x{s}/{kind}"
            save(make_icon(s),             f"{base}/senos-logo.png")
            save(make_icon(s, "symbolic"), f"{base}/senos-logo-symbolic.png")

    print("== plymouth / splash ==")
    save(make_icon(240), "config/includes.chroot/usr/share/backgrounds/senos/plymouth-logo.png")
    sp = vgrad(640, 480, PLUM, (60, 12, 36))
    save(paste_centered(sp, lockup(360, 100, False)), "config/includes.chroot/usr/share/backgrounds/senos/splash.png")
    save(paste_centered(sp.copy(), lockup(360, 100, False)), "assets/splash.png")
    bs = vgrad(640, 640, PLUM, (60, 12, 36))
    save(paste_centered(bs, lockup(440, 122, False)), "assets/boot-splash.png")

    print("== wallpapers ==")
    hero = vgrad(2000, 1121, ROSE, PINK)
    save(watermark(hero, True, 0.30),        "assets/wallpaper.jpg")
    save(watermark(hero.copy(), True, 0.30), "config/includes.chroot/usr/share/backgrounds/senos/default.jpg")
    save(watermark(hero.copy(), True, 0.30), "config/includes.chroot/usr/share/backgrounds/senos/senos-wallpaper.png")
    save(watermark(vgrad(3840, 2160, (42, 10, 30), ROSE), True, 0.26),
         "config/includes.chroot/usr/share/backgrounds/senos/senos-dark.png")
    save(watermark(vgrad(3840, 2160, (255, 241, 245), (250, 209, 225)), False, 0.26),
         "config/includes.chroot/usr/share/backgrounds/senos/senos-light.png")
    solids = {"202020": (0x20,)*3, "303030": (0x30,)*3, "e0e0e0": (0xe0,)*3, "f0f0f0": (0xf0,)*3}
    for name, c in solids.items():
        save(watermark(Image.new("RGB", (3840, 2160), c), light_logo=(c[0] <= 0x80),
                       scale=0.22, opacity=70), f"assets/Wallpaper 4K/senos_{name}.png")

    print("== banner ==")
    bn = vgrad(640, 640, ROSE, PINK).convert("RGBA")
    bn = paste_centered(bn, lockup(470, 128, False), dy=-44)
    d = ImageDraw.Draw(bn)
    d.text((320, 402), "Open Beta", font=font(int(640*0.07)), fill=WHITE + (255,), anchor="mm")
    d.text((320, 470), "Simple Vietnamese Linux", font=font(int(640*0.045), False),
           fill=(255, 235, 245, 255), anchor="mm")
    d.text((320, 560), "a product of AkSoft · aksoft.vn", font=font(int(640*0.04), False),
           fill=(255, 222, 238, 255), anchor="mm")
    save(bn, "assets/senos_vietnam_banner.png")
    save(bn.copy(), "senos_vietnam_banner.png")
    print("done.")


if __name__ == "__main__":
    main()
