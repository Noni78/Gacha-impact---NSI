import pygame
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
