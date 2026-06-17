#!/usr/bin/env python3
"""Regenerate README illustration screenshots with SenOS (prism-lotus) branding.
These are documentation mockups (not shipped in the ISO). Requires Pillow.
Run from repo root:  python scripts/gen_screenshots.py
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import gen_senos_theme as T
from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
W, H = 1280, 800
NAVY_TOP, NAVY_BOT, WHITE = T.NAVY_TOP, T.NAVY_BOT, (255, 255, 255)

def mono(sz):
    for f in ("C:/Windows/Fonts/consola.ttf", "C:/Windows/Fonts/cour.ttf"):
        try: return ImageFont.truetype(f, sz)
        except OSError: pass
    return ImageFont.load_default()

def save(img, rel):
    p = os.path.join(ROOT, rel); os.makedirs(os.path.dirname(p), exist_ok=True)
    img.convert("RGB").save(p); print("  ", rel)

def bg():
    return T.vgrad(W, H, NAVY_TOP, NAVY_BOT).convert("RGBA")

# ---- 01 boot menu ----
def boot_menu():
    img = bg(); d = ImageDraw.Draw(img)
    # faint big lotus right
    big = T.lotus_image(560); img.alpha_composite(big, (W-540, H-540))
    lot = T.lotus_image(64); img.alpha_composite(lot, (40, 30))
    d.text((112, 62), "SenOS", font=T.font(40), fill=WHITE+(255,), anchor="lm")
    d.text((W/2, 170), "Welcome to SenOS 1.0.1 64-bit", font=mono(24), fill=(220,225,240,255), anchor="mm")
    entries = ["Start SenOS", "Start SenOS (compatibility mode)", "OEM install (for manufacturers)",
               "Hardware Detection", "Boot from local drive", "Memory test"]
    x0, y0, bw, rh = 300, 240, 680, 40
    d.rectangle([x0-20, y0-16, x0-20+bw, y0-16+rh*len(entries)+24], outline=(90,100,130,255), width=2)
    fm = mono(22)
    for i, e in enumerate(entries):
        y = y0 + i*rh
        if i == 0:
            d.rectangle([x0-12, y-6, x0-12+bw-16, y+30], fill=(70,120,200,235))
        d.text((x0, y), e, font=fm, fill=WHITE+(255,) if i == 0 else (210,215,230,255), anchor="lm")
    d.text((W/2, 600), "Press ENTER to boot or TAB to edit a menu entry", font=mono(18), fill=(180,188,210,255), anchor="mm")
    d.text((W/2, 660), "Automatic boot in 4 seconds...", font=mono(18), fill=(150,160,185,255), anchor="mm")
    return img

# ---- 02 startup loading (plymouth) ----
def startup():
    img = bg(); d = ImageDraw.Draw(img)
    lot = T.lotus_image(280); img.alpha_composite(lot, (int(W/2-140), int(H/2-180)))
    d.text((W/2, H/2+120), "SenOS", font=T.font(54), fill=WHITE+(255,), anchor="mm")
    # progress dots
    import math
    for i in range(5):
        a = 90 + int(120*(0.5+0.5*math.cos(i)))
        cx = W/2 - 80 + i*40
        d.ellipse([cx-7, H/2+200-7, cx+7, H/2+200+7], fill=(255,255,255,a))
    return img

# ---- 03 desktop ----
def desktop():
    img = Image.open(os.path.join(T.WP, "aurora-3840x2160.png")).convert("RGBA").resize((W, H), Image.LANCZOS)
    d = ImageDraw.Draw(img)
    # bottom panel
    ph = 48
    panel = Image.new("RGBA", (W, ph), (16, 18, 30, 235)); img.alpha_composite(panel, (0, H-ph))
    menu = T.lotus_image(34); img.alpha_composite(menu, (10, H-ph+7))
    # a few app dots
    cols = [T.RED, T.ORANGE, T.GREEN, T.CYAN, T.PURPLE]
    for i, c in enumerate(cols):
        x = 70 + i*42
        d.ellipse([x, H-ph+12, x+24, H-ph+36], fill=c+(255,))
    d.text((W-20, H-ph/2), "21:42", font=T.font(20), fill=WHITE+(255,), anchor="rm")
    return img

# ---- 04 neofetch ----
def neofetch():
    img = Image.open(os.path.join(T.WP, "aurora-3840x2160.png")).convert("RGBA").resize((W, H), Image.LANCZOS)
    # terminal window
    tw, th, tx, ty = 980, 460, 150, 150
    term = Image.new("RGBA", (tw, th), (18, 20, 30, 245)); img.alpha_composite(term, (tx, ty))
    d = ImageDraw.Draw(img)
    d.rectangle([tx, ty, tx+tw, ty+30], fill=(34, 38, 52, 255))
    for i, c in enumerate([(255,95,86),(255,189,46),(39,201,63)]):
        d.ellipse([tx+14+i*22, ty+10, tx+26+i*22, ty+22], fill=c)
    d.text((tx+tw/2, ty+15), "senos@senos: ~", font=mono(15), fill=(200,205,220,255), anchor="mm")
    # SENOS block ascii (rainbow per letter group), left
    F = {'S':["#####","#....","#####","....#","#####"],'E':["#####","#....","####.","#....","#####"],
         'N':["#...#","##..#","#.#.#","#..##","#...#"],'O':[".###.","#...#","#...#","#...#",".###."]}
    word = "SENOS"; cols = [T.RED, T.ORANGE, T.GREEN, T.CYAN, T.PURPLE]
    cell = 7; ox, oy = tx+30, ty+70
    for ci, ch in enumerate(word):
        for r in range(5):
            for cc, v in enumerate(F[ch][r]):
                if v == '#':
                    px = ox + (ci*6+cc)*cell; py = oy + r*cell
                    d.rectangle([px, py, px+cell-1, py+cell-1], fill=cols[ci]+(255,))
    # info right
    info = [("senos","@senos"), ("OS","SenOS 1.0.1 Cinnamon x86_64"), ("Host","VMware Virtual Platform"),
            ("Kernel","6.8.0-generic"), ("Packages","2400 (dpkg)"), ("Shell","bash 5.2"),
            ("DE","Cinnamon 6.4"), ("Theme","Cinnamon-Delight"), ("Icons","SenOS Prism"),
            ("Terminal","gnome-terminal"), ("CPU","Intel (8)"), ("Memory","1850MiB / 16000MiB")]
    ix, iy = tx+300, ty+60; fm = mono(17)
    for k, v in info:
        if k == "senos":
            d.text((ix, iy), "senos", font=mono(17), fill=(57,217,138,255))
            d.text((ix+52, iy), "@senos", font=mono(17), fill=(52,198,255,255)); iy += 30; continue
        d.text((ix, iy), f"{k}", font=fm, fill=(52,198,255,255))
        d.text((ix+110, iy), f": {v}", font=fm, fill=(225,228,238,255)); iy += 28
    return img

def main():
    save(boot_menu(), "assets/screenshots/01-grub-menu.png")
    save(startup(),   "assets/screenshots/02-startup-loading.png")
    save(desktop(),   "assets/screenshots/03-desktop.png")
    save(neofetch(),  "assets/screenshots/04-neofetch.png")
    print("done.")

if __name__ == "__main__":
    main()
