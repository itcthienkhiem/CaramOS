#!/usr/bin/env python3
"""
SenOS "Prism Lotus" theme generator (dark + rainbow lotus).

Design language (from assets/images/mark.svg + assets/Wallpaper 4K/{aurora,bloom,facet}):
  - Mark: a 5-petal prism lotus (red/orange/green/cyan/purple kite petals + 2 faint
    outer petals) fanning from a bottom pivot, on a dark charcoal badge.
  - Wallpapers: aurora / bloom / facet on dark navy.

Generates: system icons (from the supplied icon PNGs), symbolic icons, SVG logos,
brand logos, plymouth/splash frames, banner, and installs the three wallpapers.

Run from repo root:  python scripts/gen_senos_theme.py   (requires Pillow)
"""
import math, os, sys
from PIL import Image, ImageDraw

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IMG  = os.path.join(ROOT, "assets", "images")
WP   = os.path.join(ROOT, "assets", "Wallpaper 4K")

# ---- prism palette (from mark.svg) -------------------------------------
RED, ORANGE, GREEN, CYAN, PURPLE = (255,93,115),(255,177,61),(57,217,138),(52,198,255),(176,123,255)
NAVY_TOP = (26, 29, 46)    # #1A1D2E
NAVY_BOT = (12, 13, 24)    # #0C0D18
WHITE = (255, 255, 255)
SYMBOL = (95, 95, 95)
FONT_BLACK = "C:/Windows/Fonts/seguibl.ttf"
FONT_BOLD  = "C:/Windows/Fonts/arialbd.ttf"
SS = 4

# mark.svg geometry (200x200 space, group translate(0,-6), pivot (100,162))
PIVOT = (100, 162)
FKITE   = [(100,42),(114,116),(100,160),(86,116)]
FSHADOW = [(100,42),(114,116),(100,160)]
BKITE   = [(100,84),(132,126),(100,160),(68,126)]
BSHADOW = [(100,84),(132,126),(100,160)]
FRONT = [(-44,RED),(-22,ORANGE),(0,GREEN),(22,CYAN),(44,PURPLE)]
BACK  = [(-76,RED),(76,PURPLE)]


def font(size, heavy=True):
    try: return __import__("PIL.ImageFont", fromlist=["ImageFont"]).truetype(FONT_BLACK if heavy else FONT_BOLD, size)
    except OSError: return __import__("PIL.ImageFont", fromlist=["ImageFont"]).truetype(FONT_BOLD, size)


def _rot(p, deg):
    a = math.radians(deg); ox, oy = PIVOT
    dx, dy = p[0]-ox, p[1]-oy
    return (ox + dx*math.cos(a) - dy*math.sin(a), oy + dx*math.sin(a) + dy*math.cos(a))


def lotus_image(box, mode="color"):
    s = box * SS; k = s / 200.0
    img = Image.new("RGBA", (s, s), (0,0,0,0)); d = ImageDraw.Draw(img)
    def poly(pts, deg, fill):
        d.polygon([(x*k, (y-6)*k) for x, y in (_rot(p, deg) for p in pts)], fill=fill)
    if mode == "symbolic":
        for deg, _c in BACK:  poly(BKITE, deg, SYMBOL+(110,))
        for deg, _c in FRONT: poly(FKITE, deg, SYMBOL+(255,))
        return img.resize((box, box), Image.LANCZOS)
    for deg, c in BACK:
        poly(BKITE, deg, c+(102,)); poly(BSHADOW, deg, (0,0,0,26))
    for deg, c in FRONT:
        poly(FKITE, deg, c+(255,)); poly(FSHADOW, deg, (0,0,0,41))
    return img.resize((box, box), Image.LANCZOS)


def vgrad(w, h, c0, c1):
    col = Image.new("RGB", (1, h))
    for y in range(h):
        t = y/max(1, h-1)
        col.putpixel((0, y), tuple(round(c0[i]+(c1[i]-c0[i])*t) for i in range(3)))
    return col.resize((w, h))


def lockup(w, h, sub=False):
    img = Image.new("RGBA", (w, h), (0,0,0,0))
    ls = int(h*0.96); lot = lotus_image(ls)
    img.alpha_composite(lot, (int(w*0.02), int((h-ls)/2)))
    d = ImageDraw.Draw(img)
    d.text((int(w*0.02)+ls+int(h*0.12), h*0.5), "SenOS", font=font(int(h*0.5)),
           fill=WHITE+(255,), anchor="lm")
    return img


def paste_centered(bg, ov, dy=0):
    bg = bg.convert("RGBA")
    bg.alpha_composite(ov, (int((bg.width-ov.width)/2), int((bg.height-ov.height)/2)+dy))
    return bg


def save(img, rel):
    p = os.path.join(ROOT, rel); os.makedirs(os.path.dirname(p), exist_ok=True)
    (img.convert("RGB").save(p, quality=92) if p.lower().endswith((".jpg",".jpeg")) else img.save(p))
    print("  ", rel)


def main():
    icon1024 = Image.open(os.path.join(IMG, "icon-1024.png")).convert("RGBA")
    icon512  = Image.open(os.path.join(IMG, "icon-512.png")).convert("RGBA")
    def appicon(sz):
        src = {16:"icon-16",32:"icon-32",48:"icon-48",64:"icon-64",128:"icon-128",256:"icon-256",512:"icon-512"}.get(sz)
        if src:
            return Image.open(os.path.join(IMG, src+".png")).convert("RGBA")
        return icon512.resize((sz, sz), Image.LANCZOS)

    print("== system icons (from supplied icon set) ==")
    for s in [16,22,24,32,48,64,96,128,256,512]:
        ic = appicon(s); sym = lotus_image(s, "symbolic")
        for kind in ("apps","places"):
            b = f"config/includes.chroot/usr/share/icons/hicolor/{s}x{s}/{kind}"
            save(ic,  f"{b}/senos-logo.png")
            save(sym, f"{b}/senos-logo-symbolic.png")

    print("== pixmaps ==")
    save(icon512, "config/includes.chroot/usr/share/pixmaps/senos-logo.png")
    save(icon512, "config/includes.chroot/usr/share/pixmaps/senos.png")
    save(icon512, "config/includes.chroot/usr/share/pixmaps/senos-logo-full.png")
    save(lotus_image(512, "symbolic"), "config/includes.chroot/usr/share/pixmaps/senos-logo-symbolic.png")
    save(lockup(770,160), "config/includes.chroot/usr/share/pixmaps/senos-lockup.png")

    print("== brand logo assets ==")
    save(icon512, "assets/Logo/SenOS_only_icon.png")
    save(icon512, "assets/SenOS_logo.png")
    save(icon512, "assets/SenOS_logo_dark.png")
    for n in ["assets/Logo + Name/SenOS_logo.png","assets/Logo + Name/SenOS_logo_dark.png"]:
        save(icon512, n)
    save(lockup(770,160), "assets/Horizontal Lockup/senos-lockup.png")

    print("== install wallpapers (aurora/bloom/facet) ==")
    B = "config/includes.chroot/usr/share/backgrounds/senos"
    aurora = Image.open(os.path.join(WP, "aurora-3840x2160.png")).convert("RGB")
    bloom  = Image.open(os.path.join(WP, "bloom-3840x2160.png")).convert("RGB")
    facet  = Image.open(os.path.join(WP, "facet-3840x2160.png")).convert("RGB")
    save(aurora, f"{B}/aurora.png"); save(bloom, f"{B}/bloom.png"); save(facet, f"{B}/facet.png")
    # default desktop wallpaper = aurora (clean). default.png MUST be a real image.
    save(aurora, f"{B}/default.png"); save(aurora, f"{B}/default.jpg")
    save(aurora, f"{B}/senos-wallpaper.png"); save(aurora, f"{B}/wallpaper.jpg")
    save(bloom,  f"{B}/senos-dark.png"); save(facet, f"{B}/senos-light.png")
    save(bloom,  "assets/wallpaper.jpg")

    print("== plymouth / splash (dark + prism lotus) ==")
    save(lotus_image(240), f"{B}/plymouth-logo.png")
    base = vgrad(640, 480, NAVY_TOP, NAVY_BOT)
    save(paste_centered(base, lockup(360, 92, ), dy=10), f"{B}/splash.png")
    save(paste_centered(vgrad(640,480,NAVY_TOP,NAVY_BOT), lockup(360,92), dy=10), "assets/splash.png")
    save(paste_centered(vgrad(640,640,NAVY_TOP,NAVY_BOT), lockup(420,108), dy=10), "assets/boot-splash.png")
    # watermark + animation (breathing lotus) + throbber (static)
    wm = lotus_image(240)
    save(wm, f"{B}/watermark.png")
    for i in range(1, 37):
        a = 0.55 + 0.45*(0.5 - 0.5*math.cos(2*math.pi*(i-1)/36))
        fr = lotus_image(240); fr.putalpha(fr.split()[3].point(lambda p: int(p*a)))
        save(fr, f"{B}/animation-%04d.png" % i)
    for i in range(1, 31):
        save(wm, f"{B}/throbber-%04d.png" % i)

    print("== banner (bloom style) ==")
    bn = bloom.resize((1280, 720), Image.LANCZOS).convert("RGBA")
    d = ImageDraw.Draw(bn)
    d.text((640, 600), "Open Beta · a product of AkSoft · aksoft.vn",
           font=font(int(720*0.035), heavy=False), fill=(225,230,245,255), anchor="mm")
    save(bn, "assets/senos_vietnam_banner.png"); save(bn.copy(), "senos_vietnam_banner.png")
    print("done.")


if __name__ == "__main__":
    main()
