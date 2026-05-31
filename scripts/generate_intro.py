"""Generate a light-themed intro GIF for GitHub profile README."""

from __future__ import annotations

import math
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "intro.gif"

WIDTH, HEIGHT = 900, 200
FPS = 15
BG = (255, 255, 255)
SKY = (248, 251, 255)
TEXT = (36, 41, 47)
ACCENT = (9, 105, 218)

PHRASES = [
    "Hi, I'm Mehedi",
    "Senior Data Analyst",
    "Data -> Insights -> Impact",
]

MOUNTAIN_LAYERS = [
    {"color": (235, 240, 246), "base": 100, "scale": 0.85, "speed": 0.25, "detail": 0.45, "peaks": 0.35},
    {"color": (220, 230, 240), "base": 115, "scale": 1.05, "speed": 0.35, "detail": 0.60, "peaks": 0.55},
    {"color": (205, 218, 232), "base": 132, "scale": 1.25, "speed": 0.50, "detail": 0.80, "peaks": 0.75},
    {"color": (188, 200, 218), "base": 148, "scale": 1.45, "speed": 0.65, "detail": 1.00, "peaks": 1.00},
]

# Distinct peaks read as mountains rather than rolling hills.
MOUNTAIN_PEAKS = [(80, 42), (220, 55), (420, 48), (580, 62), (740, 50), (860, 38)]

WAVE_LAYERS = [
    {"color": (232, 239, 246), "base": 182, "amp": 2, "length": 160, "speed": 0.30},
    {"color": (222, 232, 242), "base": 188, "amp": 3, "length": 120, "speed": 0.40},
    {"color": (212, 225, 238), "base": 193, "amp": 2, "length": 95, "speed": 0.50},
]


def load_font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    name = "C:/Windows/Fonts/segoeuib.ttf" if bold else "C:/Windows/Fonts/segoeui.ttf"
    path = Path(name)
    if path.exists():
        return ImageFont.truetype(str(path), size)
    return ImageFont.load_default()


def lerp_color(a: tuple[int, int, int], b: tuple[int, int, int], t: float) -> tuple[int, int, int]:
    return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))


def draw_sky(draw: ImageDraw.ImageDraw) -> None:
    for y in range(HEIGHT):
        t = y / max(HEIGHT - 1, 1)
        color = lerp_color(BG, SKY, min(t * 1.4, 1.0))
        draw.line([(0, y), (WIDTH, y)], fill=color)


def mountain_height(x: float, frame: int, layer: dict) -> float:
    phase = frame * layer["speed"]
    s = layer["scale"]
    d = layer["detail"]
    p = layer["peaks"]
    height = layer["base"] - s * (
        24 * math.sin((x + phase * 18) / 210 + 0.4)
        + 16 * math.sin((x - phase * 12) / 120 + 1.2)
        + 11 * d * math.sin((x + phase * 8) / 70 + 2.1)
        + 7 * d * math.cos((x - phase * 6) / 45 + 0.8)
    )
    for peak_x, peak_h in MOUNTAIN_PEAKS:
        drift = phase * 6 * layer["speed"]
        height -= p * peak_h * math.exp(-((x - peak_x - drift) ** 2) / (2 * 55**2))
    return height


def draw_mountains(draw: ImageDraw.ImageDraw, frame: int) -> None:
    step = 6
    for layer in MOUNTAIN_LAYERS:
        points: list[tuple[int, int]] = [(0, HEIGHT), (0, int(mountain_height(0, frame, layer)))]
        for x in range(step, WIDTH + 1, step):
            points.append((x, int(mountain_height(x, frame, layer))))
        points.append((WIDTH, HEIGHT))
        draw.polygon(points, fill=layer["color"])


def wave_height(x: float, frame: int, layer: dict) -> float:
    phase = frame * layer["speed"]
    primary = math.sin((x + phase * 6) / layer["length"])
    secondary = 0.35 * math.sin((x - phase * 4) / (layer["length"] * 1.6) + 0.8)
    return layer["base"] + layer["amp"] * (primary + secondary)


def draw_waves(draw: ImageDraw.ImageDraw, frame: int) -> None:
    step = 5
    for layer in WAVE_LAYERS:
        top: list[tuple[int, int]] = []
        for x in range(0, WIDTH + 1, step):
            top.append((x, int(wave_height(x, frame, layer))))
        points = top + [(WIDTH, HEIGHT), (0, HEIGHT)]
        draw.polygon(points, fill=layer["color"])


def draw_scenery(draw: ImageDraw.ImageDraw, frame: int) -> None:
    draw_sky(draw)
    draw_mountains(draw, frame)
    draw_waves(draw, frame)


def render_frame(frame: int, phrase_idx: int, typed_chars: int, cursor_on: bool) -> Image.Image:
    img = Image.new("RGB", (WIDTH, HEIGHT), BG)
    draw = ImageDraw.Draw(img)
    draw_scenery(draw, frame)

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
