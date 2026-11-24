#!/usr/bin/env python3
"""Draw the entry image for make.fun competition news-image-20261124.

A 1024x1024 newspaper front page, "THE WORLD TODAY — TUESDAY
24 NOVEMBER 2026", summing up the day's world news as reported on
24 November 2026 (Reuters, BBC, CNN, The Guardian, Al Jazeera).
Vector art only: every picture is drawn with Pillow primitives,
no photographs, no network. Run: python3 compose.py
(writes entry.png next to this file).
"""
import math

from PIL import Image, ImageDraw, ImageFont

W = H = 1024
PAPER = (247, 243, 234)
INK = (20, 20, 20)
MUTED = (90, 86, 78)
RED = (176, 30, 36)
BLUE = (29, 78, 137)
GREEN = (31, 110, 72)
GOLD = (184, 134, 11)
SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def f(path, size):
    return ImageFont.truetype(path, size)


def wrap(d, text, font, max_w):
    """Greedy word wrap; returns a list of lines that fit max_w."""
    lines, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if d.textlength(trial, font=font) <= max_w or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def para(d, text, font, x, y, max_w, fill=INK, leading=None):
    """Draw a wrapped paragraph; returns y just below the last line."""
    if leading is None:
        leading = int(font.size * 1.32)
    for line in wrap(d, text, font, max_w):
        d.text((x, y), line, font=font, fill=fill)
        y += leading
    return y


def kicker(d, x, y, text, fill=RED, size=15):
    d.text((x, y), text.upper(), font=f(SANS_B, size), fill=fill)
    return y + size + 8


def rule(d, x0, y, x1, width=2, fill=INK):
    d.line([(x0, y), (x1, y)], fill=fill, width=width)


def chip(d, x0, y0, s):
    """A green computer chip, for the Nvidia lead story."""
    d.rounded_rectangle([x0, y0, x0 + s, y0 + s], radius=s // 8,
                        fill=GREEN, outline=INK, width=3)
    for i in range(4):
        t = y0 + s * (0.22 + i * 0.18)
        d.line([(x0 - 12, t), (x0, t)], fill=INK, width=4)
        d.line([(x0 + s, t), (x0 + s + 12, t)], fill=INK, width=4)
        t2 = x0 + s * (0.22 + i * 0.18)
        d.line([(t2, y0 - 12), (t2, y0)], fill=INK, width=4)
        d.line([(t2, y0 + s), (t2, y0 + s + 12)], fill=INK, width=4)
    inner = s // 2
    d.rectangle([x0 + (s - inner) // 2, y0 + (s - inner) // 2,
                 x0 + (s + inner) // 2, y0 + (s + inner) // 2],
                fill=PAPER, outline=INK, width=2)
    d.text((x0 + s // 2, y0 + s // 2 - 13), "NVDA",
           font=f(SANS_B, 20), fill=GREEN, anchor="mm")


def radar(d, x0, y0, s):
    """A radar screen with a drone blip, for the Poland story."""
    cx, cy, r = x0 + s // 2, y0 + s // 2, s // 2
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=BLUE, width=3)
    d.ellipse([cx - r * 0.6, cy - r * 0.6, cx + r * 0.6, cy + r * 0.6],
              outline=BLUE, width=2)
    d.line([(cx - r, cy), (cx + r, cy)], fill=BLUE, width=2)
    d.line([(cx, cy - r), (cx, cy + r)], fill=BLUE, width=2)
    d.line([(cx, cy), (cx + r * 0.7, cy - r * 0.7)], fill=RED, width=3)
    bx, by = cx + r * 0.45, cy - r * 0.45
    d.ellipse([bx - 7, by - 7, bx + 7, by + 7], fill=RED)
    d.rectangle([cx - 26, cy + 12, cx + 26, cy + 24], fill=INK)
    d.line([(cx - 34, cy + 12), (cx - 34, cy + 4)], fill=INK, width=3)
    d.line([(cx + 34, cy + 12), (cx + 34, cy + 4)], fill=INK, width=3)


def tanker(d, x0, y0, s):
    """An oil tanker on waves with a naval mine, for the Gulf story."""
    d.rectangle([x0, y0 + s * 0.55, x0 + s, y0 + s * 0.72], fill=INK)
    d.polygon([(x0, y0 + s * 0.55), (x0 + s * 0.12, y0 + s * 0.42),
               (x0 + s * 0.3, y0 + s * 0.55)], fill=INK)
    for i, col in enumerate((RED, GOLD, BLUE)):
        d.rectangle([x0 + s * (0.34 + i * 0.2), y0 + s * 0.34,
                     x0 + s * (0.5 + i * 0.2), y0 + s * 0.55],
                    fill=col, outline=INK, width=2)
    d.rectangle([x0 + s * 0.78, y0 + s * 0.28, x0 + s * 0.9, y0 + s * 0.55],
                fill=PAPER, outline=INK, width=2)
    mx, my, mr = x0 + s * 0.82, y0 + s * 0.12, 11
    d.ellipse([mx - mr, my - mr, mx + mr, my + mr], fill=INK)
    for a in range(0, 360, 45):
        x1 = mx + (mr + 2) * math.cos(math.radians(a))
        y1 = my + (mr + 2) * math.sin(math.radians(a))
        x2 = mx + (mr + 8) * math.cos(math.radians(a))
        y2 = my + (mr + 8) * math.sin(math.radians(a))
        d.line([(x1, y1), (x2, y2)], fill=INK, width=3)
    for i in range(3):
        yy = y0 + s * (0.8 + i * 0.07)
        d.arc([x0, yy - 8, x0 + s, yy + 8], 0, 180, fill=BLUE, width=3)


def globe(d, x0, y0, s):
    """A cracked globe, for the COP31 story."""
    cx, cy, r = x0 + s // 2, y0 + s // 2, s // 2
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=GREEN, width=3)
    d.ellipse([cx - r * 0.55, cy - r, cx + r * 0.55, cy + r],
              outline=GREEN, width=2)
    d.line([(cx - r, cy), (cx + r, cy)], fill=GREEN, width=2)
    d.arc([cx - r, cy - r * 0.45, cx + r, cy + r * 0.45], 0, 180,
          fill=GREEN, width=2)
    d.arc([cx - r, cy - r * 0.45, cx + r, cy + r * 0.45], 180, 360,
          fill=GREEN, width=2)
    crack = [(cx - 6, cy - r), (cx + 8, cy - r * 0.4), (cx - 10, cy),
             (cx + 6, cy + r * 0.4), (cx - 4, cy + r * 0.8), (cx + 2, cy + r)]
    d.line(crack, fill=RED, width=4, joint="curve")


def warship(d, x0, y0, s):
    """A warship listing to one side, for the Benghazi story."""
    d.polygon([(x0, y0 + s * 0.55), (x0 + s, y0 + s * 0.62),
               (x0 + s * 0.92, y0 + s * 0.78), (x0 + s * 0.1, y0 + s * 0.72)],
              fill=INK)
    d.rectangle([x0 + s * 0.3, y0 + s * 0.34, x0 + s * 0.55, y0 + s * 0.55],
                fill=INK)
    d.line([(x0 + s * 0.62, y0 + s * 0.55), (x0 + s * 0.62, y0 + s * 0.2)],
           fill=INK, width=4)
    d.line([(x0 + s * 0.62, y0 + s * 0.2), (x0 + s * 0.78, y0 + s * 0.3)],
           fill=RED, width=4)
    for i in range(3):
        yy = y0 + s * (0.82 + i * 0.06)
        d.arc([x0, yy - 7, x0 + s, yy + 7], 0, 180, fill=BLUE, width=3)


def column_story(d, x, y, col_w, tag, head, deck, icon):
    """One two-column story: kicker, headline left + icon right, deck below.

    Returns the y just below the deck.
    """
    y = kicker(d, x, y, tag, size=15)
    head_end = para(d, head, f(SERIF, 28), x, y, col_w - 132, leading=33)
    icon(d, x + col_w - 106, y - 6, 100)
    deck_top = max(head_end, y + 102) + 6
    return para(d, deck, f(SANS, 18), x, deck_top, col_w)


def build():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    mx = 36
    rx = W - mx

    # ---- masthead ----
    d.text((W // 2, 30), "THE WORLD TODAY", font=f(SERIF, 66),
           fill=INK, anchor="ma")
    rule(d, mx, 112, rx, 3)
    d.text((mx, 122), "TUESDAY 24 NOVEMBER 2026",
           font=f(SANS_B, 21), fill=RED)
    d.text((rx, 122), "ONE DAY · ONE PAGE", font=f(SANS_B, 21),
           fill=MUTED, anchor="ra")
    rule(d, mx, 152, rx, 2)

    # ---- lead: Nvidia ----
    y = kicker(d, mx, 168, "Lead — Washington · Santa Clara", size=17)
    y = para(d, "Trump brings Huang back to Nvidia", f(SERIF, 48),
             mx, y, 640, leading=54)
    y = para(d, "Board reinstates the ousted chief after a White House "
                "pressure campaign led by Vice-President Vance.",
             f(SANS, 19), mx, y + 6, 640)
    y = para(d, "NVDA +33%; Nasdaq +6%. Huang testifies to the Senate "
                "on 3 December.", f(SANS, 17), mx, y + 4, 640,
             fill=MUTED)
    chip(d, 806, 182, 148)
    d.text((880, 342), "NVDA +33%", font=f(SANS_B, 20), fill=GREEN,
           anchor="ma")
    rule(d, mx, 390, rx, 2)

    # ---- row 2: Poland + Hormuz ----
    col_w = 464
    end_l = column_story(
        d, mx, 408, col_w, "Poland — NATO's eastern flank",
        "Russian drone strays into Poland",
        "Air defences on alert overnight as a drone crosses near "
        "Dorohusk; Warsaw holds fire after it turns back east. "
        "NATO to send an AWACS early-warning plane.", radar)
    end_r = column_story(
        d, 524, 408, col_w, "The Gulf — Iran",
        "Iran warns EU bases are in range",
        "Tehran says its missiles can hit targets 4,500 km away. "
        "Trump warns of a “very traumatic” outcome if the nuclear "
        "deal fails; a second US carrier is weighed.", tanker)
    rule(d, mx, max(end_l, end_r) + 14, rx, 2)

    # ---- row 3: COP31 + Benghazi ----
    y3 = max(end_l, end_r) + 32
    end_l = column_story(
        d, mx, y3, col_w, "Antalya — after the collapse",
        "COP31 is dead. What now?",
        "First climate summit to fail since 2009: some 130 nations "
        "rejected a deal with no fossil-fuel language. The world "
        "is on track for 2.8°C of warming.", globe)
    end_r = column_story(
        d, 524, y3, col_w, "Libya — the war at sea",
        "Libya condemns strike on Russian ships",
        "Corvette Merkury capsized in Benghazi port after a "
        "suspected Ukrainian sea-drone attack; Moscow says "
        "Russians were killed in the blast.", warship)
    rule(d, mx, max(end_l, end_r) + 12, rx, 2)

    # ---- minis ----
    y4 = max(end_l, end_r) + 28
    minis = [
        ("INDIA–NEPAL", "$1.6bn flood aid as Nepal's PM visits Modi"),
        ("CIKANDE, INDONESIA", "Rescue goes on after factory fire"),
        ("SOUTH AFRICA", "Voters test the ANC as polls open"),
        ("CRICKET", "India–New Zealand Test ends in a draw"),
    ]
    x = mx
    for tag, text in minis:
        d.text((x, y4), tag, font=f(SANS_B, 14), fill=RED)
        para(d, text, f(SANS, 15), x, y4 + 20, 220, leading=19)
        x += 242
    y5 = y4 + 62
    rule(d, mx, y5, rx, 1)
    d.text((mx, y5 + 10), "ALSO: WHO hails India's 10m HPV jabs · "
           "Thai–Cambodia truce holds · NATO vows space defence · "
           "Bangladesh vaccinates 50m children",
           font=f(SANS, 14), fill=MUTED)
    d.text((W // 2, 1002),
           "Drawn in code · Sources: Reuters, BBC, CNN, The Guardian, "
           "Al Jazeera", font=f(SANS, 13), fill=MUTED, anchor="ma")

    img.save("entry.png", optimize=True)
    print("wrote entry.png")


if __name__ == "__main__":
    build()
