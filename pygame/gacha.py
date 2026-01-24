import pygame
import sys
import random
import cv2

pygame.init()
HEIGHT = 900 
WIDTH = int(HEIGHT*16/9)
screen = pygame.display.set_mode((WIDTH, HEIGHT))
font = pygame.font.Font("pygame/font/genshin.ttf", 40)
button_font = pygame.font.Font("pygame/font/genshin.ttf", 30)

def scale_to_height(image, target_height):
    """
    Redimensionne une image pour que sa hauteur = target_height en gardant le ratio.
    """
    w, h = image.get_size()
    scale_factor = target_height / h
    new_w = int(w * scale_factor)
    new_h = target_height
    return pygame.transform.scale(image, (new_w, new_h))

def scale_with_borders(image, target_width, target_height, border_percent=15):
    """
    Redimensionne une image avec des bordures en pourcentage (plus petites = image plus grande)
    """
    border_w = int(target_width * border_percent / 100)
    border_h = int(target_height * border_percent / 100)
    
    new_width = target_width - (2 * border_w)
    new_height = target_height - (2 * border_h)
    
    return pygame.transform.scale(image, (new_width, new_height)), border_w, border_h

# --- Charger images ---
background = scale_to_height(pygame.image.load("pygame/img/background.png").convert_alpha(), HEIGHT)

banniere, banner_border_w, banner_border_h = scale_with_borders(pygame.image.load("pygame/img/banniere/skirk.jpg").convert_alpha(), WIDTH, HEIGHT, border_percent=15)

# --- Définir boutons ---
button_x1_rect = pygame.Rect(WIDTH//2 - 220, HEIGHT - 80, 200, 60)
button_x10_rect = pygame.Rect(WIDTH//2 + 20, HEIGHT - 80, 200, 60)
button_color = (255, 255, 230)
button_hover_color = (240, 240, 230)

# -------- Paramètres Gacha ---------  <--- ICI
pity_5_star = 60
pity_4_star = 1
soft_pity = 73
hard_pity = 90
guaranteed_5_star = False
wish_rarete = None
wish_splash_art = None

characters = {
    "5_star": [
        {"name": "Columbina", "image": "pygame/img/5_star/Columbina.png"},
        {"name": "Zhongli", "image": "pygame/img/5_star/Zhongli.png"},
    ],
    "5_star_perma": [
        {"name": "Qiqi", "image": "pygame/img/5_star/Qiqi.png"},
    ],

    "4_star": [
        {"name": "Bennett", "image": "pygame/img/4_star/Bennett.png"},
    ],

    "3_star": [
        {"name": "Thrilling Tale of Dragon Slayer", "image": "pygame/img/3_star/TTDS.png"},
        {"name": "Ferrous Shadow", "image": "pygame/img/3_star/Ferrous_Shadow.png"},
    ]
}

def rarete(pity_5_star, pity_4_star, soft_pity=70, hard_pity=90):
    """
    Calcule la rareté d'un tirage sans modifier les compteurs de pity.
    
    Args:
        pity_5_star (int): compteur actuel de 5★
        pity_4_star (int): compteur actuel de 4★
        soft_pity (int, optional): début de la soft pity pour 5★. Défaut 70
        hard_pity (int, optional): hard pity pour 5★. Défaut 90

    Returns:
        str: "5_star", "4_star" ou "3_star" selon le tirage
    """

    w5 = 0.006
    w4 = 0.051

    # Hard pity
    if pity_5_star >= hard_pity:
        return "5_star"

    # Pity 4*
    if pity_4_star >= 9:
        return "4_star"

    # Soft pity
    if pity_5_star > soft_pity:
        w5 += (pity_5_star - soft_pity) * ((1 - 0.006) / (hard_pity - soft_pity))

    w5 = min(w5, 1 - w4)
    w3 = 1 - w4 - w5

    tirage = random.choices(
        ["5_star", "4_star", "3_star"],
        [w5, w4, w3]
    )[0]

    return tirage

def faire_un_voeu(pity_5_star, pity_4_star, guaranteed_5_star, soft_pity=70, hard_pity=90):
    """
    Effectue un vœu et retourne tous les résultats.
    
    Args:
        pity_5_star (int): compteur actuel de 5★
        pity_4_star (int): compteur actuel de 4★
        guaranteed_5_star (bool): si le prochain 5★ est garanti featured
        soft_pity (int, optional): début de la soft pity pour 5★. Défaut 70
        hard_pity (int, optional): hard pity pour 5★. Défaut 90
    
    Returns:
        dict: {
            "rarete": str,  # "5_star", "5_star_perma", "4_star" ou "3_star"
            "character": dict,  # le personnage obtenu
            "animation": str,  # chemin de la vidéo
            "splash_art": pygame.Surface,  # l'image du personnage
            "new_pity_5_star": int,  # nouveau compteur 5★
            "new_pity_4_star": int,  # nouveau compteur 4★
            "new_guaranteed_5_star": bool  # nouveau statut guaranteed
        }
    """
    wish_rarete = rarete(pity_5_star, pity_4_star, soft_pity, hard_pity)
    
    new_pity_5_star = pity_5_star
    new_pity_4_star = pity_4_star
    new_guaranteed_5_star = guaranteed_5_star
    
    if wish_rarete == "5_star":
        new_pity_5_star = 0
        new_pity_4_star += 1
        wish_animation = "pygame/videos/pull_5_star.mp4"
        
        if not guaranteed_5_star and random.random() < 0.5:
            new_guaranteed_5_star = True
            wish_rarete = "5_star_perma"
        else:
            new_guaranteed_5_star = False
            
    elif wish_rarete == "4_star":
        wish_animation = "pygame/videos/pull_4_star.mp4"
        new_pity_4_star = 0
        new_pity_5_star += 1
    else:
        wish_animation = "pygame/videos/pull_3_star.mp4"
        new_pity_5_star += 1
        new_pity_4_star += 1
    
    wish_result_character = random.choice(characters[wish_rarete])
    wish_splash_art = scale_to_height(
        pygame.image.load(wish_result_character["image"]).convert_alpha(), 
        HEIGHT
    )
    
    return {
        "rarete": wish_rarete,
        "character": wish_result_character,
        "animation": wish_animation,
        "splash_art": wish_splash_art,
        "new_pity_5_star": new_pity_5_star,
        "new_pity_4_star": new_pity_4_star,
        "new_guaranteed_5_star": new_guaranteed_5_star
    }

def play_video(video_path, screen, loop=False):
    """
    Lit et affiche une vidéo sur l'écran pygame
    """
    cap = cv2.VideoCapture(video_path)
    
    if not cap.isOpened():
        print(f"Erreur: Impossible d'ouvrir la vidéo {video_path}")
        return True
    
    fps = cap.get(cv2.CAP_PROP_FPS)
    if fps == 0 or fps > 120: 
        fps = 30
    
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    print(f"Lecture de {video_path}")
    print(f"FPS: {fps}, Frames totales: {total_frames}")
    
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
    print("Vidéo terminée")
    return True

def draw_button(screen, rect, text, mouse_pos):

    """Dessine un bouton avec effet de survol"""
    if rect.collidepoint(mouse_pos):
        color = button_hover_color
    else:
        color = button_color
    
    pygame.draw.rect(screen, color, rect, border_radius=30)
    pygame.draw.rect(screen, (180, 178, 178), rect, 3, border_radius=30) 
    
    button_text = button_font.render(text, True, (183, 167, 155))
    text_rect = button_text.get_rect(center=rect.center)
    screen.blit(button_text, text_rect)

def afficher_resultats(results, screen): 
    """
    Affiche les résultats un par un avec navigation
    
    Args:
        results (list): liste des résultats des vœux
        screen: surface pygame
    
    Returns:
        tuple: (bool, bool) - (continue_running, reset_to_banniere)
    """
    current_index = 0
    showing_results = True
    clock = pygame.time.Clock()
    
    while showing_results:
        mouse_pos = pygame.mouse.get_pos()
        
        # Afficher le fond
        screen.fill((255, 255, 255))
        screen.blit(background, (WIDTH//2 - background.get_width()//2, HEIGHT//2 - background.get_height()//2))
        
        # Afficher le splash art actuel
        current_result = results[current_index]
        screen.blit(current_result["splash_art"], 
                    (WIDTH//2 - current_result["splash_art"].get_width()//2, 
                    HEIGHT//2 - current_result["splash_art"].get_height()//2))
        
        # Afficher le compteur (ex: 1/10)
        counter_text = font.render(f"{current_index + 1}/{len(results)}", True, (255, 255, 255))
        screen.blit(counter_text, (WIDTH//2 - counter_text.get_width()//2, 50))
        
        # Afficher le nom du personnage
        char_name = button_font.render(current_result["character"]["name"], True, (255, 255, 255))
        screen.blit(char_name, (WIDTH//2 - char_name.get_width()//2, HEIGHT - 100))
        
        # Instructions
        instruction = button_font.render("Clic ou Espace pour continuer - Echap pour quitter", True, (255, 255, 255))
        screen.blit(instruction, (WIDTH//2 - instruction.get_width()//2, HEIGHT - 50))
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False, False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE or event.key == pygame.K_RIGHT:
                    current_index += 1
                    if current_index >= len(results):
                        return True, True  # Retour à la bannière
                elif event.key == pygame.K_LEFT and current_index > 0:
                    current_index -= 1
                elif event.key == pygame.K_ESCAPE:
                    return True, True  # Retour à la bannière
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:  # Clic gauche
                    current_index += 1
                    if current_index >= len(results):
                        return True, True  # Retour à la bannière
        
        pygame.display.flip()
        clock.tick(60)
    
    return True, True

# --- Boucle principale ---
running = True
clock = pygame.time.Clock()
delta_time = 0.1

while running:
    mouse_pos = pygame.mouse.get_pos()
    
    screen.fill((0, 0, 0))
    text = font.render("Not Genshin Impact", True, (255, 255, 254))
    screen.blit(background, (WIDTH//2 - background.get_width()//2, HEIGHT//2 - background.get_height()//2))
    
    if wish_splash_art is None:
        border_thickness = 5
        border_rect = pygame.Rect(
            banner_border_w - border_thickness,
            banner_border_h - border_thickness,
            banniere.get_width() + (border_thickness * 2),
            banniere.get_height() + (border_thickness * 2)
        )
        pygame.draw.rect(screen, (178, 180, 166), border_rect, border_thickness, border_radius=10)  # Bordure dorée
        
        screen.blit(banniere, (banner_border_w, banner_border_h))
    else:
        screen.blit(wish_splash_art, (WIDTH//2 - wish_splash_art.get_width()//2, HEIGHT//2 - wish_splash_art.get_height()//2))
        
    screen.blit(text, (WIDTH//2 - text.get_width()//2, 20))
    
    draw_button(screen, button_x1_rect, "Voeu x1", mouse_pos)
    draw_button(screen, button_x10_rect, "Voeu x10", mouse_pos)
    pity_text = button_font.render(f"Pity 5★: {pity_5_star}/{hard_pity}", True, (255, 215, 0))
    odd_5_star =(pity_5_star - soft_pity) * ((1 - 0.006) / (hard_pity - soft_pity)) + 0.006 if pity_5_star > soft_pity else 0.006
    pity_text_2 = button_font.render(f"Chance 5★: {min(odd_5_star*100, 100):.2f}%", True, (255, 215, 0))
    screen.blit(pity_text_2, (20, 60))
    screen.blit(pity_text, (20, 20))
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1: 
                if button_x1_rect.collidepoint(event.pos):
                    result = faire_un_voeu(pity_5_star, pity_4_star, guaranteed_5_star, soft_pity, hard_pity)
                    
                    wish_rarete = result["rarete"]
                    wish_splash_art = result["splash_art"]
                    pity_5_star = result["new_pity_5_star"]
                    pity_4_star = result["new_pity_4_star"]
                    guaranteed_5_star = result["new_guaranteed_5_star"]
                    
                    if not play_video(result["animation"], screen, loop=False):
                        running = False

                elif button_x10_rect.collidepoint(event.pos):
                    results = []
                    for _ in range(10):
                        result = faire_un_voeu(pity_5_star, pity_4_star, guaranteed_5_star, soft_pity, hard_pity)
                        results.append(result)
                        
                        pity_5_star = result["new_pity_5_star"]
                        pity_4_star = result["new_pity_4_star"]
                        guaranteed_5_star = result["new_guaranteed_5_star"]
                    
                    rarete_priority = {
                        "5_star": 1,
                        "5_star_perma": 2,
                        "4_star": 3,
                        "3_star": 4
                    }   
                    best_result = min(results, key=lambda x: rarete_priority[x["rarete"]])
                    
                    if not play_video(best_result["animation"], screen, loop=False):
                        running = False
                    
                    continue_running, reset_to_banniere = afficher_resultats(results, screen)
                    if not continue_running:
                        running = False
                    
                    if reset_to_banniere:
                        wish_rarete = None
                        wish_splash_art = None
                
                elif wish_splash_art is not None:
                    wish_rarete = None
                    wish_splash_art = None
                    
    pygame.display.flip()
    delta_time = clock.tick(60)/1000
    delta_time = min(delta_time, 0.05)

pygame.quit()
sys.exit()