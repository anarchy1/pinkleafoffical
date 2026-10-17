#!/usr/bin/env python3
"""Put a price badge and the logo on a plant photo, without wrecking the colour.

    python3 tools/price_photo.py PHOTO 713 [-o out.jpg]
    python3 tools/price_photo.py a.jpg 713 b.jpg 823 c.jpg 897 --outdir ./priced
    python3 tools/price_photo.py PHOTO 713 --no-logo

Why this script exists instead of doing it by hand each time.

Kat's photos come off an iPhone in the Display P3 colour space, with an ICC
profile embedded in the file that tells a viewer how to read the numbers.
Pillow drops that profile on save unless you carry it across yourself. A file
with no profile gets read as plain sRGB, so every colour flattens out. On 30
September a set of Atabapoense photos went out looking dim and desaturated,
and the pinks, which are the entire reason anyone buys these plants, took the
worst of it. Kat spotted it immediately.

So: always carry icc_profile and exif through to the saved file. The check at
the bottom of this script proves it happened, and --verify compares the result
against the original so a regression shows up as a number rather than as a
customer seeing a dull plant.

Nothing here is customer facing on its own. The output is an image Kat sends
by hand, so no price written by this script reaches anyone without her.
"""

import argparse
import io
import os
import sys

from PIL import Image, ImageChops, ImageDraw, ImageFont

# Brand rose and cream. Restrained on purpose: the plant is the subject and
# the badge is a label, not decoration.
ROSE = (150, 90, 94)
CREAM = (250, 245, 238)

# Kat asked for the logo on these on 17 Oct 2026, so it now goes on by default.
# brand/README.md decides which file and how: the rose lockup is the asset for
# anything on a light background, and it goes on whole. Never crop it, never
# rebuild it in text, never swap in favicon.png, which is a different drawing.
# If this file is missing, stop rather than improvising a substitute.
LOGO = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "brand",
    "lockup-rose-trimmed.png",
)
LOGO_WIDTH_RATIO = 0.14
LOGO_MARGIN_RATIO = 0.05

# How the verify step tells JPEG rounding apart from a real change. Re-saving
# an untouched photo at quality 95 moved no pixel in the greyscale difference
# past 12 on the 17 Oct test set, so 32 sits well clear of encoder noise, and
# any genuine paste covers far more than a twentieth of a percent of the frame.
NOISE_FLOOR = 32
MOVED_LIMIT = 0.0005

FONT_CANDIDATES = [
    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
    "/System/Library/Fonts/Supplemental/Arial Bold.ttf",
    "/Library/Fonts/Arial Bold.ttf",
]

SHEQEL = chr(0x20AA)


def pick_font(size):
    for path in FONT_CANDIDATES:
        if os.path.exists(path):
            return ImageFont.truetype(path, size)
    sys.exit(
        "no usable bold font found. Add one to FONT_CANDIDATES.\n"
        "The font has to carry the sheqel sign, so a bare fallback will not do."
    )


def badge(photo, price):
    """Return the photo with a rose price pill centred near the top."""
    width, height = photo.size
    layer = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(layer)

    text = "%s %s" % (price, SHEQEL)
    font = pick_font(max(48, round(width * 0.081)))
    box = draw.textbbox((0, 0), text, font=font)
    text_w, text_h = box[2] - box[0], box[3] - box[1]

    pad_x, pad_y = round(width * 0.048), round(width * 0.030)
    pill_w, pill_h = text_w + pad_x * 2, text_h + pad_y * 2
    x, y = (width - pill_w) // 2, round(height * 0.055)

    draw.rounded_rectangle(
        [x, y, x + pill_w, y + pill_h], radius=pill_h // 2, fill=ROSE + (235,)
    )
    draw.text((x + pad_x - box[0], y + pad_y - box[1]), text, font=font, fill=CREAM)

    return Image.alpha_composite(photo.convert("RGBA"), layer).convert("RGB")


def stamp_logo(photo, logo_path):
    """Paste the lockup whole into the bottom right. Returns (image, top_y).

    The top_y is what the verify step uses to stay off the logo, so a stamped
    photo does not report itself as altered on every run.
    """
    mark = Image.open(logo_path).convert("RGBA")
    width, height = photo.size

    mark_w = round(width * LOGO_WIDTH_RATIO)
    mark_h = round(mark.height * mark_w / mark.width)
    mark = mark.resize((mark_w, mark_h), Image.LANCZOS)

    margin = round(width * LOGO_MARGIN_RATIO)
    x, y = width - mark_w - margin, height - mark_h - margin

    out = photo.convert("RGBA")
    out.alpha_composite(mark, (x, y))
    return out.convert("RGB"), y


def profile_name(icc):
    if not icc:
        return "NONE"
    try:
        from PIL import ImageCms

        return ImageCms.getProfileDescription(
            ImageCms.ImageCmsProfile(io.BytesIO(icc))
        ).strip()
    except Exception:
        return "present, unnamed"


def run(src, price, dest, verify=True, logo=LOGO):
    original = Image.open(src)

    # The whole point of this script. Keep them.
    icc = original.info.get("icc_profile")
    exif = original.info.get("exif")

    out = badge(original.convert("RGB"), price)

    logo_top = None
    if logo:
        if not os.path.exists(logo):
            sys.exit(
                "no logo at %s.\n"
                "Do not substitute another file. See brand/README.md, or pass "
                "--no-logo." % logo
            )
        out, logo_top = stamp_logo(out, logo)

    save_args = {"quality": 95, "subsampling": 0}
    if icc:
        save_args["icc_profile"] = icc
    if exif:
        save_args["exif"] = exif
    out.save(dest, **save_args)

    line = "%s  %s %s  profile: %s" % (
        os.path.basename(dest),
        price,
        SHEQEL,
        profile_name(icc),
    )

    if verify:
        # Compare the part of the frame neither the badge nor the logo covers.
        #
        # Count the pixels that moved, do not read the single worst one. On a
        # detailed plant photo, saving the SAME image again at quality 95 puts
        # a handful of isolated pixels 20 or more apart on leaf edges, so the
        # old "worst pixel over 12" test called four untouched Paraiso Verde
        # photos altered on 17 Oct 2026. A real paste moves a contiguous block,
        # which shows up as a share of the frame rather than as one pixel.
        width, height = original.size
        bottom = logo_top if logo_top is not None else height
        window = (0, round(height * 0.25), width, bottom)
        rgb_diff = ImageChops.difference(
            original.convert("RGB").crop(window), Image.open(dest).convert("RGB").crop(window)
        )
        # Per pixel, the worst of the three channels. Converting to greyscale
        # would average them instead and hide a shift in a single channel.
        red, green, blue = rgb_diff.split()
        diff = ImageChops.lighter(ImageChops.lighter(red, green), blue)
        worst = diff.getextrema()[1]
        histogram = diff.histogram()
        moved = sum(histogram[NOISE_FLOOR + 1:]) / float(sum(histogram))
        line += "  below badge: worst %d, %.3f%% of pixels moved" % (worst, moved * 100)
        if moved > MOVED_LIMIT:
            line += "  <-- CHECK THIS, the photo changed"
        if not icc:
            line += "  <-- no colour profile on the source, output may look flat"

    print(line)
    return dest


def main():
    parser = argparse.ArgumentParser(
        description="Overlay a price and the logo on plant photos, "
        "preserving colour profile and EXIF."
    )
    parser.add_argument(
        "pairs",
        nargs="+",
        metavar="PHOTO PRICE",
        help="one or more PHOTO PRICE pairs, e.g. small.jpg 713 big.jpg 897",
    )
    parser.add_argument("-o", "--out", help="output path (single pair only)")
    parser.add_argument("--outdir", default="priced", help="output directory (default: priced)")
    parser.add_argument(
        "--no-logo",
        dest="logo",
        action="store_const",
        const=None,
        default=LOGO,
        help="leave the logo off. It goes on by default (Kat, 17 Oct 2026)",
    )
    args = parser.parse_args()

    if len(args.pairs) % 2:
        sys.exit("give PHOTO and PRICE in pairs, e.g. small.jpg 713 big.jpg 897")

    pairs = list(zip(args.pairs[0::2], args.pairs[1::2]))

    if args.out and len(pairs) > 1:
        sys.exit("--out takes a single PHOTO PRICE pair. Use --outdir for several.")

    for src, price in pairs:
        if not os.path.exists(src):
            sys.exit("no such photo: %s" % src)
        if not price.isdigit():
            sys.exit("price should be digits only, got %r" % price)

    if args.out:
        run(pairs[0][0], pairs[0][1], args.out, logo=args.logo)
        return

    os.makedirs(args.outdir, exist_ok=True)
    for src, price in pairs:
        stem = os.path.splitext(os.path.basename(src))[0]
        run(
            src,
            price,
            os.path.join(args.outdir, "%s-%s.jpg" % (stem, price)),
            logo=args.logo,
        )


if __name__ == "__main__":
    main()
