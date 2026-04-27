from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter


ROOT = Path(__file__).resolve().parent


def lerp(a, b, t):
    return a + (b - a) * t


def lerp_color(c1, c2, t):
    return tuple(int(round(lerp(c1[i], c2[i], t))) for i in range(4))


def cubic_points(p0, p1, p2, p3, steps=36):
    points = []
    for i in range(steps + 1):
        t = i / steps
        mt = 1 - t
        x = (
            mt ** 3 * p0[0]
            + 3 * mt ** 2 * t * p1[0]
            + 3 * mt * t ** 2 * p2[0]
            + t ** 3 * p3[0]
        )
        y = (
            mt ** 3 * p0[1]
            + 3 * mt ** 2 * t * p1[1]
            + 3 * mt * t ** 2 * p2[1]
            + t ** 3 * p3[1]
        )
        points.append((x, y))
    return points


def draw_gradient_segmented(draw, points, colors, width):
    total = max(len(points) - 1, 1)
    for idx in range(total):
        t = idx / total
        if t < 0.5:
            color = lerp_color(colors[0], colors[1], t * 2)
        else:
            color = lerp_color(colors[1], colors[2], (t - 0.5) * 2)
        draw.line([points[idx], points[idx + 1]], fill=color, width=width)


def build_master():
    size = 512
    image = Image.new("RGBA", (size, size), (0, 0, 0, 0))

    base = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    base_draw = ImageDraw.Draw(base)
    for y in range(size):
        t = y / (size - 1)
        top = (11, 16, 33, 255)
        mid = (8, 12, 24, 255)
        bot = (4, 5, 13, 255)
        if t < 0.58:
            color = tuple(int(lerp(top[i], mid[i], t / 0.58)) for i in range(4))
        else:
            color = tuple(int(lerp(mid[i], bot[i], (t - 0.58) / 0.42)) for i in range(4))
        base_draw.rounded_rectangle((0, y, size, y + 2), radius=128, fill=color)
    image.alpha_composite(base)

    nebula = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    nebula_draw = ImageDraw.Draw(nebula)
    nebula_draw.ellipse((24, 18, 320, 282), fill=(22, 55, 93, 135))
    nebula_draw.ellipse((78, 48, 350, 292), fill=(16, 31, 61, 88))
    nebula = nebula.filter(ImageFilter.GaussianBlur(38))
    image.alpha_composite(nebula)

    orbit = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    orbit_draw = ImageDraw.Draw(orbit)
    orbit_draw.arc((108, 104, 420, 416), start=212, end=398, fill=(90, 216, 255, 52), width=11)
    orbit = orbit.filter(ImageFilter.GaussianBlur(0.6))
    image.alpha_composite(orbit)

    glow = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    glow_draw = ImageDraw.Draw(glow)
    glow_draw.ellipse((364, 94, 396, 126), fill=(246, 208, 123, 255))
    glow = glow.filter(ImageFilter.GaussianBlur(18))
    image.alpha_composite(glow)

    stars = ImageDraw.Draw(image)
    stars.ellipse((383, 109, 399, 125), fill=(245, 221, 159, 255))
    stars.ellipse((122, 136, 131, 145), fill=(245, 221, 159, 240))
    stars.ellipse((96, 184, 102, 190), fill=(255, 255, 255, 176))
    stars.ellipse((404, 366, 411, 373), fill=(255, 255, 255, 126))

    s_points = []
    scale = 8
    segments = [
        ((44, 16), (40, 13.3), (31.4, 12.6), (26.4, 15.6)),
        ((26.4, 15.6), (21.8, 18.3), (21.4, 23), (25, 25.8)),
        ((25, 25.8), (28.1, 28.2), (33.1, 28.9), (36.6, 30.5)),
        ((36.6, 30.5), (40.5, 32.2), (42.4, 35.1), (41.5, 39.1)),
        ((41.5, 39.1), (40.5, 43.7), (35.9, 47.5), (28.8, 48)),
        ((28.8, 48), (24.3, 48.4), (20.9, 47.3), (18.4, 45.1)),
    ]
    for idx, seg in enumerate(segments):
        pts = cubic_points(*[(x * scale, y * scale) for x, y in seg], steps=28)
        if idx:
            pts = pts[1:]
        s_points.extend(pts)

    s_glow = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    s_glow_draw = ImageDraw.Draw(s_glow)
    draw_gradient_segmented(
        s_glow_draw,
        s_points,
        [(255, 240, 191, 140), (240, 192, 96, 180), (255, 240, 191, 140)],
        62,
    )
    s_glow = s_glow.filter(ImageFilter.GaussianBlur(13))
    image.alpha_composite(s_glow)

    s_layer = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    s_draw = ImageDraw.Draw(s_layer)
    draw_gradient_segmented(
        s_draw,
        s_points,
        [(255, 240, 191, 255), (240, 192, 96, 255), (255, 240, 191, 255)],
        50,
    )
    image.alpha_composite(s_layer)

    return image


def save_outputs(master):
    master.resize((32, 32), Image.Resampling.LANCZOS).save(ROOT / "favicon-32x32.png")
    master.resize((16, 16), Image.Resampling.LANCZOS).save(ROOT / "favicon-16x16.png")
    master.resize((180, 180), Image.Resampling.LANCZOS).save(ROOT / "apple-touch-icon.png")
    master.save(
        ROOT / "favicon.ico",
        sizes=[(16, 16), (32, 32), (48, 48)],
    )


if __name__ == "__main__":
    save_outputs(build_master())
