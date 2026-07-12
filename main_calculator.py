import tkinter as tk
import ctypes
import os
import pygame
from PIL import Image, ImageTk, ImageSequence, ImageDraw, ImageChops, ImageFont

# ==========================================
# Windows DPI Fix (prevents window from being
# scaled/cut off on high-DPI displays)
# ==========================================
try:
    ctypes.windll.shcore.SetProcessDpiAwareness(1)
except Exception:
    pass

# ==========================================
# Absolute Path Resolution
# ==========================================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ASSETS_DIR = os.path.join(BASE_DIR, "assets")
IMAGES_DIR = os.path.join(ASSETS_DIR, "images")
SOUNDS_DIR = os.path.join(ASSETS_DIR, "sounds")
FONTS_DIR = os.path.join(ASSETS_DIR, "fonts")
GIFS_DIR = os.path.join(ASSETS_DIR, "gifs")

# ==========================================
# Audio Setup
# ==========================================
pygame.mixer.init()
try:
    pygame.mixer.music.load(os.path.join(SOUNDS_DIR, 'theme.mpeg'))
    pygame.mixer.music.play(-1)
except Exception:
    pass

try:
    click_sound = pygame.mixer.Sound(os.path.join(SOUNDS_DIR, 'buttons.mpeg'))
except Exception:
    click_sound = None

# ==========================================
# Font Setup
# ==========================================
FONT_PATH = os.path.join(FONTS_DIR, "PixelifySans-VariableFont_wght.ttf")

try:
    pil_button_font = ImageFont.truetype(FONT_PATH, 30)
    pil_screen_font = ImageFont.truetype(FONT_PATH, 46)
    print("Pixel font loaded successfully from:", FONT_PATH)
except Exception as e:
    print("Could not load pixel font, falling back to default:", e)
    pil_button_font = ImageFont.load_default()
    pil_screen_font = ImageFont.load_default()

# ==========================================
# Button Grid Sizing
# ==========================================
BTN_W, BTN_H = 94, 74
COL_SPACING = 102
GRID_LEFT = 45
GRID_COLS = [GRID_LEFT + i * COL_SPACING for i in range(4)]

WIDE_BTN_W = (GRID_COLS[3] + BTN_W) - GRID_COLS[2]
WIDE_BTN_X = GRID_COLS[2]

# ==========================================
# Window Setup
# ==========================================
root = tk.Tk()
root.title("Duck Calculator")
root.geometry("600x810")
root.resizable(False, False)

canvas = tk.Canvas(root, width=600, height=810, bg="#E5CA5F", highlightthickness=0)
canvas.pack(fill="both", expand=True)

OFFSET_X = (600 - 490) // 2
OFFSET_Y = (810 - 700) // 2

TITLE_OFFSET_Y = OFFSET_Y
CARD_OFFSET_Y = OFFSET_Y + 40

_image_refs = []


def render_text(text, font, fill="#000000"):
    dummy = Image.new("RGBA", (1, 1))
    draw = ImageDraw.Draw(dummy)
    bbox = draw.textbbox((0, 0), text, font=font)
    w, h = bbox[2] - bbox[0], bbox[3] - bbox[1]
    img = Image.new("RGBA", (max(w, 1) + 8, max(h, 1) + 8), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    draw.text((4 - bbox[0], 4 - bbox[1]), text, font=font, fill=fill)
    photo = ImageTk.PhotoImage(img)
    _image_refs.append(photo)
    return photo


def load_png(filename, resize_to=None, match_height=None, corner_radius=None, opacity=None):
    filepath = os.path.join(IMAGES_DIR, filename)
    try:
        if not os.path.exists(filepath):
            return None
        img = Image.open(filepath).convert("RGBA")
        if match_height:
            aspect = img.width / img.height
            new_height = match_height
            new_width = int(new_height * aspect)
            img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
        elif resize_to:
            img = img.resize(resize_to, Image.Resampling.LANCZOS)
        if opacity is not None:
            alpha = img.split()[-1].point(lambda p: int(p * opacity))
            img.putalpha(alpha)
        if corner_radius:
            mask = Image.new("L", img.size, 0)
            draw = ImageDraw.Draw(mask)
            draw.rounded_rectangle(
                [0, 0, img.size[0] - 1, img.size[1] - 1],
                radius=corner_radius, fill=255
            )
            combined_alpha = ImageChops.multiply(img.split()[-1], mask)
            img.putalpha(combined_alpha)
        return ImageTk.PhotoImage(img)
    except Exception:
        return None


def make_vertical_gradient(width, height, stops, corner_radius=None):
    stops = sorted(stops, key=lambda s: s[0])
    col = Image.new("RGB", (1, height))
    for y in range(height):
        pos = y / max(height - 1, 1)
        if pos <= stops[0][0]:
            color = stops[0][1]
        elif pos >= stops[-1][0]:
            color = stops[-1][1]
        else:
            for i in range(len(stops) - 1):
                p0, c0 = stops[i]
                p1, c1 = stops[i + 1]
                if p0 <= pos <= p1:
                    t = (pos - p0) / (p1 - p0) if p1 > p0 else 0
                    color = tuple(int(c0[j] + (c1[j] - c0[j]) * t) for j in range(3))
                    break
        col.putpixel((0, y), color)
    img = col.resize((width, height), Image.Resampling.NEAREST).convert("RGBA")
    if corner_radius:
        mask = Image.new("L", img.size, 0)
        draw = ImageDraw.Draw(mask)
        draw.rounded_rectangle([0, 0, img.size[0] - 1, img.size[1] - 1], radius=corner_radius, fill=255)
        img.putalpha(mask)
    return ImageTk.PhotoImage(img)


title_img = load_png("calculator_title.png.png", resize_to=(520, 113))
base_img = load_png("calculator_base.png", resize_to=(432, 598), corner_radius=25, opacity=0.75)


def make_button_face(w, h, corner_radius=14, face_color="#D6D9DE",
                      shadow_color="#F2C94C", outline_color="#111111",
                      outline_width=3, shadow_offset=5):
    img = Image.new("RGBA", (w + shadow_offset, h + shadow_offset), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    draw.rounded_rectangle(
        [shadow_offset, shadow_offset, w - 1 + shadow_offset, h - 1 + shadow_offset],
        radius=corner_radius, fill=shadow_color
    )
    draw.rounded_rectangle([0, 0, w - 1, h - 1], radius=corner_radius,
                            fill=face_color, outline=outline_color, width=outline_width)
    photo = ImageTk.PhotoImage(img)
    _image_refs.append(photo)
    return photo


def get_average_color(filename):
    filepath = os.path.join(IMAGES_DIR, filename)
    try:
        img = Image.open(filepath).convert("RGBA")
        cx, cy = img.width // 2, img.height // 2
        r, g, b, a = img.getpixel((cx, cy))
        return f"#{r:02x}{g:02x}{b:02x}"
    except Exception:
        return "#D6D9DE"
btn_bg_img = make_button_face(BTN_W, BTN_H)   # same style as "=" now
btn_wide_img = make_button_face(WIDE_BTN_W, BTN_H)



background_img = make_vertical_gradient(
    600, 810,
    [(0.14, (0xF2, 0xE4, 0xAF)), (0.48, (0xFF, 0xFF, 0xFF)), (1.0, (0xE5, 0xCA, 0x5F))]
)

raw_gif_frames = []
try:
    gif_path = os.path.join(GIFS_DIR, 'baby-duck.gif')
    gif = Image.open(gif_path)
    canvas_frame = Image.new("RGBA", gif.size, (0, 0, 0, 0))
    for i in range(gif.n_frames):
        gif.seek(i)
        this_frame = gif.convert("RGBA")
        canvas_frame.paste(this_frame, (0, 0), this_frame)
        composed = canvas_frame.copy().resize((65, 65), Image.Resampling.NEAREST)
        raw_gif_frames.append(composed)
except Exception:
    pass


def build_rotated_frames(angle, opacity=1.0):
    if not raw_gif_frames:
        return []
    pil_angle = -angle
    frames = []
    for f in raw_gif_frames:
        rotated = f.rotate(pil_angle, expand=True, resample=Image.BICUBIC)
        if opacity < 1.0:
            alpha = rotated.split()[-1].point(lambda p: int(p * opacity))
            rotated.putalpha(alpha)
        frames.append(ImageTk.PhotoImage(rotated))
    return frames


DUCK_LEFT_X_OUTER = 25
DUCK_LEFT_X_INNER = 55
DUCK_RIGHT_X_OUTER = 575
DUCK_RIGHT_X_INNER = 545

DUCK_TOP_Y = 160
DUCK_BOTTOM_Y = 780
DUCK_GAP = 130

duck_specs = []
row_index = 0
y = DUCK_TOP_Y
while y <= DUCK_BOTTOM_Y:
    if row_index % 2 == 0:
        left_x, right_x = DUCK_LEFT_X_OUTER, DUCK_RIGHT_X_OUTER
    else:
        left_x, right_x = DUCK_LEFT_X_INNER, DUCK_RIGHT_X_INNER
    duck_specs.append((left_x, y, 0, 100))
    duck_specs.append((right_x, y, 0, 100))
    y += DUCK_GAP
    row_index += 1

# A few extra ducks tucked right at the card's corners, peeking out
# from behind it. These work because ducks are drawn BEFORE the card
# in draw_ui() -- so the card naturally covers most of them, leaving
# just an edge peeking out, like your Figma reference.
CARD_LEFT, CARD_RIGHT = 84, 516
CARD_TOP, CARD_BOTTOM = 171, 769

duck_specs.append((CARD_LEFT + 10, CARD_TOP + 15, 0, 100))     # top-left, peeking
duck_specs.append((CARD_RIGHT - 10, CARD_TOP + 15, 0, 100))    # top-right, peeking
duck_specs.append((CARD_LEFT + 10, CARD_BOTTOM - 15, 0, 100))  # bottom-left, peeking
duck_specs.append((CARD_RIGHT - 10, CARD_BOTTOM - 15, 0, 100)) # bottom-right, peeking


duck_frame_sets = [build_rotated_frames(angle, opacity / 100) for (_, _, angle, opacity) in duck_specs] if raw_gif_frames else []

current_expression = "0"
screen_text = None
screen_text_x = 0
screen_text_y = 0


def handle_click(value):
    global current_expression
    if click_sound:
        click_sound.play()

    if value == "AC":
        current_expression = "0"
    elif value == "=":
        try:
            expr = current_expression.replace("X", "*").replace("÷", "/")
            expr = expr.replace("%", "/100")
            current_expression = str(eval(expr))
            if current_expression.endswith(".0"):
                current_expression = current_expression[:-2]
        except Exception:
            current_expression = "Error"
    elif value == "±":
        if current_expression not in ("0", "Error"):
            if current_expression.startswith("-"):
                current_expression = current_expression[1:]
            else:
                current_expression = "-" + current_expression
    elif value == "%":
        if current_expression not in ("0", "Error") and not current_expression.endswith("%"):
            current_expression += value
    elif value == ".":
        last_number = current_expression.replace("+", " ").replace("-", " ") \
                                         .replace("X", " ").replace("÷", " ").split()[-1] \
                                         if current_expression not in ("0", "Error") else "0"
        if "." not in last_number:
            if current_expression in ("0", "Error"):
                current_expression = "0."
            else:
                current_expression += value
    else:
        if current_expression == "0" or current_expression == "Error":
            current_expression = value
        else:
            current_expression += value

    new_img = render_text(current_expression, pil_screen_font)
    canvas.itemconfig(screen_text, image=new_img)
    canvas.coords(screen_text, screen_text_x, screen_text_y)


def draw_ui():
    global duck_sprites, screen_text, screen_text_x, screen_text_y
    duck_sprites = []

    if background_img:
        canvas.create_image(0, 0, image=background_img, anchor="nw")

    if raw_gif_frames:
        for i, (x, y, angle, opacity) in enumerate(duck_specs):
            frames = duck_frame_sets[i]
            sprite = canvas.create_image(x, y, image=frames[0])
            duck_sprites.append(sprite)

    if base_img:
        canvas.create_image(245 + OFFSET_X, 375 + CARD_OFFSET_Y, image=base_img, anchor="center")
    else:
        canvas.create_rectangle(29 + OFFSET_X, 76 + CARD_OFFSET_Y, 461 + OFFSET_X, 674 + CARD_OFFSET_Y, fill="#D9C15B", outline="")

    if title_img:
        canvas.create_image(245 + OFFSET_X, 45 + TITLE_OFFSET_Y, image=title_img, anchor="center")
    else:
        title_text_img = render_text("CALCULATOR", pil_screen_font)
        canvas.create_image(245 + OFFSET_X, 45 + TITLE_OFFSET_Y, image=title_text_img)

    screen_x1, screen_y1, screen_x2, screen_y2 = 45 + OFFSET_X, 110 + CARD_OFFSET_Y, 445 + OFFSET_X, 215 + CARD_OFFSET_Y
    screen_w, screen_h = screen_x2 - screen_x1, screen_y2 - screen_y1

    screen_stops = [
        (0.0, (0x67, 0xC6, 0xD9)),
        (0.34, (0xBF, 0xCA, 0xCC)),
        (0.67, (0xBF, 0xCA, 0xCC)),
        (1.0, (0x67, 0xC6, 0xD9)),
    ]
    screen_gradient_img = make_vertical_gradient(screen_w, screen_h, screen_stops, corner_radius=19)
    _image_refs.append(screen_gradient_img)
    canvas.create_image(screen_x1, screen_y1, image=screen_gradient_img, anchor="nw")

    screen_text_x, screen_text_y = screen_x2 - 25, (screen_y1 + screen_y2) / 2
    screen_img = render_text(current_expression, pil_screen_font)
    screen_text = canvas.create_image(screen_text_x, screen_text_y, image=screen_img, anchor="e")

    build_buttons()


def create_image_button(x, y, text, is_wide=False):
    img = btn_wide_img if is_wide else btn_bg_img
    TEXT_NUDGE_X, TEXT_NUDGE_Y = 6, 6

    if img:
        w, h = img.width(), img.height()
        btn_id = canvas.create_image(x, y, image=img, anchor="nw")
        text_img = render_text(text, pil_button_font)
        text_id = canvas.create_image(x + (w / 2) + TEXT_NUDGE_X, y + (h / 2) + TEXT_NUDGE_Y, image=text_img)
    else:
        w, h = (180, 60) if is_wide else (80, 60)
        btn_id = canvas.create_rectangle(x, y, x + w, y + h, fill="#EAEAEA", outline="")
        text_img = render_text(text, pil_button_font)
        text_id = canvas.create_image(x + (w / 2), y + (h / 2), image=text_img)

    PRESS_OFFSET = 3
    ids = (btn_id, text_id)

    def on_press(event, ids=ids):
        for obj in ids:
            canvas.move(obj, PRESS_OFFSET, PRESS_OFFSET)

    def on_release(event, t=text, ids=ids):
        for obj in ids:
            canvas.move(obj, -PRESS_OFFSET, -PRESS_OFFSET)
        handle_click(t)

    for obj in ids:
        canvas.tag_bind(obj, "<ButtonPress-1>", on_press)
        canvas.tag_bind(obj, "<ButtonRelease-1>", on_release)


def build_buttons():
    c0, c1, c2, c3 = GRID_COLS
    row_ys = [248, 331, 414, 497, 580]

    normal_layout = [
        ('AC', c0, row_ys[0]), ('±', c1, row_ys[0]), ('%', c2, row_ys[0]), ('÷', c3, row_ys[0]),
        ('1', c0, row_ys[1]),  ('2', c1, row_ys[1]),  ('3', c2, row_ys[1]),  ('X', c3, row_ys[1]),
        ('4', c0, row_ys[2]),  ('5', c1, row_ys[2]),  ('6', c2, row_ys[2]),  ('.', c3, row_ys[2]),
        ('7', c0, row_ys[3]),  ('8', c1, row_ys[3]),  ('9', c2, row_ys[3]),  ('+', c3, row_ys[3]),
        ('-', c0, row_ys[4]),  ('0', c1, row_ys[4]),
    ]
    for (text, x, y) in normal_layout:
        create_image_button(x + OFFSET_X, y + CARD_OFFSET_Y, text, is_wide=False)

    create_image_button(WIDE_BTN_X + OFFSET_X, row_ys[4] + CARD_OFFSET_Y, '=', is_wide=True)


gif_index = 0


def update_gif():
    global gif_index
    if raw_gif_frames and duck_sprites:
        for sprite, frames in zip(duck_sprites, duck_frame_sets):
            canvas.itemconfig(sprite, image=frames[gif_index % len(frames)])
        gif_index = (gif_index + 1) % len(raw_gif_frames)
        root.after(140, update_gif)


draw_ui()

if raw_gif_frames:
    update_gif()

root.mainloop()