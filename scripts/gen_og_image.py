from PIL import Image, ImageDraw, ImageFont, ImageFilter
import math

W, H = 1200, 630

BG      = (12, 17, 23)
BG2     = (9, 13, 18)
INK     = (233, 238, 242)
INK_SOFT= (138, 154, 166)
SIGNAL  = (45, 212, 191)

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

draw = ImageDraw.Draw(img)

display_font = ImageFont.truetype("/System/Library/Fonts/Supplemental/Georgia.ttf", 92)
mono_font    = ImageFont.truetype("/System/Library/Fonts/Menlo.ttc", 28)
mono_small   = ImageFont.truetype("/System/Library/Fonts/Menlo.ttc", 22)

margin = 96

# small kicker line (mono, teal, like .eyebrow)
kicker = "PRUTHVIRAJDESAI.QZZ.IO"
draw.text((margin, 150), kicker, font=mono_small, fill=SIGNAL)

# name (serif display, like h1)
draw.text((margin, 210), "Pruthviraj", font=display_font, fill=INK)
draw.text((margin, 210 + 100), "Desai", font=display_font, fill=INK_SOFT)

# tagline (mono, teal, like .tagline)
tagline = "MBA candidate · product, data & AI"
draw.text((margin, 460), tagline, font=mono_font, fill=SIGNAL)

# bottom hairline + status dot, like footer/status dot
dot_r = 6
dot_cx, dot_cy = margin + dot_r, 560
draw.ellipse([dot_cx - dot_r, dot_cy - dot_r, dot_cx + dot_r, dot_cy + dot_r], fill=SIGNAL)
draw.text((margin + 22, 548), "Cambridge Judge Business School", font=mono_small, fill=INK_SOFT)

img.save("/Users/pruthviraj/FUN/website/og-image.png", "PNG", optimize=True)
print("saved", img.size)
