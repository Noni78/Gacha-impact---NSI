import json
import random

import cv2
import pygame

from character import *
from settings import *

pygame.init()

#####################
# --- Affichage --- #
#####################


def scale_to_height(image, target_height):
    w, h = image.get_size()
    scale_factor = target_height / h
    new_w = int(w * scale_factor)
    new_h = target_height
    return pygame.transform.scale(image, (new_w, new_h))


def scale_to_cover(image, target_width, target_height):
    w, h = image.get_size()
    scale_factor = max(target_width / w, target_height / h)
    new_w = int(w * scale_factor)
    new_h = int(h * scale_factor)
    return pygame.transform.scale(image, (new_w, new_h))


def scale_with_borders(image, target_width, target_height, border_percent=15):
    border_w = int(target_width * border_percent / 100)
    border_h = int(target_height * border_percent / 100)
    new_width = target_width - (2 * border_w)
    new_height = target_height - (2 * border_h)
    return pygame.transform.scale(image, (new_width, new_height)), border_w, border_h


def draw_banniere_buttons(screen, mouse_pos, banniere_buttons, button_font):
    for rect, name in banniere_buttons:
        color = (140, 140, 110) if rect.collidepoint(mouse_pos) else (178, 180, 140)
        pygame.draw.rect(screen, color, rect, border_radius=5)
        text_surf = button_font.render(name, True, (78, 80, 40))
        text_rect = text_surf.get_rect(center=rect.center)
        screen.blit(text_surf, text_rect)


def animer_splash_art(screen, splash_art, progress=1.0, clamp_to_screen=False):
    """
    'anime' le splash art

    Args:
        screen: surface pygame
        splash_art: image du personnage
        WIDTH (int): largeur de la surface
        HEIGHT (int): hauteru de la surface
        progress (float): progression de l'animation de 0 a 1
    """
    scale_factor = 2 - (0.6 * min(progress, 1))

    new_width = int(splash_art.get_width() * scale_factor)
    new_height = int(splash_art.get_height() * scale_factor)

    if clamp_to_screen:
        max_width = int(WIDTH * 0.95)
        max_height = int(HEIGHT * 0.95)
        if new_width > max_width or new_height > max_height:
            ratio = min(max_width / new_width, max_height / new_height)
            new_width = int(new_width * ratio)
            new_height = int(new_height * ratio)

    scaled_splash = pygame.transform.scale(splash_art, (new_width, new_height))

    x = WIDTH // 2 - scaled_splash.get_width() // 2
    y = HEIGHT // 2 - scaled_splash.get_height() // 2

    alpha = int(255 * min(progress, 1))
    scaled_splash.set_alpha(alpha)
    screen.blit(scaled_splash, (x, y))


def darken(rgb, coefficient=0.5):
    """
    Assombrit une couleur

    Args:
        rgb (tuple): couleur a assombrir
    """
    return tuple(int(i * coefficient) for i in rgb)


def get_color(rare):
    """
    Couleur en fonctions de la rarete

    args:
        rare (str): rarete du tirage
    """
    if rare in ["5_star", "5_star_perma"]:
        return (220, 190, 20)
    if rare == "4_star":
        return (120, 60, 185)
    return (80, 140, 225)


def play_video(video_path, screen, loop=False):
    """
    Lit et affiche video sur ecran, complique et trouve sur internet --> NE PAS TOUCHER
    """
    cap = cv2.VideoCapture(video_path)

    if not cap.isOpened():
        print(f"Erreur: Impossible d'ouvrir la video {video_path}")
        return True

    fps = cap.get(cv2.CAP_PROP_FPS)
    if fps == 0 or fps > 120:
        fps = 30

    clock = pygame.time.Clock()
    playing = True
    frame_count = 0

    while playing:
        ret, frame = cap.read()
        if not ret:
            if loop:
                cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
                frame_count = 0
                ret, frame = cap.read()
                if not ret:
                    break
            else:
                break

        frame_count += 1
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame = cv2.resize(frame, (WIDTH, HEIGHT))
        frame = frame.swapaxes(0, 1)
        frame = pygame.surfarray.make_surface(frame)

        screen.fill((0, 0, 0))
        screen.blit(frame, (0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                playing = False
                cap.release()
                return False
            if event.type == pygame.KEYDOWN and event.key in (pygame.K_ESCAPE, pygame.K_SPACE):
                playing = False

        pygame.display.flip()
        clock.tick(fps)

    cap.release()
    return True


def weapon_background_path(weapon):
    """
    Donne le chemin de l'image de fond selon le type d'arme.
    Args:
        weapon (str): type d'arme ("sword", "claymore", "polearm", "bow", "catalyst")
    """
    return pygame.image.load(f"img/Weapon_Background/{weapon}.png").convert_alpha()


def draw_button(screen, rect, text, mouse_pos, hover_color, color, font):
    """Dessine bouton

    args:
    screen : surface pygame
    rect: rectangle (dimension etc)
    text: texte sur le bouton
    mous_pos: positions de la souris
    hover_color: couleur quand souris sur bouton
    color: couleur de base en RGB
    """
    if rect.collidepoint(mouse_pos):
        color = hover_color

    border_radius = int(HEIGHT * 30 / 900)
    border_width = int(HEIGHT * 3 / 900)

    pygame.draw.rect(screen, color, rect, border_radius=border_radius)
    pygame.draw.rect(screen, (180, 178, 178), rect, border_width, border_radius=border_radius)

    text_surface = font.render(text, True, (183, 167, 155))
    text_rect = text_surface.get_rect(center=rect.center)
    screen.blit(text_surface, text_rect)


def afficher_banniere(screen, banniere, banner_border_w, banner_border_h, border_thickness, border_radius):
    border_rect = pygame.Rect(
        banner_border_w - border_thickness,
        banner_border_h - border_thickness,
        banniere.get_width() + (border_thickness * 2),
        banniere.get_height() + (border_thickness * 2),
    )
    pygame.draw.rect(screen, (178, 180, 166), border_rect, border_thickness, border_radius=border_radius)
    screen.blit(banniere, (banner_border_w, banner_border_h))


def boutons(
    screen,
    mouse_pos,
    button_x1,
    button_multi,
    button_save,
    multi,
    banniere_buttons,
    button_hover_color,
    button_color,
    button_font,
):
    draw_button(screen, button_x1, "Voeu x1", mouse_pos, button_hover_color, button_color, button_font)
    draw_button(screen, button_multi, f"Voeu x{multi}", mouse_pos, button_hover_color, button_color, button_font)
    draw_button(screen, button_save, "Save", mouse_pos, button_hover_color, button_color, button_font)
    draw_banniere_buttons(screen, mouse_pos, banniere_buttons, button_font)


def afficher_souris():
    mouse_pos = pygame.mouse.get_pos()
    cursor_x = mouse_pos[0] - cursor_img.get_width() // 2
    cursor_y = mouse_pos[1] - cursor_img.get_height() // 2
    screen.blit(cursor_img, (cursor_x, cursor_y))


###################
# --- Calculs --- #
###################


def rarete(pity_5, pity_4, proba_5=0.006, proba_4=0.051, chance=1.0, soft_pity=70, hard_pity=90):
    """
    Calcule la rarete d'un tirage sans modifier les compteurs de pity.

    Returns:
        str: "5_star", "4_star" ou "3_star" selon le tirage aleatoire pondere.
    """
    weight_5_star = proba_5 * chance
    weight_4_star = proba_4 * chance

    if pity_5 >= hard_pity:
        return "5_star"
    if pity_4 >= 9:
        return "4_star"
    if pity_5 > soft_pity:
        weight_5_star += (pity_5 - soft_pity) * ((1 - proba_5) / (hard_pity - soft_pity))

    weight_5_star = min(weight_5_star, 1 - weight_4_star)
    weight_3_star = 1 - weight_4_star - weight_5_star
    return random.choices(["5_star", "4_star", "3_star"], [weight_5_star, weight_4_star, weight_3_star])[0]


def wish(pity_5_star, pity_4_star, garanti, current_banner_index, stack_capture_radiance, soft_pity=73, hard_pity=90):
    """
    Effectue 1 voeu et retourne tous les resultats.
    """
    wish_rarete = rarete(
        pity_5_star,
        pity_4_star,
        proba_init_5_star,
        proba_init_4_star,
        chance_globale,
        soft_pity,
        hard_pity,
    )
    new_pity_5_star = pity_5_star
    new_pity_4_star = pity_4_star
    new_garanti = garanti
    new_stack_capture_radiance = stack_capture_radiance
    capture_radiance = False

    if wish_rarete == "5_star":
        if stack_capture_radiance < 2:
            print("<--5050 en cours-->")
            if not garanti:
                if random.random() <= 0.5:
                    new_garanti = False
                    new_stack_capture_radiance = max(0, stack_capture_radiance - 1)
                else:
                    new_garanti = True
                    wish_rarete = "5_star_perma"
                    new_stack_capture_radiance = stack_capture_radiance + 1
            else:
                new_garanti = False
                new_stack_capture_radiance = max(0, stack_capture_radiance - 1)
        elif stack_capture_radiance == 2:
            print("<-- 5545 en cours -->")
            if random.random() <= 0.55:
                new_garanti = False
                capture_radiance = True
                new_stack_capture_radiance = 1
            else:
                new_garanti = True
                wish_rarete = "5_star_perma"
                new_stack_capture_radiance = 3
        else:
            print("<-- Vous avez si peu de chance que je vous fait gagner celui la -->")
            new_garanti = False
            capture_radiance = True
            new_stack_capture_radiance = 1

    if wish_rarete == "4_star":
        featured_4_stars = characters["5_star"][current_banner_index].get("featured_4_star", [])
        if featured_4_stars and random.random() < 0.8:
            featured_chars = [c for c in characters["4_star"] if c["name"] in featured_4_stars]
            wish_result_character = random.choice(featured_chars)
        else:
            non_featured_chars = [c for c in characters["4_star"] if c["name"] not in featured_4_stars]
            wish_result_character = random.choice(non_featured_chars) if non_featured_chars else random.choice(characters["4_star"])
    elif wish_rarete == "5_star":
        wish_result_character = characters["5_star"][current_banner_index]
    else:
        wish_result_character = random.choice(characters[wish_rarete])

    if wish_rarete in ("5_star", "5_star_perma"):
        new_pity_5_star = 0
        new_pity_4_star += 1
        wish_animation = "videos/capture_radiance.gif" if capture_radiance else "videos/pull_5_star.mp4"
    elif wish_rarete == "4_star":
        wish_animation = "videos/pull_4_star.mp4"
        new_pity_4_star = 0
        new_pity_5_star += 1
    else:
        wish_animation = "videos/pull_3_star.mp4"
        new_pity_5_star += 1
        new_pity_4_star += 1

    splash_image = pygame.image.load(wish_result_character["image"]).convert_alpha()
    if wish_result_character["type"] is None:
        wish_splash_art = scale_to_height(splash_image, HEIGHT)
    else:
        # Arme: base un peu reduite pour garder l'animation de "retrait"
        # sans paraitre trop petite.
        wish_splash_art = scale_to_height(splash_image, int(HEIGHT * 0.62))
    return {
        "rarete": wish_rarete,
        "character": wish_result_character,
        "animation": wish_animation,
        "splash_art": wish_splash_art,
        "new_pity_5_star": new_pity_5_star,
        "new_pity_4_star": new_pity_4_star,
        "new_garanti": new_garanti,
        "new_stack_capture_radiance": new_stack_capture_radiance,
    }


################
# --- Save --- #
################


def sauvegarder(pity_5, pity_4, garanti, banner_index, stack_capture_radiance, nom_fichier="save/save.json"):
    """
    Sauvegarde les donnees de pity dans un fichier JSON.
    """
    donnees = {
        "data": [
            {"pity_5_star": pity_5},
            {"pity_4_star": pity_4},
            {"garanti": str(garanti)},
            {"current_banner_index": banner_index},
            {"stack_capture_radiance": stack_capture_radiance},
        ]
    }

    with open(nom_fichier, "w", encoding="utf-8") as f:
        json.dump(donnees, f, indent=4, ensure_ascii=False)

    print(f"Donnees sauvegardees dans {nom_fichier}")

