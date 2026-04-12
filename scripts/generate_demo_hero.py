#!/usr/bin/env python3
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "docs" / "demo-hero.png"

W, H = 1600, 900
BG = "#F4F7FB"
PANEL = "#FFFFFF"
BORDER = "#D7E0EA"
SLATE = "#10243E"
SUB = "#5B718A"
INDIGO = "#4F46E5"
CYAN = "#06B6D4"
AMBER = "#F59E0B"
GREEN = "#16A34A"


def find_font(candidates):
    for path in candidates:
        if Path(path).exists():
            return path
    raise FileNotFoundError(f"missing font: {candidates}")


FONT_PATH = find_font(
    [
        # macOS
        "/System/Library/Fonts/Supplemental/Arial Unicode.ttf",
        "/System/Library/Fonts/Supplemental/Arial.ttf",
        "/Library/Fonts/Arial.ttf",
        # Linux
        "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        # Windows
        "C:/Windows/Fonts/arial.ttf",
    ]
)
BOLD_PATH = find_font(
    [
        # macOS
        "/System/Library/Fonts/Supplemental/Arial Bold.ttf",
        "/Library/Fonts/Arial Bold.ttf",
        # Linux
        "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
        # Windows
        "C:/Windows/Fonts/arialbd.ttf",
        FONT_PATH,
    ]
)


def font(size, bold=False):
    return ImageFont.truetype(BOLD_PATH if bold else FONT_PATH, size)


def wrap_text(draw, text, fnt, max_width):
    words = text.split()
    lines = []
    current = words[0]
    for word in words[1:]:
        probe = f"{current} {word}"
        if draw.textbbox((0, 0), probe, font=fnt)[2] <= max_width:
            current = probe
        else:
            lines.append(current)
            current = word
    lines.append(current)
    return lines


def draw_wrapped(draw, xy, text, fnt, fill, max_width, line_gap=8):
    x, y = xy
    lines = wrap_text(draw, text, fnt, max_width)
    for line in lines:
        draw.text((x, y), line, font=fnt, fill=fill)
        box = draw.textbbox((x, y), line, font=fnt)
        y += (box[3] - box[1]) + line_gap
    return y


def centered_text(draw, box, text, fnt, fill):
    x1, y1, x2, y2 = box
    bbox = draw.textbbox((0, 0), text, font=fnt)
    tw = bbox[2] - bbox[0]
    th = bbox[3] - bbox[1]
    draw.text((x1 + (x2 - x1 - tw) / 2, y1 + (y2 - y1 - th) / 2), text, font=fnt, fill=fill)


img = Image.new("RGB", (W, H), BG)
draw = ImageDraw.Draw(img)

# Background accents
draw.ellipse((-260, -220, 780, 980), fill=INDIGO)
draw.polygon([(980, 0), (1600, 0), (1600, 900), (780, 900), (1080, 500)], fill=CYAN)
draw.rectangle((680, 0, 980, 900), fill=BG)

# Hero band
hero = (70, 60, W - 70, 300)
draw.rounded_rectangle(hero, radius=34, fill="#0F172A")
for x in range(0, 260, 18):
    draw.rounded_rectangle((W - 360 + x, 85, W - 348 + x, 132), radius=6, fill=(255, 255, 255))

draw.text((120, 98), "AI OS Framework", font=font(22, bold=True), fill="#93C5FD")
title_font = font(54, bold=True)
subtitle_font = font(26)
title_lines = wrap_text(
    draw,
    "Build a control plane that executives can actually operate.",
    title_font,
    1120,
)
title_y = 138
for line in title_lines:
    draw.text((120, title_y), line, font=title_font, fill="white")
    title_y += 62
draw.text(
    (120, title_y + 6),
    "Contracts, subsystem boundaries, War Room visibility, and recovery-aware operations.",
    font=subtitle_font,
    fill="#D7E7FF",
)

# Left card
left = (90, 350, 760, 815)
draw.rounded_rectangle(left, radius=28, fill=PANEL, outline=BORDER, width=2)
draw.text((120, 382), "Architecture at a glance", font=font(30, bold=True), fill=SLATE)
draw.text(
    (120, 428),
    "One control plane. Multiple domain subsystems. One operator surface.",
    font=font(20),
    fill=SUB,
)

# Architecture nodes
control = (157, 480, 453, 555)
draw.rounded_rectangle(control, radius=22, fill=INDIGO)
centered_text(draw, (157, 494, 453, 520), "Control Plane", font(24, bold=True), "white")
centered_text(draw, (157, 522, 453, 545), "governance / contracts / health", font(17), "#E0E7FF")

runtime = (120, 604, 490, 683)
draw.rounded_rectangle(runtime, radius=22, fill="#EFF6FF", outline="#BFDBFE", width=2)
centered_text(draw, (120, 618, 490, 645), "Runtime Aggregation", font(22, bold=True), SLATE)
centered_text(draw, (120, 648, 490, 670), "M07 / M08 / health / actions", font(17), SUB)

draw.line((305, 555, 305, 604), fill="#94A3B8", width=5)
draw.line((305, 683, 305, 718), fill="#94A3B8", width=5)

sub_boxes = [
    ("Trading", "#FEF3C7", "#D97706"),
    ("CRM", "#ECFEFF", "#0891B2"),
    ("Email", "#ECFEFF", "#0891B2"),
    ("Knowledge", "#F3E8FF", "#7C3AED"),
    ("Twin", "#FCE7F3", "#DB2777"),
]
sx = 120
for label, fill, fg in sub_boxes:
    box = (sx, 732, sx + 90, 786)
    draw.rounded_rectangle(box, radius=16, fill=fill, outline="#D8DEE9")
    centered_text(draw, box, label, font(16, bold=False), fg)
    sx += 102

war_room = (130, 792, 480, 848)
draw.rounded_rectangle(war_room, radius=18, fill="#DCFCE7", outline="#86EFAC", width=2)
centered_text(draw, war_room, "War Room / Operator View", font(20, bold=True), "#166534")

# Right card
right = (810, 350, 1510, 815)
draw.rounded_rectangle(right, radius=28, fill=PANEL, outline=BORDER, width=2)
draw.text((840, 382), "Executive outcome", font=font(30, bold=True), fill=SLATE)
draw_wrapped(
    draw,
    (840, 428),
    "The point is not more agents. The point is a system that stays legible under pressure.",
    font(19),
    SUB,
    610,
    line_gap=6,
)

metric_specs = [
    ((840, 500, 1070, 642), INDIGO, None, "white", "Now", "3", "top priorities"),
    ((1092, 500, 1322, 642), "#FFF7ED", "#FED7AA", "#9A3412", "Risk", "2", "cross-system blockers"),
    ((1344, 500, 1478, 642), "#ECFDF5", "#A7F3D0", "#166534", "Health", "Ready", "recoverable controls"),
]
for box, fill, outline, text_fill, label, big, small in metric_specs:
    draw.rounded_rectangle(box, radius=20, fill=fill, outline=outline or fill, width=2 if outline else 0)
    x1, y1, x2, y2 = box
    draw.text((x1 + 18, y1 + 14), label, font=font(20, bold=True), fill=text_fill)
    big_font = font(56, bold=True) if len(big) <= 3 else font(44, bold=True)
    draw.text((x1 + 18, y1 + 48), big, font=big_font, fill=text_fill)
    small_y = y2 - 28 if len(big) <= 3 else y2 - 32
    draw.text((x1 + 18, small_y), small, font=font(15), fill=text_fill if fill == INDIGO else SUB)

notice = (840, 658, 1480, 828)
draw.rounded_rectangle(notice, radius=22, fill="#F8FAFC", outline=BORDER, width=2)
draw.text((868, 694), "What managers should notice", font=font(19, bold=True), fill=SLATE)
items = [
    "Control plane owns visibility.",
    "Subsystems evolve without losing coherence.",
]
iy = 726
for idx, item in enumerate(items, start=1):
    bubble = (872, iy, 902, iy + 30)
    draw.rounded_rectangle(bubble, radius=12, fill="#E0E7FF")
    centered_text(draw, bubble, str(idx), font(16, bold=True), INDIGO)
    draw.text((918, iy + 7), item, font=font(15), fill=SUB)
    iy += 40

footer = "Open-source starter for control-plane architecture, contract-first subsystems, and War Room operations."
fw = draw.textbbox((0, 0), footer, font=font(18))[2]
draw.text(((W - fw) / 2, 878), footer, font=font(18), fill="#334155")

OUT.parent.mkdir(parents=True, exist_ok=True)
img.save(OUT)
print(OUT)
