"""Generate the site's social/icon images.

  og-image.png          homepage / section-page share card
  og/<slug>.png         one share card per blog post (title read from the post's og:title)
  apple-touch-icon.png  180x180 home-screen icon (matches favicon.svg)

Run from anywhere: python3 scripts/gen_og_image.py
"""
from pathlib import Path
import html
import re

from PIL import Image, ImageDraw, ImageFont, ImageFilter

ROOT = Path(__file__).resolve().parent.parent

W, H = 1200, 630

BG      = (12, 17, 23)
BG2     = (9, 13, 18)
INK     = (233, 238, 242)
INK_SOFT= (138, 154, 166)
SIGNAL  = (45, 212, 191)

def background():
    img = Image.new("RGB", (W, H), BG)

    # vertical gradient bg -> bg2
    grad = Image.new("L", (1, H))
    for y in range(H):
        t = y / H
        grad.putpixel((0, y), int(255 * (1 - t)))
    grad = grad.resize((W, H))
    bgtop = Image.new("RGB", (W, H), BG)
    bgbot = Image.new("RGB", (W, H), BG2)
    img = Image.composite(bgtop, bgbot, grad)

    # radial teal glow, top-right (matches site's body background)
    glow = Image.new("L", (W, H), 0)
    gd = ImageDraw.Draw(glow)
    cx, cy = int(W * 0.78), int(H * -0.05)
    max_r = 620
    for r in range(max_r, 0, -4):
        alpha = int(70 * (1 - r / max_r) ** 1.6)
        gd.ellipse([cx - r, cy - r, cx + r, cy + r], fill=alpha)
    glow = glow.filter(ImageFilter.GaussianBlur(40))
    teal_layer = Image.new("RGB", (W, H), SIGNAL)
    img = Image.composite(teal_layer, img, glow)

    # subtle dot grid
    dots = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    dd = ImageDraw.Draw(dots)
    step = 22
    for x in range(0, W, step):
        for y in range(0, H, step):
            dd.ellipse([x, y, x + 1, y + 1], fill=(255, 255, 255, 13))
    img = img.convert("RGBA")
    img.alpha_composite(dots)
    img = img.convert("RGB")
    return img


display_font = ImageFont.truetype("/System/Library/Fonts/Supplemental/Georgia.ttf", 92)
title_font   = ImageFont.truetype("/System/Library/Fonts/Supplemental/Georgia.ttf", 68)
mono_font    = ImageFont.truetype("/System/Library/Fonts/Menlo.ttc", 28)
mono_small   = ImageFont.truetype("/System/Library/Fonts/Menlo.ttc", 22)

margin = 96
KICKER = "PRUTHVIRAJDESAI.QZZ.IO"


def footer(draw, text):
    # status dot + mono caption, like the site footer
    dot_r = 6
    dot_cx, dot_cy = margin + dot_r, 560
    draw.ellipse([dot_cx - dot_r, dot_cy - dot_r, dot_cx + dot_r, dot_cy + dot_r], fill=SIGNAL)
    draw.text((margin + 22, 548), text, font=mono_small, fill=INK_SOFT)


def home_card():
    img = background()
    draw = ImageDraw.Draw(img)
    draw.text((margin, 150), KICKER, font=mono_small, fill=SIGNAL)
    draw.text((margin, 210), "Pruthviraj", font=display_font, fill=INK)
    draw.text((margin, 210 + 100), "Desai", font=display_font, fill=INK_SOFT)
    draw.text((margin, 460), "MBA candidate · product, data & AI", font=mono_font, fill=SIGNAL)
    footer(draw, "Cambridge Judge Business School")
    return img


def wrap(draw, text, font, width):
    lines, line = [], ""
    for word in text.split():
        trial = f"{line} {word}".strip()
        if draw.textlength(trial, font=font) <= width or not line:
            line = trial
        else:
            lines.append(line)
            line = word
    lines.append(line)
    return lines


def post_card(title, meta):
    img = background()
    draw = ImageDraw.Draw(img)
    draw.text((margin, 120), KICKER + "  /  WRITING", font=mono_small, fill=SIGNAL)
    lines = wrap(draw, title, title_font, W - 2 * margin)[:4]
    y = 180
    for line in lines:
        draw.text((margin, y), line, font=title_font, fill=INK)
        y += 82
    draw.text((margin, y + 20), meta, font=mono_font, fill=SIGNAL)
    footer(draw, "Pruthviraj Desai")
    return img


def touch_icon():
    # mirrors favicon.svg: dark rounded square, faint teal border, serif "P"
    S, scale = 180, 4
    big = S * scale
    img = Image.new("RGB", (big, big), BG)  # iOS applies its own rounding mask
    d = ImageDraw.Draw(img)
    d.rounded_rectangle([0, 0, big - 1, big - 1], radius=int(big * 7 / 32),
                        outline=(22, 75, 72), width=int(big * 1.5 / 32))
    font = ImageFont.truetype("/System/Library/Fonts/Supplemental/Georgia Bold.ttf", int(big * 21 / 32))
    d.text((big / 2, big * 23 / 32), "P", font=font, fill=SIGNAL, anchor="ms")
    return img.resize((S, S), Image.LANCZOS)


def meta(page, prop):
    m = re.search(rf'<meta property="{prop}" content="([^"]*)"', page)
    return html.unescape(m.group(1)) if m else ""


if __name__ == "__main__":
    home_card().save(ROOT / "og-image.png", "PNG", optimize=True)

    (ROOT / "og").mkdir(exist_ok=True)
    for post in sorted((ROOT / "blog").glob("*.html")):
        page = post.read_text()
        title = meta(page, "og:title")
        date = re.search(r'<time datetime="[^"]*">([^<]*)</time>', page).group(1)
        tags = re.findall(r'<span class="post-tag">([^<]*)</span>', page)
        post_card(title, " · ".join([date] + tags)).save(ROOT / "og" / f"{post.stem}.png", "PNG", optimize=True)

    touch_icon().save(ROOT / "apple-touch-icon.png", "PNG", optimize=True)
    print("saved og-image.png, og/*.png, apple-touch-icon.png")
