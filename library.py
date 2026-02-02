import pygame
import random
import cv2
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

def scale_with_borders(image, target_width, target_height, border_percent=15):
    border_w = int(target_width * border_percent / 100)
    border_h = int(target_height * border_percent / 100)
    new_width = target_width - (2 * border_w)
    new_height = target_height - (2 * border_h)
    return pygame.transform.scale(image, (new_width, new_height)), border_w, border_h

def draw_banniere_buttons(screen, mouse_pos, banniere_buttons,button_font):
    for rect, name in banniere_buttons:
        color = (140, 140, 110) if rect.collidepoint(mouse_pos) else (178, 180, 140)
        pygame.draw.rect(screen, color, rect, border_radius=5)
        text_surf = button_font.render(name, True, (78, 80, 40))
        text_rect = text_surf.get_rect(center=rect.center)
        screen.blit(text_surf, text_rect)

def animer_splash_art(screen, splash_art,progress=1.0):
    """
    'anime' le splash art
    
    Args:
        screen: surface pygame
        splash_art: image du personnage
        WIDTH (int): largeur de la surface
        HEIGHT (int): hauteru de la surface
        progress (float): progression de l'animation de 0 à 1
    """
    scale_factor = 2 - (0.6 * min(progress, 1))
    
    new_width = int(splash_art.get_width() * scale_factor)
    new_height = int(splash_art.get_height() * scale_factor)
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
            rgb (tuple): couleur à assombrir
        """
        return tuple(int(i * coefficient) for i in rgb)

def get_color(rare):

    """
    Couleur en fonctions de la rareté

    args:
        rare (str): rareté du tirage
    """
    if rare in ["5_star", "5_star_perma"]:
        return (220, 190, 20)
    if rare == "4_star":
        return (120, 60, 185)
    return (80, 140, 225)

def play_video(video_path, screen,loop=False):
    """
    Lit et affiche vidéo sur écran, compliqué et trouvé sur internet --> NE PAS TOUCHER
    """
    cap = cv2.VideoCapture(video_path)
    
    if not cap.isOpened():
        print(f"Erreur: Impossible d'ouvrir la vidéo {video_path}")
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
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE or event.key == pygame.K_SPACE:
                    playing = False
        
        pygame.display.flip()
        clock.tick(fps)

    cap.release()
    #print("Vidéo terminée")
    return True

def weapon_background_path(weapon):
    """
    Donne le chemin de l'image de fond selon le type d'arme.
    Args:
        weapon (str): type d'arme ("sword", "claymore", "polearm", "bow", "catalyst")
    """
    return pygame.image.load(f"img/Weapon_Background/{weapon}.png").convert_alpha()

def draw_button(screen, rect, text, mouse_pos,hover_color,color,font):
    """Dessine bouton
    
    args :
    screen : surface pygame
    rect: rectangle (dimension etc)
    text (float): texte sur le bouton
    mous_pos: positions de la souris
    hover_color: couleur quans souris sur bouton
    color: couleur de base en RGB
    """
    if rect.collidepoint(mouse_pos):
        color = hover_color
    else:
        color = color
    
    border_radius = int(HEIGHT * 30 / 900)
    border_width = int(HEIGHT * 3 / 900)
    
    pygame.draw.rect(screen, color, rect, border_radius=border_radius)
    pygame.draw.rect(screen, (180, 178, 178), rect, border_width, border_radius=border_radius) 
    
    text = font.render(text, True, (183, 167, 155))
    text_rect = text.get_rect(center=rect.center)
    screen.blit(text, text_rect)

def afficher_souris():
    mouse_pos = pygame.mouse.get_pos()
    cursor_x = mouse_pos[0] - cursor_img.get_width() // 2 
    cursor_y = mouse_pos[1] - cursor_img.get_height() // 2
    screen.blit(cursor_img, (cursor_x, cursor_y))

###################
# --- Calculs --- #
###################

def rarete(pity_5, pity_4, proba_5=0.006, proba_4=0.051,chance=1.0,soft_pity=70, hard_pity=90):
    """
    Calcule la rareté d'un tirage sans modifier les compteurs de pity.
    
    Args:
        pity_5_star (int): compteur actuel pity 5★
        pity_4_star (int): compteur actuel pity 4★
        proba_5 (float): probabilité d'avoir  un perso 5★
        proba_4 (float): probabilité d'avoir  un perso 4★
        chance (float): chance
        soft_pity (int, optional): début de la soft pity pour 5★
        hard_pity (int, optional): hard pity pour 5★

    Returns:
        str: "5_star", "4_star" ou "3_star" selon le tirage aléatoire pondéré.
    """
    weight_5_star = proba_5*chance
    weight_4_star = proba_4*chance
    if pity_5 >= hard_pity:
        return "5_star"
    if pity_4 >= 9:
        return "4_star"
    if pity_5 > soft_pity:
        weight_5_star += (pity_5 - soft_pity) * ((1 - proba_5) / (hard_pity - soft_pity))

    weight_5_star = min(weight_5_star, 1 - weight_4_star)
    weight_3_star = 1 - weight_4_star - weight_5_star
    tirage = random.choices(
        ["5_star", "4_star", "3_star"],
        [weight_5_star, weight_4_star, weight_3_star]
        )[0]
    return tirage

def wish(pity_5_star, pity_4_star, garanti,current_banner_index, soft_pity=73, hard_pity=90, ):
    """
    Effectue 1 voeu et retourne tous les résultats.
    
    Args:
        pity_5_star,pity_4_star (int): compteur actuel pity 5★ et 4★
        garanti (bool): True si le prochain 5★ est garanti 
        soft_pity (int, optional): soft pity 5★
        hard_pity (int, optional): hard pity 5★ 
        current_banner_index (int): index de la bannière actuelle
    
    Returns:
        dict: {
            "rarete": str,  # "5_star", "5_star_perma", "4_star" ou "3_star"
            "character": dict,  # le personnage obtenu
            "animation": str,  # chemin d'animaton de voeu
            "splash_art": pygame.Surface,  #image du personnage
            "new_pity_5_star": int,  # nouvelle pity 5★
            "new_pity_4_star": int,  # nouvelle pity 4★
            "new_garanti": bool  # nouveau statut guaranteed
        }
    """
    wish_rarete = rarete(pity_5_star, pity_4_star,proba_init_5_star,proba_init_4_star,chance_globale ,soft_pity, hard_pity)
    new_pity_5_star = pity_5_star
    new_pity_4_star = pity_4_star
    new_garanti = garanti
    
    if wish_rarete == "5_star":
        new_pity_5_star = 0
        new_pity_4_star += 1
        wish_animation = "videos/pull_5_star.mp4"
    elif wish_rarete == "4_star":
        wish_animation = "videos/pull_4_star.mp4"
        new_pity_4_star = 0
        new_pity_5_star += 1
    else:
        wish_animation = "videos/pull_3_star.mp4"
        new_pity_5_star += 1
        new_pity_4_star += 1

    if wish_rarete == "5_star":
        if not garanti and random.random() < 0.5:
            new_garanti = True
            wish_rarete = "5_star_perma"
        else:
            new_garanti = False
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
    
    wish_splash_art = scale_to_height(pygame.image.load(wish_result_character["image"]).convert_alpha(), HEIGHT)
    return {
        "rarete": wish_rarete,
        "character": wish_result_character,
        "animation": wish_animation,
        "splash_art": wish_splash_art,
        "new_pity_5_star": new_pity_5_star,
        "new_pity_4_star": new_pity_4_star,
        "new_garanti": new_garanti
    }

################
# --- Save --- #
################

def sauvegarder_pity(pity_5, pity_4, garanti,banner_index, nom_fichier="save/save.json"):
    """
    Sauvegarde les données de pity dans un fichier JSON.
    """
    donnees = {
        "data": [
            {"pity_5_star": pity_5},
            {"pity_4_star": pity_4},
            {"garanti": str(garanti)},
            {"current_banner_index": banner_index}
        ]
    }
    
    with open(nom_fichier, 'w', encoding='utf-8') as f:
        json.dump(donnees, f, indent=4, ensure_ascii=False)
    
    print(f"Données sauvegardées dans {nom_fichier}")