#!/usr/bin/env python3
"""SenOS LIGHT theme assets: light prism-lotus icon set + light wallpapers.
Uses assets/images/light/ for system icons; generates light wallpapers.
Run from repo root:  python scripts/gen_senos_light.py   (requires Pillow)
"""
import math, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import gen_senos_theme as T
from PIL import Image, ImageDraw

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LIGHT = os.path.join(ROOT, "assets", "images", "light")
INK = (31, 36, 51)          # dark text on light
L_TOP = (245, 247, 251)     # light gradient top
L_BOT = (225, 231, 244)     # light gradient bottom (soft lavender)

def save(img, rel):
    p = os.path.join(ROOT, rel); os.makedirs(os.path.dirname(p), exist_ok=True)
    (img.convert("RGB").save(p, quality=92) if p.lower().endswith((".jpg",".jpeg")) else img.save(p))
    print("  ", rel)

def radial(diam, color, strength):
    t = 600; m = Image.new("L", (t, t), 0); px = m.load(); c = t/2
    for y in range(t):
        for x in range(t):
            d = math.hypot(x-c, y-c)/c
            px[x, y] = max(0, int(strength*(1-min(1, d))**1.8))
    g = Image.new("RGBA", (t, t), color+(0,)); g.putalpha(m)
    return g.resize((diam, diam), Image.LANCZOS)

def wallpaper(w, h, text=True):
    bg = T.vgrad(w, h, L_TOP, L_BOT).convert("RGBA")
    gd = int(h*1.2); bg.alpha_composite(radial(gd, (255,255,255), 150), (int(w/2-gd/2), int(h*0.40-gd/2)))
    D = int(h*0.46); lot = T.lotus_image(D)
    bg.alpha_composite(lot, (int(w/2 - D/2), int(h*0.42 - D*0.52)))
    if text:
        d = ImageDraw.Draw(bg)
        d.text((w/2, h*0.70), "SenOS", font=T.font(int(h*0.058)), fill=INK+(255,), anchor="mm")
        d.text((w/2, h*0.70+int(h*0.052)), "một sản phẩm của aksoft.vn",
               font=T.font(int(h*0.020), heavy=False), fill=(90,98,120,255), anchor="mm")
    return bg.convert("RGB")

def lockup(w, h):
    img = Image.new("RGBA", (w, h), (0,0,0,0))
    ls = int(h*0.96); lot = T.lotus_image(ls)
    img.alpha_composite(lot, (int(w*0.02), int((h-ls)/2)))
    ImageDraw.Draw(img).text((int(w*0.02)+ls+int(h*0.12), h*0.5), "SenOS",
                             font=T.font(int(h*0.5)), fill=INK+(255,), anchor="lm")
    return img

def main():
    ic1024 = Image.open(os.path.join(LIGHT, "icon-1024.png")).convert("RGBA")
    ic512  = Image.open(os.path.join(LIGHT, "icon-512.png")).convert("RGBA")
    def appicon(sz):
        src = {16:"icon-16",32:"icon-32",48:"icon-48",64:"icon-64",128:"icon-128",256:"icon-256",512:"icon-512"}.get(sz)
        return Image.open(os.path.join(LIGHT, src+".png")).convert("RGBA") if src else ic512.resize((sz,sz), Image.LANCZOS)

    print("== light system icons ==")
    for s in [16,22,24,32,48,64,96,128,256,512]:
        ic = appicon(s); sym = T.lotus_image(s, "symbolic")
        for kind in ("apps","places"):
            b = f"config/includes.chroot/usr/share/icons/hicolor/{s}x{s}/{kind}"
            save(ic, f"{b}/senos-logo.png"); save(sym, f"{b}/senos-logo-symbolic.png")
    save(ic512, "config/includes.chroot/usr/share/pixmaps/senos-logo.png")
    save(ic512, "config/includes.chroot/usr/share/pixmaps/senos.png")
    save(ic512, "config/includes.chroot/usr/share/pixmaps/senos-logo-full.png")
    save(lockup(770,160), "config/includes.chroot/usr/share/pixmaps/senos-lockup.png")
    save(ic512, "assets/Logo/SenOS_only_icon.png")
    save(ic512, "assets/SenOS_logo.png")

    print("== light wallpapers ==")
    B = "config/includes.chroot/usr/share/backgrounds/senos"
    wp = wallpaper(3840, 2160)
    save(wp, f"{B}/senos-light.png")
    save(wp, f"{B}/default.png"); save(wp, f"{B}/default.jpg")
    save(wp, f"{B}/senos-wallpaper.png"); save(wp, f"{B}/wallpaper.jpg")
    save(wallpaper(3840, 2160, text=False), f"{B}/senos-light-plain.png")
    save(wp, "assets/wallpaper.jpg")
    save(wallpaper(2560, 1440), "assets/Wallpaper 4K/senos_light.png")
    print("done.")

if __name__ == "__main__":
    main()
