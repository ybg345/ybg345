"""Generate intro.gif for GitHub profile README."""

from __future__ import annotations

import math
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "intro.gif"

WIDTH, HEIGHT = 920, 240
FPS = 12
BG = (13, 17, 23)
ACCENT = (9, 105, 218)
TEXT = (230, 237, 243)
MUTED = (88, 166, 255)
GREEN = (63, 185, 80)

PHRASES = [
    "Hi, I'm Mehedi",
    "Senior Data Analyst",
    "Data -> Insights -> Impact",
]

FONT_CANDIDATES = [
    Path("C:/Windows/Fonts/CascadiaMono.ttf"),
    Path("C:/Windows/Fonts/consola.ttf"),
    Path("C:/Windows/Fonts/lucon.ttf"),
]


def load_font(size: int) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    for path in FONT_CANDIDATES:
        if path.exists():
            return ImageFont.truetype(str(path), size)
    return ImageFont.load_default()


def draw_background(draw: ImageDraw.ImageDraw, frame: int) -> None:
    for x in range(0, WIDTH, 28):
        alpha = 18 + int(8 * math.sin((x + frame * 3) / 42))
        draw.line([(x, 0), (x, HEIGHT)], fill=(alpha, alpha + 8, alpha + 18), width=1)

    bar_heights = [42, 68, 55, 88, 61, 74, 49]
    base_y = HEIGHT - 34
    for i, h in enumerate(bar_heights):
        pulse = math.sin((frame / 8) + i * 0.7) * 10
        height = int(h + pulse)
        x0 = 36 + i * 18
        draw.rectangle(
            [x0, base_y - height, x0 + 10, base_y],
            fill=(9, 105, 218, 180) if i % 2 == 0 else (63, 185, 80, 180),
        )


def render_frame(frame: int, phrase_idx: int, typed_chars: int, cursor_on: bool) -> Image.Image:
    img = Image.new("RGB", (WIDTH, HEIGHT), BG)
    draw = ImageDraw.Draw(img)

    draw_background(draw, frame)

    title_font = load_font(34)
    sub_font = load_font(18)

    draw.rounded_rectangle([24, 24, WIDTH - 24, HEIGHT - 24], radius=18, outline=(48, 54, 61), width=2)
    draw.text((44, 38), "mehedi@analytics", font=sub_font, fill=MUTED)
    draw.text((WIDTH - 210, 38), "live dashboard", font=sub_font, fill=GREEN)

    phrase = PHRASES[phrase_idx][:typed_chars]
    draw.text((44, 92), phrase, font=title_font, fill=TEXT)

    if cursor_on:
        bbox = draw.textbbox((44, 92), phrase, font=title_font)
        cursor_x = bbox[2] + 6 if phrase else 44
        draw.rectangle([cursor_x, 96, cursor_x + 14, 132], fill=ACCENT)

    draw.text((44, 150), "Python · SQL · Snowflake · Tableau · Agentic AI", font=sub_font, fill=MUTED)

    dots = "." * ((frame // 8) % 4)
    draw.text((44, 182), f"loading insights{dots}", font=sub_font, fill=ACCENT)

    return img


def build_frames() -> list[Image.Image]:
    frames: list[Image.Image] = []
    hold = FPS * 2

    for idx, phrase in enumerate(PHRASES):
        for n in range(len(phrase) + 1):
            for tick in range(2):
                frames.append(render_frame(len(frames), idx, n, cursor_on=tick == 0))
        for _ in range(hold):
            frames.append(render_frame(len(frames), idx, len(phrase), cursor_on=len(frames) % 2 == 0))

    return frames


def main() -> None:
    frames = build_frames()
    duration = int(1000 / FPS)
    frames[0].save(
        OUTPUT,
        save_all=True,
        append_images=frames[1:],
        duration=duration,
        loop=0,
        optimize=True,
    )
    print(f"Wrote {OUTPUT} ({len(frames)} frames)")


if __name__ == "__main__":
    main()
