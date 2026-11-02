"""The site's photo grade: warm, quiet, a little like old paper in candlelight.

Use it on any photo that looks harsh, cold or dated next to the others, so every picture on the site sits in the
same light. Shadows go toward the site's ink (#1d1b17), highlights toward its cream paper (#f7f2e8), colour is softened
by a quarter, mid-tones get a gentle S-curve, and the edges darken slightly.

    python3 _notes/tools/grade.py IN.jpg OUT.jpg [--width 1600] [--crop x0,y0,x1,y1] [--strength 1.0]

--crop is in fractions of the picture (0..1). Output is JPEG q80, progressive.
"""
import argparse
import numpy as np
from PIL import Image, ImageOps

INK = np.array([29, 27, 23]) / 255.0      # --ink
PAPER = np.array([247, 242, 232]) / 255.0  # --paper


def grade(im, strength=1.0):
    a = np.asarray(im.convert("RGB"), dtype=np.float32) / 255.0
    orig = a.copy()
    lum = (a @ np.array([0.2126, 0.7152, 0.0722], dtype=np.float32))[..., None]
    a = lum + (a - lum) * 0.76                                   # soften colour (a quarter)
    a = a + 0.10 * np.sin(np.pi * (a - 0.5)) * (a * (1 - a)) * 4  # gentle S-curve in the mid-tones
    a = INK + a * (PAPER - INK)                                   # blacks to ink, whites to cream
    warm = np.array([1.03, 1.0, 0.94], dtype=np.float32)          # a touch of gold in the light
    a = a * (1 + (warm - 1) * lum)
    h, w = a.shape[:2]                                            # soft vignette
    y, x = np.ogrid[-1:1:h * 1j, -1:1:w * 1j]
    v = 1 - 0.16 * np.clip((x ** 2 + y ** 2) / 2, 0, 1) ** 1.3
    a = a * v[..., None]
    a = orig + (a - orig) * strength
    return Image.fromarray((np.clip(a, 0, 1) * 255 + 0.5).astype(np.uint8))


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("src"); ap.add_argument("dst")
    ap.add_argument("--width", type=int, default=1600)
    ap.add_argument("--crop", default=None)
    ap.add_argument("--strength", type=float, default=1.0)
    o = ap.parse_args()
    im = ImageOps.exif_transpose(Image.open(o.src)).convert("RGB")
    if o.crop:
        x0, y0, x1, y1 = (float(v) for v in o.crop.split(","))
        W, H = im.size
        im = im.crop((int(x0 * W), int(y0 * H), int(x1 * W), int(y1 * H)))
    if im.width > o.width:
        im = im.resize((o.width, round(im.height * o.width / im.width)), Image.LANCZOS)
    grade(im, o.strength).save(o.dst, quality=80, optimize=True, progressive=True)
    print(o.dst, im.size)
