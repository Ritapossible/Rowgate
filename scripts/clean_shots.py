"""Sharpen the Bob IDE screen captures so the cell references are readable.

The captures are ~1080px-wide frames of a 1920px screen, so the code spans in
Bob's answers sit below one pixel per stroke. Upscaling with LANCZOS and
re-sharpening the edges recovers them; it cannot invent detail the frame never
had, so record at full resolution when you can.

Usage: python scripts/clean_shots.py <source-dir> <name>=<file.jpg> ...
"""

import sys
from pathlib import Path

from PIL import Image, ImageEnhance, ImageFilter


def enhance(im: Image.Image, crop_bottom: int = 0, scale: int = 3) -> Image.Image:
    im = im.convert("RGB")
    if crop_bottom:  # trim the desktop taskbar
        im = im.crop((0, 0, im.width, im.height - crop_bottom))
    im = im.resize((im.width * scale, im.height * scale), Image.LANCZOS)
    im = im.filter(ImageFilter.UnsharpMask(radius=1.4, percent=190, threshold=2))  # letter strokes
    im = im.filter(ImageFilter.UnsharpMask(radius=4.0, percent=45, threshold=3))   # panel edges
    return ImageEnhance.Contrast(im).enhance(1.22)


def main(argv: list[str]) -> int:
    if len(argv) < 3:
        print(__doc__)
        return 2
    src = Path(argv[1])
    for pair in argv[2:]:
        out_path, _, in_name = pair.partition("=")
        im = Image.open(src / in_name)
        dst = Path(out_path)
        dst.parent.mkdir(parents=True, exist_ok=True)
        enhance(im, crop_bottom=24).save(dst, "PNG", optimize=True)
        print(f"{dst}  {im.size} -> {Image.open(dst).size}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
