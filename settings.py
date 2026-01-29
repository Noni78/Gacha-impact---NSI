import pygame
from character import *
pygame.init()
# ---pity---
pity_5_star = 70
pity_4_star = 0
soft_pity = 73
hard_pity = 90
guaranteed_5_star = False
multi = 10  # Petit conseil ne pas mettre au dessus de 100, et pas en dessous de 5 sinon c'est pas beau
chance_globale = 100/100 # défaut : 100%
proba_init_5_star = 0.006
proba_init_4_star = 0.051
proba_effective_5_star = proba_init_5_star*chance_globale
# --- Screen ---
HEIGHT = 300 #   <------------------------------------------------------------------------------ ici HEIGHT
WIDTH = int(HEIGHT*16/9)
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Totally not a Genshin Impact wishing replica")
pygame.display.set_icon(pygame.image.load("img/icon.png").convert_alpha())
mouse_pos = pygame.mouse.get_pos()
# --- Affichage ---
wish_rarete = None
wish_splash_art = None
animation_progress = 0.0 
# --- Cursor ---
try:
    cursor_img = pygame.image.load("img/Cursor.png").convert_alpha()
    cursor_size = int(HEIGHT * 32 / 900)
    cursor_img = pygame.transform.scale(cursor_img, (cursor_size, cursor_size))
    pygame.mouse.set_visible(False)
    use_custom_cursor = True
except:
    use_custom_cursor = False

# --- Boutons ---
button_height = int(HEIGHT * 60 / 900)
button_width = int(HEIGHT * 200 / 900)
button_spacing = int(HEIGHT * 20 / 900)
button_bottom_margin = int(HEIGHT * 80 / 900)
button_x1_rect = pygame.Rect(WIDTH//2 - button_width - button_spacing//2, HEIGHT - button_bottom_margin, button_width, button_height)
button_multi_rect = pygame.Rect(WIDTH//2 + button_spacing//2, HEIGHT - button_bottom_margin, button_width, button_height)
button_color = (255, 255, 230)
button_hover_color = (200, 200, 170)
# --- Boutons choix bannière ---
banniere_button_width = int(HEIGHT * 200 / 900)
banniere_button_height = int(HEIGHT * 50 / 900)
banniere_button_spacing = int(HEIGHT * 20 / 900)
banniere_buttons = []
for i, char in enumerate(characters["5_star"]):
    rect = pygame.Rect(
        banniere_button_spacing,
        banniere_button_spacing + HEIGHT*65/500 + i * (banniere_button_height + banniere_button_spacing),
        banniere_button_width,
        banniere_button_height
    )
    banniere_buttons.append((rect, char["name"]))
# --- Miscellaenous --- 
font_size = int(HEIGHT * 40 / 900)  
font = pygame.font.Font("font/genshin.ttf", font_size)
button_font_size = int(HEIGHT * 30 / 900)
button_font = pygame.font.Font("font/genshin.ttf", button_font_size)
clock = pygame.time.Clock()
delta_time = 0.1
pity_y = int(HEIGHT * 10 / 900)
pity_y2 = int(HEIGHT * 50 / 900)
pity_y3 = int(HEIGHT * 90 / 900)
pity_x = int(HEIGHT * 20 / 900)
border_thickness = int(HEIGHT * 5 / 900)
border_radius = int(HEIGHT * 10 / 900)