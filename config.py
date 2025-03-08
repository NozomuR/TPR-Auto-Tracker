# config.py
import os

# Global constants
ITEM_SIZE = (48, 48)          # Each item image will be resized to 48x48 pixels
WINDOW_GEOMETRY = "560x834"    # Default window size: width x height
SKIP_ITEMS = {"ooccoo", "quest_item"}  # Items to skip in the layout

# Memory reading constants for bitwise-read items
BITWISE_BASE_ADDRESS = 0x8040628C  # Base address for the bit‑flag block
BITWISE_NUM_BYTES = 32             # Total number of bytes to read from that block
