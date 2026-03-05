import json
import os
import sys

import pygame

from character import *

pygame.init()


def _default_save_data():
    return {
        "data": [
            {"pity_5_star": 0},
            {"pity_4_star": 0},
            {"garanti": False},
            {"current_banner_index": 0},
            {"stack_capture_radiance": 0},
        ]
    }


def _as_bool(value):
    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        return value.strip().lower() in ("1", "true", "yes", "oui")
    return bool(value)


def _normalize_save_data(raw_data):
    default = _default_save_data()
    data_list = raw_data.get("data", []) if isinstance(raw_data, dict) else []

    def pick(index, key, fallback):
        if index < len(data_list) and isinstance(data_list[index], dict):
            return data_list[index].get(key, fallback)
        return fallback

    pity_5 = int(pick(0, "pity_5_star", default["data"][0]["pity_5_star"]))
    pity_4 = int(pick(1, "pity_4_star", default["data"][1]["pity_4_star"]))
    garanti = _as_bool(pick(2, "garanti", default["data"][2]["garanti"]))
    current_banner_index = int(pick(3, "current_banner_index", default["data"][3]["current_banner_index"]))
    stack_capture_radiance = int(pick(4, "stack_capture_radiance", default["data"][4]["stack_capture_radiance"]))

    pity_5 = max(0, pity_5)
    pity_4 = max(0, pity_4)
    current_banner_index = max(0, min(current_banner_index, len(characters["5_star"]) - 1))
    stack_capture_radiance = max(0, stack_capture_radiance)

    return {
        "data": [
            {"pity_5_star": pity_5},
            {"pity_4_star": pity_4},
            {"garanti": garanti},
            {"current_banner_index": current_banner_index},
            {"stack_capture_radiance": stack_capture_radiance},
        ]
    }


def _save_directory():
    if getattr(sys, "frozen", False):
        return os.path.dirname(sys.executable)
    return os.path.dirname(os.path.abspath(__file__))


SAVE_FILE = os.path.join(_save_directory(), "save.json")
LEGACY_SAVE_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "save", "save.json")


def _load_or_create_save():
    default_data = _default_save_data()

    if not os.path.exists(SAVE_FILE) and os.path.exists(LEGACY_SAVE_FILE):
        try:
            with open(LEGACY_SAVE_FILE, encoding="utf-8") as f:
                legacy_data = _normalize_save_data(json.load(f))
            with open(SAVE_FILE, "w", encoding="utf-8") as f:
                json.dump(legacy_data, f, indent=4, ensure_ascii=False)
            return legacy_data
        except (OSError, json.JSONDecodeError, ValueError, TypeError):
            pass

    if not os.path.exists(SAVE_FILE):
        with open(SAVE_FILE, "w", encoding="utf-8") as f:
            json.dump(default_data, f, indent=4, ensure_ascii=False)
        return default_data

    try:
        with open(SAVE_FILE, encoding="utf-8") as f:
            loaded = _normalize_save_data(json.load(f))
        with open(SAVE_FILE, "w", encoding="utf-8") as f:
            json.dump(loaded, f, indent=4, ensure_ascii=False)
        return loaded
    except (OSError, json.JSONDecodeError, ValueError, TypeError):
        with open(SAVE_FILE, "w", encoding="utf-8") as f:
            json.dump(default_data, f, indent=4, ensure_ascii=False)
        return default_data


data = _load_or_create_save()

################
# --- pity --- #
################

pity_5_star = data["data"][0]["pity_5_star"]
pity_4_star = data["data"][1]["pity_4_star"]
soft_pity = 73
hard_pity = 90
garanti = data["data"][2]["garanti"]
stack_capture_radiance = data["data"][4]["stack_capture_radiance"]
multi = 10  # Petit conseil: ne pas mettre au-dessus de 100, ni en dessous de 5.
chance_globale = 100 / 100  # 100%
proba_init_5_star = 0.006
proba_init_4_star = 0.051
proba_effective_5_star = proba_init_5_star * chance_globale

####################
# --- Affichage --- #
####################

HEIGHT = 810
WIDTH = int(HEIGHT * 16 / 9)
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("Totally not a Genshin Impact wishing replica")
pygame.display.set_icon(pygame.image.load("img/icon.png").convert_alpha())
mouse_pos = pygame.mouse.get_pos()
wish_rarete = None
wish_splash_art = None
animation_progress = 0.0
force_ratio_16_9 = False  # Passe a True pour forcer le ratio 16:9

# --- Cursor --- #
try:
    cursor_img = pygame.image.load("img/Cursor.png").convert_alpha()
    cursor_size = int(HEIGHT * 32 / 900)
    cursor_img = pygame.transform.scale(cursor_img, (cursor_size, cursor_size))
    pygame.mouse.set_visible(False)
    use_custom_cursor = True
except Exception:
    use_custom_cursor = False

# --- Boutons --- #
button_height = int(HEIGHT * 60 / 900)
button_width = int(HEIGHT * 200 / 900)
button_spacing = int(HEIGHT * 20 / 900)
button_bottom_margin = int(HEIGHT * 80 / 900)
button_x1 = pygame.Rect(WIDTH // 2 - button_width - button_spacing // 2, HEIGHT - button_bottom_margin, button_width, button_height)
button_multi = pygame.Rect(WIDTH // 2 + button_spacing // 2, HEIGHT - button_bottom_margin, button_width, button_height)
button_save = pygame.Rect(WIDTH - button_width - button_spacing // 1.5, button_spacing // 1.5, button_width, button_height)
button_color = (255, 255, 230)
button_hover_color = (200, 200, 170)

# --- Boutons choix banniere --- #
banniere_button_width = int(HEIGHT * 200 / 900)
banniere_button_height = int(HEIGHT * 50 / 900)
banniere_button_spacing = int(HEIGHT * 20 / 900)
banniere_buttons = []
for i, char in enumerate(characters["5_star"]):
    rect = pygame.Rect(
        banniere_button_spacing,
        banniere_button_spacing + HEIGHT * 65 / 500 + i * (banniere_button_height + banniere_button_spacing),
        banniere_button_width,
        banniere_button_height,
    )
    banniere_buttons.append((rect, char["name"]))

#########################
# --- Miscellaneous --- #
#########################

font_size = int(HEIGHT * 40 / 900)
font = pygame.font.Font("font/genshin.ttf", font_size)
button_font_size = int(HEIGHT * 30 / 900)
button_font = pygame.font.Font("font/genshin.ttf", button_font_size)
clock = pygame.time.Clock()
delta_time = 0.1
pity_y = int(HEIGHT * 10 / 900)
pity_y2 = int(HEIGHT * 50 / 900)
pity_y3 = int(HEIGHT * 90 / 900)
capture_radiance_y = int(HEIGHT * 840 / 900)
capture_radiance_x = int(HEIGHT * 20 / 900)
pity_x = int(HEIGHT * 20 / 900)
border_thickness = int(HEIGHT * 5 / 900)
border_radius = int(HEIGHT * 10 / 900)
current_banner_index = data["data"][3]["current_banner_index"]
banniere_path = characters["5_star"][current_banner_index]["banniere"]
