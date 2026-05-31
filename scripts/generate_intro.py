"""Generate a light-themed particle intro GIF for GitHub profile README."""

from __future__ import annotations

import math
import random
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "intro.gif"

WIDTH, HEIGHT = 900, 200
FPS = 15
BG = (255, 255, 255)
TEXT = (36, 41, 47)
ACCENT = (9, 105, 218)
PARTICLE = (180, 190, 200)
LINE = (220, 226, 232)

PHRASES = [
    "Hi, I'm Mehedi",
    "Senior Data Analyst",
    "Data -> Insights -> Impact",
]

random.seed(42)
PARTICLES = [(random.randint(40, WIDTH - 40), random.randint(30, HEIGHT - 30)) for _ in range(28)]


def load_font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    name = "C:/Windows/Fonts/segoeuib.ttf" if bold else "C:/Windows/Fonts/segoeui.ttf"
    path = Path(name)
    if path.exists():
        return ImageFont.truetype(str(path), size)
    return ImageFont.load_default()


def draw_particles(draw: ImageDraw.ImageDraw, frame: int) -> None:
    points = []
    for i, (x, y) in enumerate(PARTICLES):
        ox = int(6 * math.sin((frame + i * 11) / 18))
        oy = int(4 * math.cos((frame + i * 7) / 14))
        points.append((x + ox, y + oy))

    for i, p1 in enumerate(points):
        for p2 in points[i + 1 :]:
            dist = math.hypot(p1[0] - p2[0], p1[1] - p2[1])
            if dist < 120:
                draw.line([p1, p2], fill=LINE, width=1)

    for p in points:
        draw.ellipse([p[0] - 2, p[1] - 2, p[0] + 2, p[1] + 2], fill=PARTICLE)


def render_frame(frame: int, phrase_idx: int, typed_chars: int, cursor_on: bool) -> Image.Image:
    img = Image.new("RGB", (WIDTH, HEIGHT), BG)
    draw = ImageDraw.Draw(img)
    draw_particles(draw, frame)

    title_font = load_font(34, bold=True)
    phrase = PHRASES[phrase_idx][:typed_chars]
    bbox = draw.textbbox((0, 0), phrase or " ", font=title_font)
    text_w = bbox[2] - bbox[0]
    x = (WIDTH - text_w) // 2
    y = (HEIGHT - 40) // 2
    draw.text((x, y), phrase, font=title_font, fill=TEXT)

    if cursor_on:
        cursor_x = x + text_w + 4
        draw.rectangle([cursor_x, y + 4, cursor_x + 2, y + 36], fill=ACCENT)

    return img


def build_frames() -> list[Image.Image]:
    frames: list[Image.Image] = []
    hold = FPS * 2

    for idx, phrase in enumerate(PHRASES):
        for n in range(len(phrase) + 1):
            for tick in range(2):
                frames.append(render_frame(len(frames), idx, n, cursor_on=tick == 0))
        for i in range(hold):
            frames.append(render_frame(len(frames), idx, len(phrase), cursor_on=i % 2 == 0))

    return frames


def main() -> None:
    frames = build_frames()
    frames[0].save(
        OUTPUT,
        save_all=True,
        append_images=frames[1:],
        duration=int(1000 / FPS),
        loop=0,
        optimize=True,
    )
    print(f"Wrote {OUTPUT} ({len(frames)} frames)")


if __name__ == "__main__":
    main()
