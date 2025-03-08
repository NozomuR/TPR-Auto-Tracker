# utils.py
import os
from PIL import Image, ImageTk, ImageEnhance, ImageOps, ImageColor, ImageChops
import dolphin_memory_engine as dme
from config import BITWISE_BASE_ADDRESS, BITWISE_NUM_BYTES, ITEM_SIZE


def load_image(filepath):
    """Load an image from disk."""
    return Image.open(filepath)


def process_image(image, mode="colored", brightness=1.0):
    """
    Process an image:
      - "colored": returns the image (optionally with brightness adjustment)
      - "grey": returns a desaturated (greyed‑out) version.
    """
    img = image.copy()
    if mode == "grey":
        img = ImageEnhance.Color(img).enhance(0.0)
    if brightness != 1.0:
        img = ImageEnhance.Brightness(img).enhance(brightness)
    return img


from PIL import ImageOps


def tint_image(img, tint):
    base_img = img.convert("RGBA")
    tint_rgb = ImageColor.getrgb(tint)
    solid_color = Image.new("RGBA", base_img.size, tint_rgb + (0,))
    tinted_img = ImageChops.multiply(base_img, solid_color)
    tinted_img.putalpha(base_img.split()[3])
    return tinted_img


def apply_tint(image, tint_color):
    """
    Convert the image to grayscale and then colorize it so that white becomes tint_color.
    This method preserves detail while shifting the hue.
    """
    # Convert to grayscale.
    gray = image.convert("L")
    # Colorize: map black to black and white to the tint.
    tinted = ImageOps.colorize(gray, black="#000000", white=tint_color)
    return tinted

def get_photo_image(filepath, mode="colored", brightness=1.0, size=ITEM_SIZE, tint=None):
    """Load, resize, process, and optionally tint an image, and return a PhotoImage."""
    from PIL import ImageOps, ImageEnhance
    # Load the image.
    image = Image.open(filepath)
    # Resize the image to fit within 'size' while preserving aspect ratio.
    image = ImageOps.contain(image, size)
    # Create a transparent canvas and center the image.
    canvas = Image.new("RGBA", size, (0, 0, 0, 0))
    x = (size[0] - image.width) // 2
    y = (size[1] - image.height) // 2
    canvas.paste(image, (x, y))
    # Process the image: if mode is "grey", desaturate; otherwise, adjust brightness.
    processed = canvas.copy()
    if mode == "grey":
        processed = ImageEnhance.Color(processed).enhance(0.0)
    if brightness != 1.0:
        processed = ImageEnhance.Brightness(processed).enhance(brightness)
    # If mode is grey, optionally darken a bit.
    if mode == "grey":
        processed = ImageEnhance.Brightness(processed).enhance(0.5)
    # If a tint is provided and we're in colored mode, apply our tint.
    if tint and mode == "colored":
        processed = apply_tint(processed, tint)
    photo = ImageTk.PhotoImage(processed)
    photo.original = processed  # Save the processed PIL image.
    return photo


def read_bitwise_flags():
    """Read BITWISE_NUM_BYTES from BITWISE_BASE_ADDRESS using the Dolphin memory engine."""
    try:
        data = dme.read_bytes(BITWISE_BASE_ADDRESS, BITWISE_NUM_BYTES)
        return data  # Should be a bytes or bytearray object
    except Exception as e:
        print(f"Error reading bitwise flags: {e}")
        return None
