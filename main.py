import os
import math
import tkinter as tk
from PIL import Image, ImageTk, ImageOps
from config import WINDOW_GEOMETRY  # Ensure this is defined in your config.
import dolphin_memory_engine as dme
from tracker import Tracker  # Import your Tracker class


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


def main():
    root = tk.Tk()
    root.geometry(WINDOW_GEOMETRY)
    root.configure(bg="#1e1e1e")

    # Create a waiting frame.
    waiting_frame = tk.Frame(root, bg="#1e1e1e")
    waiting_frame.pack(expand=True, fill="both")

    # Load the waiting image (e.g., a GameCube disk).
    waiting_image_path = os.path.join("items", "wait.png")  # Adjust filename if needed.
    try:
        orig_wait_img = Image.open(waiting_image_path).convert("RGBA")
        print("Waiting image loaded.")
        # Resize the image to a suitable size (e.g., 100x100 pixels).
        orig_wait_img = orig_wait_img.resize((200, 200), Image.LANCZOS)
    except Exception as e:
        print("Error loading waiting image:", e)
        orig_wait_img = None

    # Create a label for the waiting image and place it at the center.
    image_label = tk.Label(waiting_frame, bg="#1e1e1e")
    image_label.place(relx=0.5, rely=0.4, anchor="center")
    if orig_wait_img is not None:
        spin_and_float(image_label, orig_wait_img, angle=0, t=0)
    else:
        image_label.config(text="(Waiting image not found)", fg="white", font=("Roboto", 15))

    # Create a label for the waiting text and place it below the image.
    text_label = tk.Label(waiting_frame,
                          text="Waiting for connection from Dolphin...",
                          font=("Roboto", 15),
                          bg="#1e1e1e",
                          fg="white")
    text_label.place(relx=0.5, rely=0.65, anchor="center")

    def try_hook():
        try:
            dme.hook()  # Attempt to hook to Dolphin.
            if not dme.is_hooked():
                raise Exception("Not hooked!")
        except Exception as e:
            root.after(1000, try_hook)
        else:
            waiting_frame.destroy()
            Tracker(root)

    try_hook()
    root.mainloop()


if __name__ == "__main__":
    main()
