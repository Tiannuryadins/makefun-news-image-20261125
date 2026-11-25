#!/usr/bin/env python3
"""Render the 25 November 2026 world-news poster (1024x1024 PNG).

Fresh renderer written 25 Nov 2026 for make.fun news-image-20261125.
Every story and figure was checked against live sources on 25 Nov 2026
(OneTurn, BBC/Guardian via OneTurn, Reuters, AP, The Hindu, SRI,
Newsof.today). No network access, no randomness, no timestamps in the
image: two runs produce byte-identical PNG output.

Structure (per the news-image playbook, visual-first):
  masthead + red italic dek naming the top 3 stories + 7-stat number
  strip + 7 region tabs + 3 large illustrated leads + 10 illustrated
  cards + world map with story dots + 18-line index = 31 stories,
  14 illustrations (13 scenes + map).
"""
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
M = 16                      # outer margin
CW = W - 2 * M              # content width = 992

FONT_DIR = "/usr/share/fonts/truetype/noto"
SERIF = os.path.join(FONT_DIR, "NotoSerif-Bold.ttf")
SERIF_R = os.path.join(FONT_DIR, "NotoSerif-Regular.ttf")
SERIF_I = os.path.join(FONT_DIR, "NotoSerif-Italic.ttf")
SERIF_BI = os.path.join(FONT_DIR, "NotoSerif-BoldItalic.ttf")
SANS = os.path.join(FONT_DIR, "NotoSans-Regular.ttf")
SANS_B = os.path.join(FONT_DIR, "NotoSans-Bold.ttf")
SANS_I = os.path.join(FONT_DIR, "NotoSans-Italic.ttf")


def font(path, size):
    return ImageFont.truetype(path, size)


# ---------------------------------------------------------------- palette
PAPER = (247, 242, 232)
INK = (26, 26, 26)
RED = (176, 30, 36)
NAVY = (22, 50, 79)
TEAL = (15, 96, 104)
GOLD = (184, 134, 11)
GREEN = (31, 122, 60)
ORANGE = (214, 96, 20)
GREY = (90, 88, 82)
LINE = (200, 192, 176)
CARD_BG = (255, 255, 255)

REGION_COLORS = [
    ("NORTH AMERICA", (22, 50, 79)),
    ("SOUTH AMERICA", (31, 122, 60)),
    ("EUROPE", (96, 56, 140)),
    ("MIDDLE EAST", (176, 30, 36)),
    ("AFRICA", (214, 120, 20)),
    ("ASIA-PACIFIC", (15, 96, 104)),
    ("TECH & MARKETS", (60, 60, 60)),
]


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap returning a list of lines fitting max_w."""
    lines, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= max_w or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def text_block(draw, x, y, lines, fnt, fill, leading):
    for ln in lines:
        draw.text((x, y), ln, font=fnt, fill=fill)
        y += leading
    return y


def rounded_rect(draw, box, radius, fill=None, outline=None, width=1):
    draw.rounded_rectangle(box, radius=radius, fill=fill,
                           outline=outline, width=width)


# ================================================================ scenes
# Each scene draws a fresh, story-specific illustration into a new image.
# No illustration is reused from earlier editions.

def scene_nvidia(w, h):
    """Night skyline + plunging chart + green chip."""
    img = Image.new("RGB", (w, h), (13, 27, 48))
    d = ImageDraw.Draw(img)
    for i, (sx, sy) in enumerate([(20, 18), (70, 30), (140, 12), (200, 26),
                                  (260, 14), (300, 32), (40, 44), (230, 44)]):
        d.ellipse([sx, sy, sx + 3, sy + 3], fill=(255, 255, 200))
    # skyline
    for bx, bw, bh in [(0, 34, 46), (36, 26, 70), (64, 40, 52), (106, 30, 82),
                       (138, 44, 58), (184, 28, 74), (214, 36, 50),
                       (252, 30, 66), (284, 38, 44)]:
        d.rectangle([bx, h - bh - 26, bx + bw, h - 26], fill=(8, 16, 30))
        for wy in range(h - bh - 20, h - 30, 12):
            for wx in range(bx + 5, bx + bw - 4, 10):
                if (wx + wy) % 23 < 9:
                    d.rectangle([wx, wy, wx + 4, wy + 5], fill=(255, 214, 90))
    # ground + chip
    d.rectangle([0, h - 26, w, h], fill=(5, 10, 20))
    d.rounded_rectangle([w // 2 - 52, h - 118, w // 2 + 52, h - 78],
                        radius=6, fill=(118, 200, 70), outline=(230, 255, 210), width=2)
    f = font(SANS_B, 26)
    d.text((w // 2 - 40, h - 114), "NVDA", font=f, fill=(10, 40, 10))
    # plunging chart
    pts = [(14, 26), (52, 34), (90, 30), (128, 52), (166, 48), (204, 74),
           (242, 70), (280, 100), (w - 12, 128)]
    d.line(pts, fill=(255, 70, 60), width=4)
    d.polygon([(w - 26, 118), (w - 6, 118), (w - 16, 140)], fill=(255, 70, 60))
    return img


def scene_hormuz(w, h):
    """Dusk strait: tanker, spiky mines, explosion burst."""
    img = Image.new("RGB", (w, h), (232, 122, 44))
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, w, 58], fill=(244, 178, 92))
    d.ellipse([w - 62, 6, w - 14, 54], fill=(255, 226, 150))
    d.rectangle([0, 58, w, h], fill=(28, 68, 96))
    for y in range(66, h, 14):
        d.line([(0, y), (w, y)], fill=(52, 104, 138), width=2)
    # distant headland
    d.polygon([(0, 58), (70, 30), (150, 58)], fill=(120, 70, 44))
    # tanker
    d.rectangle([58, 96, 252, 122], fill=(24, 24, 28))
    for cx in range(66, 246, 26):
        d.rectangle([cx, 78, cx + 20, 96], fill=(190, 60, 40))
    d.rectangle([226, 66, 244, 96], fill=(220, 220, 210))
    d.rectangle([228, 60, 242, 66], fill=(40, 40, 40))
    # mines
    for mx, my in [(36, 128), (286, 132)]:
        for ang in range(0, 360, 45):
            import math
            x2 = mx + int(13 * math.cos(math.radians(ang)))
            y2 = my + int(13 * math.sin(math.radians(ang)))
            d.line([(mx, my), (x2, y2)], fill=(20, 20, 20), width=3)
        d.ellipse([mx - 8, my - 8, mx + 8, my + 8], fill=(20, 20, 20))
    # explosion burst above tanker
    cx, cy = 150, 66
    for r, col in [(30, (255, 210, 60)), (20, (255, 140, 30)), (11, (255, 80, 20))]:
        pts = []
        import math
        for k in range(12):
            ang = math.radians(k * 30)
            rr = r if k % 2 == 0 else r * 0.55
            pts.append((cx + rr * math.cos(ang), cy + rr * math.sin(ang)))
        d.polygon(pts, fill=col)
    # smoke
    for sx, sy, sr in [(120, 44, 10), (140, 36, 12), (164, 42, 9)]:
        d.ellipse([sx - sr, sy - sr, sx + sr, sy + sr], fill=(90, 90, 92))
    return img


def scene_selloff(w, h):
    """Falling market bars + Tokyo tower + red arrows."""
    img = Image.new("RGB", (w, h), (240, 236, 224))
    d = ImageDraw.Draw(img)
    # Tokyo tower silhouette
    d.polygon([(w - 74, h), (w - 62, 34), (w - 56, 34), (w - 44, h)],
              fill=(150, 40, 40))
    d.line([(w - 59, 34), (w - 59, 16)], fill=(150, 40, 40), width=3)
    d.rectangle([w - 76, h - 52, w - 42, h - 44], fill=(150, 40, 40))
    # descending bars (values in white inside each bar)
    bars = [("NIKKEI", "-2.76%", 60, (176, 30, 36)),
            ("S&P", "-0.5%", 42, (214, 96, 20)),
            ("SENSEX", "+1.8%", 78, (31, 122, 60))]
    bx = 18
    for label, val, bh, col in bars:
        d.rectangle([bx, h - 30 - bh, bx + 56, h - 30], fill=col)
        f = font(SANS_B, 13)
        d.text((bx + 4, h - 28 - bh), val, font=f, fill=(255, 255, 255))
        d.text((bx + 2, h - 28), label, font=f, fill=INK)
        bx += 72
    return img


def scene_microsoft(w, h):
    """Dark server room, red CODE RED banner, warning triangle."""
    img = Image.new("RGB", (w, h), (18, 24, 34))
    d = ImageDraw.Draw(img)
    # red banner across the top
    d.rectangle([0, 0, w, 24], fill=(176, 30, 36))
    f = font(SANS_B, 16)
    d.text((8, 3), "CODE RED", font=f, fill=(255, 255, 255))
    d.text((w - 74, 5), "24h OUTAGE", font=font(SANS_B, 10),
           fill=(255, 210, 210))
    # server racks below
    for rx in (10, 70, 130):
        d.rectangle([rx, 32, rx + 48, h - 6], fill=(44, 56, 72),
                    outline=(120, 140, 160), width=1)
        for ry in range(38, h - 12, 13):
            col = (90, 220, 110) if (rx + ry) % 3 else (230, 60, 50)
            d.rectangle([rx + 6, ry, rx + 15, ry + 6], fill=col)
            d.rectangle([rx + 21, ry, rx + 42, ry + 6], fill=(30, 38, 50))
    return img


def scene_shenzhou(w, h):
    """Night launch: rocket, flame, stars, Earth curve."""
    img = Image.new("RGB", (w, h), (10, 16, 40))
    d = ImageDraw.Draw(img)
    for sx, sy in [(14, 12), (60, 30), (120, 10), (170, 26), (30, 52), (150, 48)]:
        d.ellipse([sx, sy, sx + 3, sy + 3], fill=(255, 255, 255))
    # Earth curve
    d.ellipse([-40, h - 26, w + 40, h + 60], fill=(30, 90, 160))
    d.ellipse([20, h - 18, 90, h + 10], fill=(40, 120, 90))
    # rocket
    rx = w // 2
    d.polygon([(rx, 8), (rx - 12, 30), (rx + 12, 30)], fill=(200, 30, 30))
    d.rectangle([rx - 12, 30, rx + 12, 66], fill=(235, 235, 230))
    d.rectangle([rx - 12, 44, rx + 12, 52], fill=(200, 30, 30))
    d.polygon([(rx - 12, 66), (rx - 22, 78), (rx - 12, 72)], fill=(180, 30, 30))
    d.polygon([(rx + 12, 66), (rx + 22, 78), (rx + 12, 72)], fill=(180, 30, 30))
    d.polygon([(rx - 6, 66), (rx + 6, 66), (rx + 12, 88), (rx, 96), (rx - 12, 88)],
              fill=(255, 180, 40))
    # station
    d.rectangle([w - 52, 14, w - 14, 20], fill=(200, 200, 190))
    d.rectangle([w - 40, 8, w - 26, 26], fill=(160, 160, 150))
    return img


def scene_cartagena(w, h):
    """Supermarket front with striped awning + police cordon tape."""
    img = Image.new("RGB", (w, h), (250, 244, 228))
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, w, h], fill=(250, 244, 228))
    # building
    d.rectangle([16, 26, w - 16, h - 18], fill=(250, 250, 248),
                outline=(120, 110, 100), width=2)
    # striped awning
    for i in range(9):
        col = (176, 30, 36) if i % 2 == 0 else (255, 255, 255)
        d.rectangle([16 + i * 19, 26, 16 + (i + 1) * 19, 44], fill=col)
    # windows / doors
    d.rectangle([26, 56, 76, h - 18], fill=(120, 170, 210))
    d.rectangle([86, 56, 136, h - 18], fill=(120, 170, 210))
    d.rectangle([146, 56, w - 26, h - 18], fill=(90, 90, 96))
    f = font(SANS_B, 15)
    d.text((20, 6), "SUPERMARKET", font=f, fill=INK)
    # cordon tape
    d.rectangle([0, h - 16, w, h - 4], fill=(255, 210, 40))
    for tx in range(0, w, 24):
        d.polygon([(tx, h - 16), (tx + 12, h - 16), (tx + 6, h - 4), (tx - 6, h - 4)],
                  fill=(20, 20, 20))
    return img


def scene_senegal(w, h):
    """Green pitch, gold trophy, confetti, flag stripes."""
    img = Image.new("RGB", (w, h), (24, 110, 52))
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, w, 14], fill=(0, 140, 60))
    d.rectangle([0, 14, w, 28], fill=(255, 220, 0))
    d.rectangle([0, 28, w, 42], fill=(220, 40, 40))
    # pitch lines
    d.ellipse([w // 2 - 46, 52, w // 2 + 46, 96], outline=(255, 255, 255), width=2)
    d.line([(0, 74), (w, 74)], fill=(255, 255, 255), width=2)
    # trophy
    cx, cy = w // 2, 62
    d.polygon([(cx - 22, 46), (cx - 30, 30), (cx - 18, 30), (cx - 18, 46)],
              fill=(255, 200, 40))
    d.polygon([(cx + 22, 46), (cx + 30, 30), (cx + 18, 30), (cx + 18, 46)],
              fill=(255, 200, 40))
    d.polygon([(cx - 18, 28), (cx + 18, 28), (cx + 12, 52), (cx - 12, 52)],
              fill=(255, 215, 60), outline=(160, 110, 0))
    d.rectangle([cx - 4, 52, cx + 4, 62], fill=(255, 215, 60))
    d.rectangle([cx - 14, 62, cx + 14, 68], fill=(255, 215, 60))
    # confetti
    for px, py, col in [(20, 50, (255, 220, 0)), (40, 84, (255, 255, 255)),
                        (160, 48, (255, 220, 0)), (172, 82, (255, 80, 80)),
                        (90, 88, (255, 255, 255)), (120, 50, (255, 80, 80))]:
        d.rectangle([px, py, px + 5, py + 5], fill=col)
    return img


def scene_solomon(w, h):
    """Two flags over ocean: Solomon Islands + Australia."""
    img = Image.new("RGB", (w, h), (60, 140, 200))
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, w, h], fill=(60, 140, 200))
    for y in range(0, h, 12):
        d.line([(0, y), (w, y)], fill=(80, 160, 215), width=2)
    # Solomon Islands flag (left)
    fx, fy, fw, fh = 14, 14, 74, 46
    d.polygon([(fx, fy), (fx + fw, fy), (fx, fy + fh)], fill=(20, 80, 180))
    d.polygon([(fx, fy + fh), (fx + fw, fy), (fx + fw, fy + fh)], fill=(40, 160, 60))
    d.line([(fx, fy + fh), (fx + fw, fy)], fill=(255, 220, 0), width=3)
    for sx, sy in [(fx + 14, fy + 12), (fx + 26, fy + 8), (fx + 38, fy + 14),
                   (fx + 20, fy + 20), (fx + 32, fy + 22)]:
        d.ellipse([sx - 2, sy - 2, sx + 2, sy + 2], fill=(255, 255, 255))
    # Australia flag (right)
    ax, ay, aw, ah = 104, 14, 74, 46
    d.rectangle([ax, ay, ax + aw, ay + ah], fill=(20, 40, 120))
    d.rectangle([ax, ay, ax + 34, ay + 22], fill=(200, 30, 40))
    d.line([(ax, ay), (ax + 34, ay + 22)], fill=(255, 255, 255), width=2)
    d.line([(ax + 34, ay), (ax, ay + 22)], fill=(255, 255, 255), width=2)
    for sx, sy in [(ax + 56, ay + 10), (ax + 66, ay + 26), (ax + 48, ay + 32),
                   (ax + 62, ay + 40)]:
        d.ellipse([sx - 2, sy - 2, sx + 2, sy + 2], fill=(255, 255, 255))
    # handshake arc + sun
    d.arc([60, 58, 134, 92], 180, 360, fill=(255, 220, 0), width=4)
    d.text((58, 68), "PACT", font=font(SANS_B, 16), fill=(255, 255, 255))
    return img


def scene_house(w, h):
    """US Capitol dome on navy, big 259."""
    img = Image.new("RGB", (w, h), (22, 50, 79))
    d = ImageDraw.Draw(img)
    for sx, sy in [(14, 12), (50, 22), (170, 14), (150, 30), (90, 10)]:
        d.ellipse([sx, sy, sx + 3, sy + 3], fill=(255, 255, 255))
    cx = w // 2
    # dome
    d.ellipse([cx - 34, 26, cx + 34, 78], fill=(240, 240, 235))
    d.rectangle([cx - 40, 62, cx + 40, 84], fill=(240, 240, 235))
    d.rectangle([cx - 46, 78, cx + 46, 84], fill=(220, 220, 215))
    d.line([(cx, 26), (cx, 16)], fill=(240, 240, 235), width=3)
    d.ellipse([cx - 3, 12, cx + 3, 18], fill=(255, 215, 60))
    # wings
    d.rectangle([18, 66, cx - 40, 84], fill=(210, 210, 205))
    d.rectangle([cx + 40, 66, w - 18, 84], fill=(210, 210, 205))
    d.rectangle([0, 84, w, h], fill=(16, 36, 58))
    f = font(SERIF, 26)
    d.text((16, 4), "259", font=f, fill=(255, 215, 60))
    return img


def scene_spain(w, h):
    """Ballot box + Spanish flag + ballot paper."""
    img = Image.new("RGB", (w, h), (245, 240, 225))
    d = ImageDraw.Draw(img)
    # Spanish flag top
    d.rectangle([0, 0, w, 12], fill=(200, 30, 40))
    d.rectangle([0, 12, w, 30], fill=(255, 210, 40))
    d.rectangle([0, 30, w, 42], fill=(200, 30, 40))
    # ballot box
    d.rectangle([56, 52, 140, 92], fill=(90, 60, 160))
    d.rectangle([56, 52, 140, 60], fill=(110, 78, 180))
    d.rectangle([86, 46, 110, 52], fill=(30, 30, 30))
    # ballot paper going in
    d.polygon([(92, 14), (118, 14), (118, 46), (92, 46)], fill=(255, 255, 255),
              outline=(120, 120, 120))
    d.line([(98, 24), (112, 24)], fill=(40, 120, 60), width=3)
    d.line([(98, 32), (112, 32)], fill=(150, 150, 150), width=2)
    d.line([(98, 40), (106, 40)], fill=(150, 150, 150), width=2)
    d.text((66, 68), "VOTA", font=font(SANS_B, 13), fill=(255, 255, 255))
    return img


def scene_tariffs(w, h):
    """Stacked shipping containers + crane hook + % tag."""
    img = Image.new("RGB", (w, h), (235, 230, 215))
    d = ImageDraw.Draw(img)
    cols = [(200, 60, 40), (30, 110, 160), (220, 150, 30), (40, 140, 80)]
    d.rectangle([14, 58, 86, 84], fill=cols[0])
    d.rectangle([90, 58, 162, 84], fill=cols[1])
    d.rectangle([50, 30, 122, 56], fill=cols[2])
    d.rectangle([126, 30, 182, 56], fill=cols[3])
    for (x0, y0, x1, y1) in [(14, 58, 86, 84), (90, 58, 162, 84),
                             (50, 30, 122, 56), (126, 30, 182, 56)]:
        for vx in range(x0 + 8, x1, 12):
            d.line([(vx, y0), (vx, y1)], fill=(0, 0, 0, 40), width=1)
    # crane hook
    d.line([(176, 0), (176, 22)], fill=(60, 60, 60), width=3)
    d.arc([166, 18, 186, 38], 0, 270, fill=(60, 60, 60), width=3)
    # % tag
    d.rounded_rectangle([8, 6, 66, 28], radius=5, fill=(176, 30, 36))
    d.text((14, 8), "16 NATIONS", font=font(SANS_B, 12), fill=(255, 255, 255))
    return img


def scene_bangladesh(w, h):
    """Garment factory, chimneys, thread spools, +36% tag."""
    img = Image.new("RGB", (w, h), (250, 238, 210))
    d = ImageDraw.Draw(img)
    # factory
    d.rectangle([14, 48, 150, 88], fill=(190, 90, 60))
    d.polygon([(14, 48), (38, 30), (62, 48)], fill=(150, 60, 40))
    d.polygon([(62, 48), (86, 30), (110, 48)], fill=(150, 60, 40))
    d.polygon([(110, 48), (134, 30), (150, 48)], fill=(150, 60, 40))
    d.rectangle([126, 14, 140, 48], fill=(120, 60, 50))
    d.ellipse([132, 6, 152, 20], fill=(230, 230, 225))
    d.ellipse([144, 10, 162, 24], fill=(230, 230, 225))
    for wx in range(24, 146, 24):
        d.rectangle([wx, 60, wx + 12, 76], fill=(255, 220, 120))
    # spools
    for sx, col in [(162, (30, 110, 160)), (178, (200, 30, 40))]:
        d.rectangle([sx, 56, sx + 12, 88], fill=col)
        d.rectangle([sx - 2, 52, sx + 14, 58], fill=(240, 240, 230))
        d.rectangle([sx - 2, 86, sx + 14, 90], fill=(240, 240, 230))
    d.rounded_rectangle([8, 6, 84, 28], radius=5, fill=(31, 122, 60))
    d.text((14, 8), "WAGES +36%", font=font(SANS_B, 12), fill=(255, 255, 255))
    return img


def scene_jets(w, h):
    """Fighter jet over radar rings, dusk sky."""
    img = Image.new("RGB", (w, h), (250, 200, 120))
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, w, 56], fill=(250, 200, 120))
    d.rectangle([0, 56, w, h], fill=(90, 60, 90))
    d.ellipse([w - 46, 6, w - 10, 42], fill=(255, 240, 180))
    # radar rings
    for r in (18, 30, 42):
        d.ellipse([26 - r, 66 - r, 26 + r, 66 + r], outline=(255, 255, 255), width=2)
    d.line([(26, 66), (60, 40)], fill=(255, 80, 60), width=3)
    # jet silhouette
    jx, jy = 110, 44
    d.polygon([(jx - 52, jy), (jx - 30, jy - 6), (jx + 34, jy - 3),
               (jx + 52, jy), (jx + 34, jy + 3), (jx - 30, jy + 6)],
              fill=(30, 30, 36))
    d.polygon([(jx - 18, jy - 6), (jx - 2, jy - 22), (jx + 6, jy - 6)],
              fill=(30, 30, 36))
    d.polygon([(jx - 34, jy + 4), (jx - 22, jy + 16), (jx - 12, jy + 4)],
              fill=(30, 30, 36))
    d.polygon([(jx - 52, jy), (jx - 64, jy - 4), (jx - 64, jy + 4)],
              fill=(255, 120, 40))
    return img


# ================================================================ world map
# Simplified continent outlines (equirectangular) with story dots.

CONTINENTS = [
    # North America
    [(-168, 66), (-140, 70), (-120, 72), (-95, 80), (-75, 72), (-60, 62),
     (-55, 47), (-70, 42), (-80, 32), (-97, 26), (-105, 20), (-118, 15),
     (-95, 16), (-86, 12), (-105, 22), (-125, 40), (-150, 60), (-168, 66)],
    # South America
    [(-80, 10), (-60, 8), (-50, 0), (-35, -8), (-40, -22), (-55, -35),
     (-68, -52), (-73, -40), (-70, -18), (-80, -5), (-80, 10)],
    # Africa
    [(-17, 15), (-10, 30), (10, 37), (30, 32), (43, 12), (51, 11),
     (40, -5), (35, -18), (28, -33), (18, -35), (12, -18), (9, 4),
     (-8, 4), (-17, 15)],
    # Europe
    [(-10, 36), (-9, 43), (-2, 48), (0, 51), (5, 58), (10, 62), (18, 56),
     (24, 60), (30, 60), (28, 54), (23, 45), (19, 42), (12, 44), (3, 42),
     (-10, 36)],
    # Asia
    [(30, 60), (40, 68), (60, 70), (90, 75), (120, 73), (150, 70),
     (170, 66), (160, 60), (140, 40), (130, 33), (120, 22), (108, 10),
     (100, 8), (90, 15), (80, 8), (70, 20), (60, 25), (50, 29), (43, 12),
     (35, 30), (30, 36), (30, 60)],
    # Australia
    [(113, -22), (122, -14), (132, -12), (142, -11), (150, -22), (153, -27),
     (150, -37), (140, -38), (130, -32), (115, -35), (113, -22)],
]

# (lon, lat, region index into REGION_COLORS)
DOTS = [
    (-122, 37, 0), (-74, 40, 0), (-75, 10, 1), (-58, -35, 2),
    (51, 26, 3), (44, 33, 3), (3, 46, 2), (28, -26, 4),
    (139, 35, 5), (121, 31, 5), (77, 28, 5), (151, -34, 5),
    (31, 30, 3), (18, -1, 4), (103, 1, 5),
]


def draw_world_map(w, h):
    img = Image.new("RGB", (w, h), (214, 228, 240))
    d = ImageDraw.Draw(img)
    # graticule
    for gx in range(0, w, 42):
        d.line([(gx, 0), (gx, h)], fill=(190, 205, 222), width=1)
    for gy in range(0, h, 30):
        d.line([(0, gy), (w, gy)], fill=(190, 205, 222), width=1)

    def proj(lon, lat):
        return ((lon + 180) / 360.0 * w, (90 - lat) / 180.0 * h)

    for poly in CONTINENTS:
        pts = [proj(lon, lat) for lon, lat in poly]
        d.polygon(pts, fill=(168, 196, 150), outline=(120, 150, 110))
    for lon, lat, reg in DOTS:
        x, y = proj(lon, lat)
        col = REGION_COLORS[reg][1]
        d.ellipse([x - 5, y - 5, x + 5, y + 5], fill=col,
                  outline=(255, 255, 255), width=2)
    return img


# ================================================================ content
DEK = ("Nvidia slides 7% as Congress questions Trump's role in Huang's "
       "return \u2014 mines strike two tankers in Hormuz \u2014 Asia's "
       "AI sell-off deepens")

STATS = [
    ("-7%", "NVIDIA SHARES"),
    ("-2.76%", "NIKKEI, TOKYO"),
    ("7,201", "S&P 500, -0.5%"),
    ("$87.49", "BRENT CRUDE"),
    ("+1.8%", "SENSEX, INDIA"),
    ("259", "DEMOCRATS' HOUSE"),
    ("+36%", "BANGLADESH WAGE"),
]

LEADS = [
    {"kicker": "TECH \u00b7 SANTA CLARA", "color": NAVY,
     "scene": scene_nvidia,
     "head": "Nvidia slides 7% as lawmakers question Trump's role in Huang's return",
     "body": ("Shares fell after a rally on Huang's comeback faded. "
              "He told staff he broke conduct rules and is in therapy.")},
    {"kicker": "ENERGY \u00b7 STRAIT OF HORMUZ", "color": RED,
     "scene": scene_hormuz,
     "head": "Mines hit two tankers in the Strait of Hormuz, Iran's Guards say",
     "body": ("Brent holds at $87.49, down 21% over the month, as shipping "
              "fears rise and a swimmer crosses the strait.")},
    {"kicker": "MARKETS \u00b7 TOKYO", "color": (214, 96, 20),
     "scene": scene_selloff,
     "head": "Asia's AI sell-off deepens as doubts over the boom return",
     "body": ("Tokyo's Nikkei fell 2.76% and the S&P 500 slid 0.5% to "
              "7,201, while India's Sensex rose 1.8%.")},
]

CARDS = [
    {"kicker": "TECH", "color": RED, "scene": scene_microsoft,
     "head": "Microsoft's \u2018Code Red\u2019",
     "body": ("Memos reveal a 24-hour outage on 12\u201313 Nov, the worst "
              "in Exchange Online history.")},
    {"kicker": "SPACE", "color": NAVY, "scene": scene_shenzhou,
     "head": "China launches Shenzhou-24",
     "body": ("Pakistan's first astronaut reaches Tiangong, the first "
              "foreigner aboard China's station.")},
    {"kicker": "COLOMBIA", "color": (31, 122, 60), "scene": scene_cartagena,
     "head": "Hostage siege in Cartagena",
     "body": ("Gunmen seized a supermarket after a failed cash-truck "
              "robbery, holding about 20 shoppers.")},
    {"kicker": "SPORT", "color": (31, 122, 60), "scene": scene_senegal,
     "head": "Senegal regain AFCON crown",
     "body": ("The Lions of Teranga lift the Africa Cup of Nations title "
              "again in green, yellow and red.")},
    {"kicker": "PACIFIC", "color": TEAL, "scene": scene_solomon,
     "head": "Solomons pick Australia",
     "body": ("Honiara signs a treaty naming Australia its top partner, "
              "ruling out foreign bases. (AP)")},
    {"kicker": "USA", "color": NAVY, "scene": scene_house,
     "head": "Democrats take the House",
     "body": ("The party wins at least 259 seats in Washington, reshaping "
              "the balance of power.")},
    {"kicker": "SPAIN", "color": (176, 30, 36), "scene": scene_spain,
     "head": "Spain heads to snap polls",
     "body": ("Madrid calls an early election as the government gambles "
              "on a fresh mandate from voters.")},
    {"kicker": "TRADE", "color": (214, 96, 20), "scene": scene_tariffs,
     "head": "Trump readies new tariffs",
     "body": ("Duties planned on 16 partners after a probe into excess "
              "industrial capacity. (The Hindu)")},
    {"kicker": "BANGLADESH", "color": GREEN, "scene": scene_bangladesh,
     "head": "Garment workers win +36%",
     "body": ("Garment workers secure a 36% minimum-wage rise after months "
              "of talks with owners.")},
    {"kicker": "KOREA", "color": (96, 56, 140), "scene": scene_jets,
     "head": "Russian jets enter Korean ADIZ",
     "body": ("Seoul says Russian aircraft entered its air-defence zone "
              "\u2014 the latest test of nerves. (SRI)")},
]

INDEX = [
    (2, "China probes Shanghai party chief Chen Jining"),
    (4, "DR Congo plane missing; rebels claim downing"),
    (5, "Hong Kong marks a year since the Tai Po fire"),
    (4, "Zambia indicts opposition leader for treason"),
    (5, "Dozens trapped in Indonesian mine; rescue under way"),
    (4, "Khartoum drone strikes draw condemnation"),
    (3, "Iran flogs singer 74 times over unveiled concert"),
    (3, "Israel warns Iran is developing chemical weapons"),
    (3, "Israeli strikes in Gaza kill 7, incl. senior official"),
    (5, "N. Korea threatens to shut Swiss office in Pyongyang"),
    (2, "NATO vows space defence over Russian satellite"),
    (2, "Kyiv: Ukraine hit Russian ship in Gulf of Finland"),
    (6, "Tidal to ban fully AI-generated music"),
    (6, "Broadcom patches 23 VMware flaws, one critical"),
    (0, "\u00c1brego Garc\u00eda leaves US for Spain"),
    (0, "Pentagon criticises Canada's military spending"),
    (5, "S. Korea minister quits over exam-cheating scandal"),
    (5, "Sooryavanshi, 15, hits record 204 off 53 balls"),
]


# ================================================================ render
def render():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    f_title = font(SERIF, 44)
    f_sub = font(SANS_B, 13)
    f_dek = font(SERIF_I, 17)
    f_stat_n = font(SERIF, 21)
    f_stat_l = font(SANS_B, 10)
    f_tab = font(SANS_B, 11)
    f_kick = font(SANS_B, 10)
    f_head = font(SERIF, 17)
    f_body = font(SANS, 12)
    f_card_head = font(SERIF, 14)
    f_card_body = font(SANS, 11)
    f_idx_head = font(SANS_B, 12)
    f_idx = font(SANS, 12)
    f_foot = font(SANS, 11)

    # ---- masthead
    title = "THE WORLD IN ONE IMAGE"
    d.text(((W - d.textlength(title, font=f_title)) / 2, 8), title,
           font=f_title, fill=INK)
    sub = "WEDNESDAY, 25 NOVEMBER 2026  \u00b7  31 STORIES  \u00b7  7 REGIONS"
    d.text(((W - d.textlength(sub, font=f_sub)) / 2, 60), sub,
           font=f_sub, fill=GREY)
    d.line([(M, 82), (W - M, 82)], fill=INK, width=2)
    d.line([(M, 85), (W - M, 85)], fill=INK, width=1)

    # ---- red italic dek
    dek_lines = wrap(d, DEK, f_dek, CW)
    y = 92
    for ln in dek_lines:
        d.text(((W - d.textlength(ln, font=f_dek)) / 2, y), ln,
               font=f_dek, fill=RED)
        y += 22

    # ---- number strip
    y0 = 140
    bw = (CW - 6 * 6) // 7
    for i, (num, lab) in enumerate(STATS):
        x = M + i * (bw + 6)
        rounded_rect(d, [x, y0, x + bw, y0 + 44], 4,
                     fill=CARD_BG, outline=LINE)
        d.text((x + (bw - d.textlength(num, font=f_stat_n)) / 2, y0 + 2),
               num, font=f_stat_n, fill=RED)
        d.text((x + (bw - d.textlength(lab, font=f_stat_l)) / 2, y0 + 28),
               lab, font=f_stat_l, fill=GREY)

    # ---- region tabs
    y0 = 192
    for i, (name, col) in enumerate(REGION_COLORS):
        x = M + i * (bw + 6)
        rounded_rect(d, [x, y0, x + bw, y0 + 22], 4, fill=col)
        d.text((x + (bw - d.textlength(name, font=f_tab)) / 2, y0 + 4),
               name, font=f_tab, fill=(255, 255, 255))

    # ---- 3 leads
    y0 = 222
    lw = (CW - 2 * 10) // 3
    lh = 206
    for i, lead in enumerate(LEADS):
        x = M + i * (lw + 10)
        rounded_rect(d, [x, y0, x + lw, y0 + lh], 6,
                     fill=CARD_BG, outline=LINE)
        scene = lead["scene"](lw - 2, 118)
        img.paste(scene, (x + 1, y0 + 1))
        ty = y0 + 126
        d.text((x + 8, ty), lead["kicker"], font=f_kick, fill=lead["color"])
        ty += 15
        head_lines = wrap(d, lead["head"], f_head, lw - 16)
        ty = text_block(d, x + 8, ty, head_lines[:2], f_head, INK, 20)
        body_lines = wrap(d, lead["body"], f_body, lw - 16)
        text_block(d, x + 8, ty + 2, body_lines[:2], f_body, (60, 58, 52), 15)

    # ---- 10 cards, 2 rows of 5
    cw = (CW - 4 * 10) // 5
    ch = 172
    for row in range(2):
        y0 = 438 + row * (ch + 10)
        for col in range(5):
            card = CARDS[row * 5 + col]
            x = M + col * (cw + 10)
            rounded_rect(d, [x, y0, x + cw, y0 + ch], 6,
                         fill=CARD_BG, outline=LINE)
            scene = card["scene"](cw - 2, 86)
            img.paste(scene, (x + 1, y0 + 1))
            ty = y0 + 92
            d.text((x + 7, ty), card["kicker"], font=f_kick, fill=card["color"])
            ty += 14
            head_lines = wrap(d, card["head"], f_card_head, cw - 14)
            ty = text_block(d, x + 7, ty, head_lines[:2], f_card_head, INK, 16)
            body_lines = wrap(d, card["body"], f_card_body, cw - 14)
            text_block(d, x + 7, ty + 1, body_lines[:3], f_card_body,
                       (60, 58, 52), 13)

    # ---- bottom: map + index
    y0 = 800
    bh = 176
    map_w = 330
    rounded_rect(d, [M, y0, M + map_w, y0 + bh], 6,
                 fill=CARD_BG, outline=LINE)
    m = draw_world_map(map_w - 2, bh - 26)
    img.paste(m, (M + 1, y0 + 25))
    d.text((M + 8, y0 + 5), "WHERE IT HAPPENED", font=f_idx_head, fill=INK)
    d.text((M + 8, y0 + bh - 18), "Dots coloured by region \u2014 see tabs above",
           font=font(SANS_I, 10), fill=GREY)

    ix = M + map_w + 10
    iw = W - M - ix
    rounded_rect(d, [ix, y0, ix + iw, y0 + bh], 6,
                 fill=CARD_BG, outline=LINE)
    d.text((ix + 10, y0 + 5), "THE DAY IN BRIEF", font=f_idx_head, fill=INK)
    d.line([(ix + 10, y0 + 24), (ix + iw - 10, y0 + 24)], fill=LINE, width=1)
    col_w = (iw - 20) // 2
    for j, (reg, item) in enumerate(INDEX):
        cx = ix + 10 + (j // 9) * col_w
        cy = y0 + 30 + (j % 9) * 16
        col = REGION_COLORS[reg][1]
        d.ellipse([cx, cy + 4, cx + 7, cy + 11], fill=col)
        lines = wrap(d, item, f_idx, col_w - 14)
        d.text((cx + 11, cy), lines[0], font=f_idx, fill=INK)

    # ---- footer
    d.line([(M, 986), (W - M, 986)], fill=INK, width=1)
    foot = ("Sources: BBC \u00b7 The Guardian \u00b7 The Hindu \u00b7 Reuters \u00b7 AP "
            "\u00b7 OneTurn \u00b7 Newsof.today \u00b7 SRI \u2014 figures checked "
            "against live sources, 25 Nov 2026")
    d.text(((W - d.textlength(foot, font=f_foot)) / 2, 992), foot,
           font=f_foot, fill=GREY)
    foot2 = "make.fun/bounty/news-image-20261125"
    d.text(((W - d.textlength(foot2, font=f_foot)) / 2, 1008), foot2,
           font=f_foot, fill=GREY)
    return img


def main():
    out = os.environ.get("POSTER_OUT", "poster.png")
    poster = render()
    poster.save(out, format="PNG", optimize=True)
    print(f"wrote {out} {poster.size} "
          f"({os.path.getsize(out)} bytes)")


if __name__ == "__main__":
    main()
