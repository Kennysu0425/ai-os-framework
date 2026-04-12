#!/usr/bin/env python3
from pathlib import Path

try:
    from PIL import Image, ImageDraw, ImageFont
except ImportError:
    raise SystemExit(
        "Pillow is required for image generation.\n"
        "Install it with: pip install -r requirements-images.txt"
    )


ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
WARM_ROOM_PNG = DOCS / "war-room-demo.png"
SOCIAL_PNG = DOCS / "social-preview.png"


def find_font(candidates):
    for path in candidates:
        if Path(path).exists():
            return path
    raise FileNotFoundError(f"missing font from {candidates}")


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


def centered(draw, box, text, fnt, fill):
    x1, y1, x2, y2 = box
    bb = draw.textbbox((0, 0), text, font=fnt)
    tw = bb[2] - bb[0]
    th = bb[3] - bb[1]
    draw.text((x1 + (x2 - x1 - tw) / 2, y1 + (y2 - y1 - th) / 2), text, font=fnt, fill=fill)


def wrap(draw, text, fnt, width):
    words = text.split()
    lines = []
    cur = words[0]
    for word in words[1:]:
        probe = f"{cur} {word}"
        if draw.textbbox((0, 0), probe, font=fnt)[2] <= width:
            cur = probe
        else:
            lines.append(cur)
            cur = word
    lines.append(cur)
    return lines


def draw_wrapped(draw, xy, text, fnt, fill, width, gap=6):
    x, y = xy
    for line in wrap(draw, text, fnt, width):
        draw.text((x, y), line, font=fnt, fill=fill)
        bb = draw.textbbox((x, y), line, font=fnt)
        y += (bb[3] - bb[1]) + gap
    return y


def build_war_room_demo():
    W, H = 1600, 980
    img = Image.new("RGB", (W, H), "#F4F7FB")
    d = ImageDraw.Draw(img)

    # background
    d.ellipse((-240, -140, 560, 620), fill="#E0E7FF")
    d.ellipse((1120, -120, 1760, 520), fill="#CFFAFE")

    # top window chrome
    main = (70, 60, W - 70, H - 60)
    d.rounded_rectangle(main, radius=28, fill="#FFFFFF", outline="#D9E2EC", width=2)
    d.rounded_rectangle((70, 60, W - 70, 126), radius=28, fill="#FFFFFF", outline="#D9E2EC", width=2)
    d.rectangle((70, 92, W - 70, 126), fill="#FFFFFF")
    for i, c in enumerate(["#FB7185", "#F59E0B", "#10B981"]):
        d.ellipse((96 + i * 24, 85, 112 + i * 24, 101), fill=c)
    d.text((146, 78), "AI OS Framework Demo War Room", font=font(22, bold=True), fill="#102A43")
    d.text((1150, 78), "operator-facing control plane", font=font(16), fill="#64748B")

    # hero
    hero = (110, 160, 1490, 270)
    d.rounded_rectangle(hero, radius=24, fill="#EEF2FF", outline="#C7D2FE", width=2)
    d.text((140, 190), "Executive view", font=font(18, bold=True), fill="#4F46E5")
    d.text((140, 220), "A minimal operator surface that turns subsystem contracts into priorities, risks, and next actions.", font=font(26, bold=True), fill="#102A43")

    # metrics
    metrics = [
        ((110, 310, 425, 440), "#FFFFFF", "#D9E2EC", "Overall Status", "warning", "#D97706"),
        ((445, 310, 760, 440), "#FFFFFF", "#D9E2EC", "Top Priorities", "1", "#4F46E5"),
        ((780, 310, 1095, 440), "#FFFFFF", "#D9E2EC", "Top Risks", "2", "#DC2626"),
        ((1115, 310, 1430, 440), "#FFFFFF", "#D9E2EC", "Agents", "3", "#0F766E"),
    ]
    for box, fill, outline, label, value, value_color in metrics:
        d.rounded_rectangle(box, radius=22, fill=fill, outline=outline, width=2)
        x1, y1, x2, y2 = box
        d.text((x1 + 20, y1 + 20), label, font=font(18), fill="#64748B")
        d.text((x1 + 20, y1 + 56), value, font=font(44, bold=True), fill=value_color)

    # main content columns
    left = (110, 470, 880, 860)
    right = (910, 470, 1490, 860)
    d.rounded_rectangle(left, radius=24, fill="#FFFFFF", outline="#D9E2EC", width=2)
    d.rounded_rectangle(right, radius=24, fill="#FFFFFF", outline="#D9E2EC", width=2)

    # executive reading
    d.text((140, 504), "Executive Reading", font=font(28, bold=True), fill="#102A43")
    d.text((140, 556), "Top Priorities", font=font(20, bold=True), fill="#334155")
    prios = ["Review subsystem warnings"]
    y = 592
    for item in prios:
        d.rounded_rectangle((144, y + 8, 154, y + 18), radius=3, fill="#4F46E5")
        d.text((168, y), item, font=font(19), fill="#475569")
        y += 36
    d.text((140, 652), "Top Risks", font=font(20, bold=True), fill="#334155")
    risks = ["Queue pressure in email", "Trading instability"]
    y = 688
    for item in risks:
        d.rounded_rectangle((144, y + 8, 154, y + 18), radius=3, fill="#DC2626")
        d.text((168, y), item, font=font(19), fill="#475569")
        y += 36
    d.text((140, 774), "Top Actions", font=font(20, bold=True), fill="#334155")
    acts = ["Review priority replies", "Review trading readiness"]
    y = 810
    for item in acts:
        d.rounded_rectangle((144, y + 8, 154, y + 18), radius=3, fill="#0F766E")
        d.text((168, y), item, font=font(19), fill="#475569")
        y += 36

    # right: health + agents
    d.text((940, 504), "Control Plane Health", font=font(28, bold=True), fill="#102A43")
    health_boxes = [
        ((940, 552, 1200, 640), "#ECFDF5", "#A7F3D0", "telegram", "healthy", "#166534"),
        ((1220, 552, 1460, 640), "#ECFDF5", "#A7F3D0", "scheduler", "healthy", "#166534"),
    ]
    for box, fill, outline, label, val, fg in health_boxes:
        d.rounded_rectangle(box, radius=20, fill=fill, outline=outline, width=2)
        x1, y1, x2, y2 = box
        d.text((x1 + 18, y1 + 16), label, font=font(18, bold=True), fill=fg)
        d.text((x1 + 18, y1 + 42), val, font=font(28, bold=True), fill=fg)

    d.text((940, 682), "Subsystem Agents", font=font(24, bold=True), fill="#102A43")
    agent_cards = [
        ((940, 726, 1210, 838), "#FFF7ED", "#FED7AA", "Trading", "warning", "BTC intraday monitor is active"),
        ((1228, 726, 1490, 838), "#F0FDF4", "#BBF7D0", "Knowledge", "ready", "3 high-signal items promoted"),
    ]
    for box, fill, outline, title, stat, line in agent_cards:
        d.rounded_rectangle(box, radius=18, fill=fill, outline=outline, width=2)
        x1, y1, x2, y2 = box
        d.text((x1 + 18, y1 + 16), title, font=font(20, bold=True), fill="#102A43")
        d.text((x1 + 18, y1 + 46), stat, font=font(18, bold=True), fill="#92400E" if stat == "warning" else "#166534")
        draw_wrapped(d, (x1 + 18, y1 + 74), line, font(16), "#64748B", x2 - x1 - 36, 4)

    footer = "Thin contracts in. Executive reading out."
    fw = d.textbbox((0, 0), footer, font=font(20, bold=True))[2]
    d.text(((W - fw) / 2, 902), footer, font=font(20, bold=True), fill="#475569")

    DOCS.mkdir(parents=True, exist_ok=True)
    img.save(WARM_ROOM_PNG)


def build_social_preview():
    W, H = 1280, 640
    img = Image.new("RGB", (W, H), "#0F172A")
    d = ImageDraw.Draw(img)
    d.ellipse((-180, -120, 500, 560), fill="#4338CA")
    d.ellipse((920, -140, 1420, 380), fill="#0891B2")

    # main glass panel
    panel = (60, 54, 1220, 586)
    d.rounded_rectangle(panel, radius=36, fill="#FFFFFF", outline="#D9E2EC", width=2)
    d.rounded_rectangle((60, 54, 1220, 194), radius=36, fill="#111827")
    d.rectangle((60, 140, 1220, 194), fill="#111827")

    d.text((98, 92), "AI OS Framework", font=font(20, bold=True), fill="#93C5FD")
    d.text((98, 124), "Control plane architecture for AI subsystems.", font=font(42, bold=True), fill="white")

    d.text((100, 234), "What it gives you", font=font(18, bold=True), fill="#4F46E5")
    bullets = [
        "One control plane",
        "Contract-first subsystem integration",
        "War Room visibility for operators and executives",
        "Health, recovery, and observability built in",
    ]
    y = 272
    for item in bullets:
        d.rounded_rectangle((104, y + 7, 116, y + 19), radius=4, fill="#4F46E5")
        d.text((130, y), item, font=font(24), fill="#102A43")
        y += 48

    # right visual cluster
    card1 = (760, 236, 1128, 474)
    d.rounded_rectangle(card1, radius=26, fill="#F8FAFC", outline="#D9E2EC", width=2)
    d.text((790, 266), "War Room", font=font(22, bold=True), fill="#102A43")
    d.rounded_rectangle((790, 314, 948, 396), radius=18, fill="#EEF2FF", outline="#C7D2FE", width=2)
    d.text((810, 334), "Priorities", font=font(18, bold=True), fill="#4F46E5")
    d.text((810, 358), "1", font=font(34, bold=True), fill="#4F46E5")
    d.rounded_rectangle((966, 314, 1098, 396), radius=18, fill="#FFF7ED", outline="#FED7AA", width=2)
    d.text((986, 334), "Risks", font=font(18, bold=True), fill="#B45309")
    d.text((986, 358), "2", font=font(34, bold=True), fill="#B45309")
    d.rounded_rectangle((790, 416, 1098, 448), radius=14, fill="#ECFDF5", outline="#A7F3D0", width=2)
    d.text((810, 421), "Operator-facing status, not hidden agent state", font=font(16, bold=True), fill="#166534")

    d.text((100, 540), "Open-source starter for builders who want AI systems that stay legible under pressure.", font=font(22), fill="#475569")

    img.save(SOCIAL_PNG)


if __name__ == "__main__":
    build_war_room_demo()
    build_social_preview()
    print(WARM_ROOM_PNG)
    print(SOCIAL_PNG)
