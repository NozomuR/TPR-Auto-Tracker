import math
import os
import time
import tkinter as tk
import dolphin_memory_engine as dme  # Keep using dme as before
import numpy as np
from PIL import Image, ImageTk, ImageFilter, ImageChops, ImageOps, ImageEnhance, ImageDraw, ImageFont, ImageColor
from config import ITEM_SIZE, SKIP_ITEMS, WINDOW_GEOMETRY
from utils import get_photo_image, read_bitwise_flags


from item_config import items_config  # This now includes your Bugs entry


def spin_and_float(label, orig_img, angle=0, t=0):
    """
    Rotates the original image by a given angle and applies a vertical offset based on a sine wave.
    This creates a spinning and floating effect.
    """
    # Rotate the image.
    rotated = orig_img.rotate(angle, resample=Image.BICUBIC, expand=False)
    photo = ImageTk.PhotoImage(rotated)
    label.config(image=photo)
    label.image = photo  # Keep a reference.

    # Calculate vertical offset (floating effect).
    amplitude = 5  # Maximum offset in pixels.
    offset_y = amplitude * math.sin(math.radians(t))

    # Update the label position using place_configure.
    label.place_configure(relx=0.5, rely=0.4, anchor="center", y=offset_y)

    # Update angle and time for smooth animation.
    new_angle = (angle + 1) % 360  # 1 degree increment.
    new_t = (t + 2) % 360  # Adjust the vertical offset increment.
    label.after(30, spin_and_float, label, orig_img, new_angle, new_t)


class Tracker:
    def __init__(self, root):
        self.root = root
        self.root.title("Game Tracker")
        self.root.configure(bg="#1e1e1e")
        # Convert the first two values of WINDOW_GEOMETRY to ints (e.g., (800,600))
        self.ref_geometry = tuple(map(int, WINDOW_GEOMETRY[:2]))
        self.items = {}
        self.load_items()
        self.create_ui()
        self.last_scale = None  # Used to throttle resize events.
        self.update_tracker()  # Begin polling memory

    def load_items(self):
        """Preload each item’s images for its various states."""
        self.items = {}
        for key, cfg in items_config.items():
            item = {}
            item["name"] = cfg["name"]
            item["progressive"] = cfg.get("progressive", False)
            item["config"] = cfg
            item["photo_images"] = {}
            if cfg.get("image_files"):
                for state, filename in cfg["image_files"].items():
                    path = os.path.join("items", filename)
                    # For bomb bag items, load the grey version for the "none" state.
                    if key in {"bomb_bag1", "bomb_bag2", "bomb_bag3"}:
                        mode = "grey" if state == "none" else "colored"
                    else:
                        mode = "grey" if state in {"empty", "none"} else "colored"
                    try:
                        photo = get_photo_image(path, mode=mode, size=ITEM_SIZE)
                    except Exception as e:
                        photo = None
                    item["photo_images"][state] = photo
            elif cfg.get("image_file"):
                path = os.path.join("items", cfg["image_file"])
                item["photo_images"]["acquired"] = get_photo_image(path, mode="colored", size=ITEM_SIZE)
                item["photo_images"]["empty"] = get_photo_image(path, mode="grey", size=ITEM_SIZE)
            else:
                item["photo_images"] = None

            # No previous state yet.
            item["prev_state"] = None
            self.items[key] = item

    def create_ui(self):
        """Build the UI using hard-coded rows for specific items."""
        self.main_frame = tk.Frame(self.root, bg="#1e1e1e")
        self.main_frame.pack(expand=True, fill="both", padx=10, pady=10)

        # Define rows with the exact item keys.
        rows = [
            ["sword", "combined_shields", "combined_magic_armor", "shadow_crystal", "fishing_rod", "ancient_sky_book"],
            ["slingshot", "lantern", "gale_boomerang", "iron_boots", "heros_bow", "clawshot"],
            ["bomb_bag1", "bomb_bag2", "bomb_bag3", "ball_and_chain", "dominion_rod", "hawkeye"],
            ["bottles", "poe_souls", "Bugs", "hidden_skill", "trade_item", "wallet"],
            ["aurus_memo", "ashei_sketch", "scent", "fused_shadow1", "fused_shadow2", "fused_shadow3"],
            ["mirror_shards"],
        ]

        for row_keys in rows:
            row_frame = tk.Frame(self.main_frame, bg="#1e1e1e")
            row_frame.pack(pady=4)
            self.add_items_to_frame(row_frame, row_keys, columns=len(row_keys), scale=1.0)

    def add_items_to_frame(self, parent, item_keys, columns, scale=1.0):
        """
        Add items into the given parent frame using a grid with tighter spacing.
        """
        row, col = 0, 0
        cell_width = int(ITEM_SIZE[0] * scale) + 8
        cell_height = int(ITEM_SIZE[1] * scale) + 8
        for key in item_keys:
            if key in SKIP_ITEMS or key not in self.items:
                continue
            item = self.items[key]
            # Use a larger scale for special items like mirror_shards.
            item_scale = 3.0 if key == "mirror_shards" else scale
            cell = tk.Frame(parent, bg="#1e1e1e",
                            width=int(cell_width * item_scale),
                            height=int(cell_height * item_scale))
            cell.grid(row=row, column=col, padx=2, pady=2)
            cell.grid_propagate(False)
            initial_state = item["config"].get("initial_state", "none" if item["progressive"] else "empty")
            if item["photo_images"]:
                photo = item["photo_images"].get(initial_state)
                if photo is not None:
                    pil_img = ImageOps.contain(photo.original,
                                               (int(ITEM_SIZE[0] * item_scale), int(ITEM_SIZE[1] * item_scale)))
                    photo = ImageTk.PhotoImage(pil_img)
                    photo.original = pil_img

                label = tk.Label(cell, image=photo, bg="#1e1e1e")
            else:
                label = tk.Label(cell, text=item["name"], fg="white", bg="#1e1e1e")
            label.place(relx=0.5, rely=0.5, anchor="center")
            item["label_widget"] = label
            item["frame_widget"] = cell

            col += 1
            if col >= columns:
                col = 0
                row += 1

    def glow_transition(self, item, base_img, final_state, steps=20, step=0):
        factor = 1.0 + (1.0 if final_state == "completed" else 0.5) * math.sin(math.pi * step / steps)
        enhancer = ImageEnhance.Brightness(base_img)
        glow_img = enhancer.enhance(factor)
        new_image = ImageTk.PhotoImage(glow_img)
        new_image.original = glow_img
        item["label_widget"].config(image=new_image)
        item["label_widget"].image = new_image
        if step < steps:
            self.root.after(50, self.glow_transition, item, base_img, final_state, steps, step + 1)
        else:
            item["glow_running"] = False
            item["prev_state"] = final_state

    def bounce_effect(self, label, current_scale, step, cycles, base_scale):
        from PIL import ImageTk
        if cycles <= 0:
            original = getattr(label.image, 'original', None)
            if original:
                final_size = (int(ITEM_SIZE[0] * base_scale), int(ITEM_SIZE[1] * base_scale))
                final_photo = ImageTk.PhotoImage(original.resize(final_size, Image.LANCZOS))
                final_photo.original = original
                label.config(image=final_photo)
                label.image = final_photo
            return
        original = getattr(label.image, 'original', None)
        if original is None:
            return
        # Calculate new dimensions based on the current_scale
        new_size = (int(ITEM_SIZE[0] * current_scale), int(ITEM_SIZE[1] * current_scale))
        resized = original.resize(new_size, Image.LANCZOS)
        new_photo = ImageTk.PhotoImage(resized)
        new_photo.original = original
        label.config(image=new_photo)
        label.image = new_photo
        # Oscillate around the base_scale: increase on odd cycles, decrease on even cycles.
        new_scale = current_scale + step if cycles % 2 == 1 else current_scale - step
        self.root.after(50, self.bounce_effect, label, new_scale, step * 0.9, cycles - 1, base_scale)

    def flash_item(self, item):
        if "label_widget" not in item:
            return
        # For Mirror Shards, use a base scale of 3.0; otherwise, default to 1.0.
        base_scale = 3.0 if item["name"] == "Mirror Shards" else 1.0
        # Start the bounce effect at the base scale.
        self.bounce_effect(item["label_widget"], base_scale, step=0.1, cycles=6, base_scale=base_scale)

    def update_tracker(self):
        # First, check if Dolphin is still hooked.
        try:
            if not dme.is_hooked():
                if not getattr(self, "connection_lost_called", False):
                    self.connection_lost_called = True
                    self.connection_lost()
                return
        except Exception:
            self.root.after(100, self.update_tracker)
            return

        try:
            bitwise_data = read_bitwise_flags()

            for key, item in self.items.items():
                if "label_widget" not in item:
                    continue
                cfg = item["config"]

                # --- Branch for items that use multiple addresses (e.g., Bugs) ---
                if "addresses" in cfg:
                    values = [dme.read_byte(addr) for addr in cfg["addresses"]]
                    count = cfg["get_state"](values)
                    state = count  # Using the count as the state.
                    base_path = os.path.join("items", cfg["image_file"])
                    if count == 0:
                        base_img = get_photo_image(base_path, mode="grey", size=ITEM_SIZE).original
                    else:
                        base_img = Image.open(base_path).convert("RGBA").resize(ITEM_SIZE, Image.LANCZOS)
                    draw = ImageDraw.Draw(base_img)
                    font_size = int(ITEM_SIZE[1] * 0.8)
                    try:
                        font = ImageFont.truetype("Roboto-Bold.ttf", font_size)
                    except Exception:
                        font = ImageFont.load_default()
                    text = str(count)
                    bbox = font.getbbox(text)
                    text_width = bbox[2] - bbox[0]
                    text_height = bbox[3] - bbox[1]
                    outline_thickness = 2
                    padding = 4
                    position = (ITEM_SIZE[0] - text_width - padding, ITEM_SIZE[1] - text_height - padding)
                    draw.text(
                        position,
                        text,
                        font=font,
                        fill="Yellow",
                        stroke_width=outline_thickness,
                        stroke_fill="#1e1e1e"
                    )
                    new_image = ImageTk.PhotoImage(base_img)
                    new_image.original = base_img
                    if state != item.get("prev_state"):
                        item["label_widget"].config(image=new_image)
                        item["label_widget"].image = new_image
                        self.flash_item(item)
                        item["prev_state"] = state
                    continue

                # --- Branch for forest_small_keys ---
                if key == "forest_small_keys":
                    save_file_node_base = 0x804065B0
                    local_node_base = 0x80406B18
                    offset = cfg["address"] - save_file_node_base
                    try:
                        node_idx = dme.read_byte(0x80406B38)
                    except Exception:
                        node_idx = 0
                    base_address = local_node_base if node_idx == 0x10 else save_file_node_base
                    target_address = base_address + offset
                    try:
                        val = dme.read_byte(target_address)
                    except Exception:
                        val = 0
                    state = cfg["get_state"](val)
                    if state != item.get("prev_state"):
                        base_path = os.path.join("items", cfg["image_file"])
                        if state == 0:
                            base_img = get_photo_image(base_path, mode="grey", size=ITEM_SIZE).original
                        else:
                            base_img = Image.open(base_path).convert("RGBA").resize(ITEM_SIZE, Image.LANCZOS)
                        draw = ImageDraw.Draw(base_img)
                        font_size = int(ITEM_SIZE[1] * 0.8)
                        try:
                            font = ImageFont.truetype("Roboto-Bold.ttf", font_size)
                        except Exception:
                            font = ImageFont.load_default()
                        text = str(state)
                        bbox = font.getbbox(text)
                        text_width = bbox[2] - bbox[0]
                        text_height = bbox[3] - bbox[1]
                        outline_thickness = 2
                        padding = 4
                        position = (ITEM_SIZE[0] - text_width - padding, ITEM_SIZE[1] - text_height - padding)
                        draw.text(
                            position,
                            text,
                            font=font,
                            fill="Yellow",
                            stroke_width=outline_thickness,
                            stroke_fill="#1e1e1e"
                        )
                        new_image = ImageTk.PhotoImage(base_img)
                        new_image.original = base_img
                        item["label_widget"].config(image=new_image)
                        item["label_widget"].image = new_image
                        self.flash_item(item)
                        item["prev_state"] = state
                    continue

                # --- Branch for mirror_shards ---
                if key == "mirror_shards":
                    val = dme.read_byte(cfg["address"])
                    count = bin(val).count("1")
                    scale_factor = 3.0
                    size = (int(ITEM_SIZE[0] * scale_factor), int(ITEM_SIZE[1] * scale_factor))
                    if count >= 4:
                        state = "completed"
                        base_path = os.path.join("items", cfg["image_files"]["completed"])
                        base_img = Image.open(base_path).convert("RGBA").resize(size, Image.LANCZOS)
                    elif count == 0:
                        state = "empty"
                        base_path = os.path.join("items",
                                                 cfg["image_files"].get("empty", cfg["image_files"]["shard_1"]))
                        base_img = Image.open(base_path).convert("RGBA")
                        base_img = base_img.resize(size, Image.LANCZOS)
                        r, g, b, a = base_img.split()
                        gray = ImageOps.grayscale(Image.merge("RGB", (r, g, b)))
                        base_img = Image.merge("RGBA", (gray, gray, gray, a))
                    else:
                        state = f"shard_{count}"
                        base_path = os.path.join("items", cfg["image_files"]["empty"])
                        base_img = Image.open(base_path).convert("RGBA").resize(size, Image.LANCZOS)
                        for i in range(1, count + 1):
                            shard_path = os.path.join("items", cfg["image_files"][f"shard_{i}"])
                            shard_img = Image.open(shard_path).convert("RGBA").resize(size, Image.LANCZOS)
                            base_img = Image.alpha_composite(base_img, shard_img)
                    if state != item.get("prev_state") and not item.get("glow_running", False):
                        if count > 0:
                            item["glow_running"] = True
                            self.glow_transition(item, base_img, state, steps=20, step=0)
                        else:
                            new_image = ImageTk.PhotoImage(base_img)
                            new_image.original = base_img
                            item["label_widget"].config(image=new_image)
                            item["label_widget"].image = new_image
                            self.flash_item(item)
                            item["prev_state"] = state
                    continue

                # --- Branch for scent ---
                elif key == "scent":
                    val = dme.read_byte(cfg["address"])
                    state = cfg["get_state"](val)
                    tint_colors = {
                        "ilia": "#c75a90",
                        "poe": "#9b5ac7",
                        "reekfish": "#fc7521",
                        "youth": "#c7c05a",
                        "medicine": "#6ac75a",
                        "none": "#808080"
                    }
                    tint = tint_colors.get(state, "#808080")
                    mode = "colored" if state != "none" else "grey"
                    base_photo = get_photo_image(os.path.join("items", cfg["image_file"]),
                                                 mode=mode, size=ITEM_SIZE)
                    base_img = base_photo.original.convert("RGBA")
                    tint_rgb = ImageColor.getrgb(tint)
                    solid_color = Image.new("RGBA", base_img.size, tint_rgb + (0,))
                    tinted_img = ImageChops.multiply(base_img, solid_color)
                    tinted_img.putalpha(base_img.split()[3])
                    new_image = ImageTk.PhotoImage(tinted_img)
                    new_image.original = tinted_img
                    if state != item.get("prev_state"):
                        item["label_widget"].config(image=new_image)
                        item["label_widget"].image = new_image
                        self.flash_item(item)
                        item["prev_state"] = state
                    continue

                # --- Branch for poe_souls ---
                elif key == "poe_souls":
                    val = dme.read_byte(cfg["address"])
                    count = val
                    state = count
                    base_path = os.path.join("items", cfg["image_file"])
                    if count == 0:
                        base_img = get_photo_image(base_path, mode="grey", size=ITEM_SIZE).original
                    else:
                        base_img = Image.open(base_path).convert("RGBA").resize(ITEM_SIZE, Image.LANCZOS)
                    draw = ImageDraw.Draw(base_img)
                    font_size = int(ITEM_SIZE[1] * 0.8)
                    try:
                        font = ImageFont.truetype("Roboto-Bold.ttf", 10)
                    except Exception:
                        font = ImageFont.load_default()
                    text = str(count)
                    bbox = font.getbbox(text)
                    text_width = bbox[2] - bbox[0]
                    text_height = bbox[3] - bbox[1]
                    outline_thickness = 2
                    padding = 4
                    position = (ITEM_SIZE[0] - text_width - padding, ITEM_SIZE[1] - text_height - padding)
                    draw.text(
                        position,
                        text,
                        font=font,
                        fill="Yellow",
                        stroke_width=outline_thickness,
                        stroke_fill="#1e1e1e"
                    )
                    new_image = ImageTk.PhotoImage(base_img)
                    new_image.original = base_img
                    if state != item.get("prev_state"):
                        item["label_widget"].config(image=new_image)
                        item["label_widget"].image = new_image
                        self.flash_item(item)
                        item["prev_state"] = state
                    continue

                # --- Branch for combined_shields ---
                elif key == "combined_shields":
                    if bitwise_data is None:
                        continue
                    state = cfg["get_state"](bitwise_data)
                    if state != item.get("prev_state"):
                        hylian_state, ordon_state = state
                        hylian_path = os.path.join("items", cfg["image_files"]["hylian"])
                        ordon_path = os.path.join("items", cfg["image_files"]["ordon"])
                        hylian_photo = get_photo_image(
                            hylian_path,
                            mode=("colored" if hylian_state == "acquired" else "grey"),
                            size=ITEM_SIZE
                        )
                        ordon_photo = get_photo_image(
                            ordon_path,
                            mode=("colored" if ordon_state == "acquired" else "grey"),
                            size=ITEM_SIZE
                        )
                        hylian_pil = hylian_photo.original
                        ordon_pil = ordon_photo.original
                        combined_pil = Image.new("RGBA", ITEM_SIZE)
                        combined_pil.paste(hylian_pil, (0, 0), hylian_pil)
                        combined_pil.paste(ordon_pil, (0, 0), ordon_pil)
                        new_image = ImageTk.PhotoImage(combined_pil)
                        new_image.original = combined_pil
                        item["label_widget"].config(image=new_image)
                        item["label_widget"].image = new_image
                        self.flash_item(item)
                        item["prev_state"] = state
                    continue

                elif key == "ancient_sky_book":
                    # Read the count of sky characters from address 0x804062B5.
                    try:
                        count = dme.read_byte(0x804062B5)
                    except Exception:
                        count = 0
                    state = count

                    # Load the base image for the sky book.
                    base_path = os.path.join("items", cfg["image_file"])
                    if count == 0:
                        # Use a greyed-out image if there are no sky characters.
                        base_img = get_photo_image(base_path, mode="grey", size=ITEM_SIZE).original
                    else:
                        # Use the colored version otherwise.
                        base_img = Image.open(base_path).convert("RGBA").resize(ITEM_SIZE, Image.LANCZOS)

                    # Overlay the count on the image.
                    draw = ImageDraw.Draw(base_img)
                    font_size = int(ITEM_SIZE[1] * 0.8)
                    try:
                        font = ImageFont.truetype("Roboto-Bold.ttf", 10)
                    except Exception:
                        font = ImageFont.load_default()
                    text = str(count)
                    bbox = font.getbbox(text)
                    text_width = bbox[2] - bbox[0]
                    text_height = bbox[3] - bbox[1]
                    outline_thickness = 2
                    padding = 4
                    # Position the text in the bottom right corner.
                    position = (ITEM_SIZE[0] - text_width - padding, ITEM_SIZE[1] - text_height - padding)
                    draw.text(
                        position,
                        text,
                        font=font,
                        fill="Yellow",
                        stroke_width=outline_thickness,
                        stroke_fill="#1e1e1e"
                    )
                    new_image = ImageTk.PhotoImage(base_img)
                    new_image.original = base_img

                    # Only update the widget if the state has changed.
                    if state != item.get("prev_state"):
                        item["label_widget"].config(image=new_image)
                        item["label_widget"].image = new_image
                        self.flash_item(item)
                        item["prev_state"] = state
                    continue

                # --- Branch for combined_magic_armor ---
                elif key == "combined_magic_armor":
                    if bitwise_data is None:
                        continue
                    state = cfg["get_state"](bitwise_data)
                    if state != item.get("prev_state"):
                        magic_state, zora_state = state
                        magic_path = os.path.join("items", cfg["image_files"]["magic"])
                        zora_path = os.path.join("items", cfg["image_files"]["zora"])
                        magic_photo = get_photo_image(magic_path,
                                                      mode=("colored" if magic_state == "acquired" else "grey"),
                                                      size=ITEM_SIZE)
                        zora_photo = get_photo_image(zora_path,
                                                     mode=("colored" if zora_state == "acquired" else "grey"),
                                                     size=ITEM_SIZE)
                        magic_pil = magic_photo.original
                        zora_pil = zora_photo.original
                        combined_pil = Image.new("RGBA", ITEM_SIZE)
                        combined_pil.paste(magic_pil, (0, 0), magic_pil)
                        combined_pil.paste(zora_pil, (0, 0), zora_pil)
                        new_image = ImageTk.PhotoImage(combined_pil)
                        new_image.original = combined_pil
                        item["label_widget"].config(image=new_image)
                        item["label_widget"].image = new_image
                        self.flash_item(item)
                        item["prev_state"] = state
                    continue

                # --- Other simple branches ---
                elif cfg.get("bitwise"):
                    if bitwise_data is None:
                        continue
                    state = cfg["get_state"](bitwise_data)
                    new_image = item["photo_images"].get(state, item["photo_images"].get("empty"))
                elif key == "clawshot":
                    primary_val = dme.read_byte(cfg["address"])
                    secondary_val = dme.read_byte(cfg["secondary_address"])
                    state = cfg["get_state"](primary_val, secondary_val)
                    new_image = item["photo_images"].get(state, item["photo_images"].get("empty"))
                elif key == "dominion_rod":
                    base_val = dme.read_byte(cfg["address"])
                    powered_val = dme.read_byte(cfg["powered_address"])
                    state = cfg["get_state"](base_val, powered_val)
                    new_image = item["photo_images"].get(state, item["photo_images"].get("empty"))
                else:
                    val = dme.read_byte(cfg["address"])
                    state = cfg["get_state"](val)
                    new_image = item["photo_images"].get(state, item["photo_images"].get("empty"))

                if key not in ["combined_shields", "combined_magic_armor"] and state != item.get("prev_state"):
                    item["label_widget"].config(image=new_image)
                    item["label_widget"].image = new_image
                    self.flash_item(item)
                    item["prev_state"] = state

        except RuntimeError as e:
            print("Memory read failed. Likely the game has closed:", e)
            dme.un_hook()
            if not getattr(self, "connection_lost_called", False):
                self.connection_lost_called = True
                self.connection_lost()
            return

        self.root.after(100, self.update_tracker)

    def connection_lost(self):
        # Destroy the main UI if it exists.
        if hasattr(self, "main_frame") and self.main_frame.winfo_exists():
            self.main_frame.destroy()

        # Create a waiting screen with a dark background.
        waiting_frame = tk.Frame(self.root, bg="#1e1e1e")
        waiting_frame.pack(expand=True, fill="both")

        # Load the waiting disk image.
        waiting_image_path = os.path.join("items", "wait.png")
        try:
            orig_wait_img = Image.open(waiting_image_path).convert("RGBA")
            orig_wait_img = orig_wait_img.resize((200, 200), Image.LANCZOS)
            print("Waiting image loaded for connection lost screen.")
        except Exception as e:
            print("Error loading waiting image:", e)
            orig_wait_img = None

        # Create a label for the animated disk.
        image_label = tk.Label(waiting_frame, bg="#1e1e1e")
        image_label.place(relx=0.5, rely=0.4, anchor="center")
        if orig_wait_img is not None:
            spin_and_float(image_label, orig_wait_img, angle=0, t=0)
        else:
            image_label.config(text="(Waiting image not found)", fg="white", font=("Roboto", 15))

        # Display a text label below the disk.
        waiting_label = tk.Label(waiting_frame,
                              text="Waiting for connection from Dolphin...",
                              font=("Roboto", 15),
                              bg="#1e1e1e",
                              fg="white")
        waiting_label.place(relx=0.5, rely=0.65, anchor="center")

        def try_rehook():
            print("Attempting re-hook...")
            try:
                dme.un_hook()  # Clear any stale connection.
                dme.hook()
                if not dme.is_hooked():
                    raise Exception("Not hooked!")
            except Exception as e:
                print("Re-hook failed, retrying...", e)
                waiting_frame.after(1000, try_rehook)
            else:
                print("Re-hook succeeded!")
                waiting_frame.destroy()
                self.connection_lost_called = False

                # Destroy all existing widgets so we start fresh.
                for widget in self.root.winfo_children():
                    widget.destroy()

                # Create a new Tracker instance, which rebuilds the UI and starts tracking.
                Tracker(self.root)

        try_rehook()


if __name__ == "__main__":
    root = tk.Tk()
    app = Tracker(root)
    root.mainloop()
