import pygame
import sys
import random
import cv2

pygame.init()
HEIGHT = 500
WIDTH = int(HEIGHT*16/9)
screen = pygame.display.set_mode((WIDTH, HEIGHT))

font_size = int(HEIGHT * 40 / 900)  
button_font_size = int(HEIGHT * 30 / 900)

font = pygame.font.Font("pygame/font/genshin.ttf", font_size)
button_font = pygame.font.Font("pygame/font/genshin.ttf", button_font_size)

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

# --- Charger background ---
background = scale_to_height(pygame.image.load("pygame/img/background.png").convert_alpha(), HEIGHT)

# --- Paramètres Gacha ---
pity_5_star = 80
pity_4_star = 1
soft_pity = 73
hard_pity = 90
guaranteed_5_star = False
wish_rarete = None
wish_splash_art = None

characters = {
    "5_star": [
        {
            "name": "Columbina", 
            "image": "pygame/img/5_star/Columbina.png", 
            "banniere": "pygame/img/banniere/Columbina.jpg",
            "featured_4_star": ["Ifa", "Sethos", "Fischl"]
        },
        {
            "name": "Zhongli", 
            "image": "pygame/img/5_star/Zhongli.png", 
            "banniere": "pygame/img/banniere/Zhongli.jpg",
            "featured_4_star": ["Rosaria", "Lan Yan", "Yun Jin"]
        },
        {
            "name": "Skirk", 
            "image": "pygame/img/5_star/Skirk.png", 
            "banniere": "pygame/img/banniere/Skirk.jpg",
            "featured_4_star": ["Diona", "Candace", "Dahlia"]
        },
    ],
    "5_star_perma": [
        {"name": "Qiqi", "image": "pygame/img/5_star/Qiqi.png"},
        {"name": "Dehya", "image": "pygame/img/5_star/Dehya.png"},
        {"name": "Diluc", "image": "pygame/img/5_star/Diluc.png"},
        {"name": "Jean", "image": "pygame/img/5_star/Jean.png"},
        {"name": "Keqing", "image": "pygame/img/5_star/Keqing.png"},
        {"name": "Mona", "image": "pygame/img/5_star/Mona.png"},
        {"name": "Tighnari", "image": "pygame/img/5_star/Tighnari.png"},
        {"name": "Yumemizuki Mizuki", "image": "pygame/img/5_star/Yumemizuki_Mizuki.png"},
    ],
    "4_star": [
        {"name": "Bennett", "image": "pygame/img/4_star/Bennett.png"},
        {"name": "Sethos", "image": "pygame/img/4_star/Sethos.png"},
        {"name": "Candace", "image": "pygame/img/4_star/Candace.png"},
        {"name": "Dahlia", "image": "pygame/img/4_star/Dahlia.png"},
        {"name": "Diona", "image": "pygame/img/4_star/Diona.png"},
        {"name": "Fischl", "image": "pygame/img/4_star/Fischl.png"},
        {"name": "Ifa", "image": "pygame/img/4_star/Ifa.png"},
        {"name": "Lan Yan", "image": "pygame/img/4_star/Lan_Yan.png"},
        {"name": "Rosaria", "image": "pygame/img/4_star/Rosaria.png"},
        {"name": "Yun Jin", "image": "pygame/img/4_star/Yun_Jin.png"},
    ],
    "3_star": [
        {"name": "Thrilling Tale of Dragon Slayer", "image": "pygame/img/3_star/TTDS.png", "type": "catalyst"},
        {"name": "Ferrous Shadow", "image": "pygame/img/3_star/Ferrous_Shadow.png","type": "claymore"},
        {"name": "Slingshot", "image": "pygame/img/3_star/Slingshot.png", "type": "bow"},
        {"name": "Black Tassel", "image": "pygame/img/3_star/Black_tassel.png", "type": "polearm"},
        {"name": "Cool Steel", "image": "pygame/img/3_star/Cool_Steel.png", "type": "sword"},  
    ]
}

# --- Initialisation bannière ---
current_banner_index = 0  
banniere_path = characters["5_star"][current_banner_index]["banniere"]
banniere, banner_border_w, banner_border_h = scale_with_borders(pygame.image.load(banniere_path).convert_alpha(), WIDTH, HEIGHT, border_percent=15)

# --- Boutons Voeu ---
button_height = int(HEIGHT * 60 / 900)
button_width = int(HEIGHT * 200 / 900)
button_spacing = int(HEIGHT * 20 / 900)
button_bottom_margin = int(HEIGHT * 80 / 900)

button_x1_rect = pygame.Rect(WIDTH//2 - button_width - button_spacing//2, HEIGHT - button_bottom_margin, button_width, button_height)
button_x10_rect = pygame.Rect(WIDTH//2 + button_spacing//2, HEIGHT - button_bottom_margin, button_width, button_height)
button_color = (255, 255, 230)
button_hover_color = (240, 240, 230)

# --- Boutons gauche pour choix bannière ---
left_button_width = int(HEIGHT * 200 / 900)
left_button_height = int(HEIGHT * 50 / 900)
left_button_spacing = int(HEIGHT * 20 / 900)
left_buttons = []
for i, char in enumerate(characters["5_star"]):
    rect = pygame.Rect(
        left_button_spacing,
        left_button_spacing + HEIGHT*65/500 + i * (left_button_height + left_button_spacing),
        left_button_width,
        left_button_height
    )
    left_buttons.append((rect, char["name"]))

# --- Fonctions ---
def draw_left_buttons(screen, mouse_pos):
    for rect, name in left_buttons:
        color = (140, 140, 110) if rect.collidepoint(mouse_pos) else (178, 180, 140)
        pygame.draw.rect(screen, color, rect, border_radius=5)
        text_surf = button_font.render(name, True, (78, 80, 40))
        text_rect = text_surf.get_rect(center=rect.center)
        screen.blit(text_surf, text_rect)

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

def faire_un_voeu(pity_5_star, pity_4_star, guaranteed_5_star, soft_pity=70, hard_pity=90, current_banner_index=0):
    """
    Effectue un vœu et retourne tous les résultats.
    
    Args:
        pity_5_star (int): compteur actuel de 5★
        pity_4_star (int): compteur actuel de 4★
        guaranteed_5_star (bool): si le prochain 5★ est garanti featured
        soft_pity (int, optional): début de la soft pity pour 5★. Défaut 70
        hard_pity (int, optional): hard pity pour 5★. Défaut 90
        current_banner_index (int): index de la bannière actuelle
    
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
    
    elif wish_rarete == "4_star":
        wish_animation = "pygame/videos/pull_4_star.mp4"
        new_pity_4_star = 0
        new_pity_5_star += 1
    else:
        wish_animation = "pygame/videos/pull_3_star.mp4"
        new_pity_5_star += 1
        new_pity_4_star += 1
        
    if wish_rarete == "5_star":
        if not guaranteed_5_star and random.random() < 0.5:
            new_guaranteed_5_star = True
            wish_rarete = "5_star_perma"
        else:
            new_guaranteed_5_star = False
    
    if wish_rarete == "4_star":
        featured_4_stars = characters["5_star"][current_banner_index].get("featured_4_star", [])
        if featured_4_stars and random.random() < 0.5:  
            # Featured 4★
            featured_chars = [c for c in characters["4_star"] if c["name"] in featured_4_stars]
            wish_result_character = random.choice(featured_chars)
        else:
            # Non-featured 4★
            non_featured_chars = [c for c in characters["4_star"] if c["name"] not in featured_4_stars]
            wish_result_character = random.choice(non_featured_chars) if non_featured_chars else random.choice(characters["4_star"])
    elif wish_rarete == "5_star":
        wish_result_character = characters["5_star"][current_banner_index]
    else:
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
    
    border_radius = int(HEIGHT * 30 / 900)
    border_width = int(HEIGHT * 3 / 900)
    
    pygame.draw.rect(screen, color, rect, border_radius=border_radius)
    pygame.draw.rect(screen, (180, 178, 178), rect, border_width, border_radius=border_radius) 
    
    button_text = button_font.render(text, True, (183, 167, 155))
    text_rect = button_text.get_rect(center=rect.center)
    screen.blit(button_text, text_rect)

def afficher_resultats(results, screen): 
    """
    Affiche les résultats des voeux un par un 
    
    Args:
        results (list): liste des résultats des vœux
        screen: surface pygame
    
    Returns:
        tuple: (bool, bool) - (continue_running, reset_to_banniere)
    """
    current_index = 0
    showing_results = True
    clock = pygame.time.Clock()
    
    counter_y = int(HEIGHT * 50 / 900)
    name_y = int(HEIGHT * 100 / 900)
    instruction_y = int(HEIGHT * 50 / 900)
    
    while showing_results:
        mouse_pos = pygame.mouse.get_pos()
        
        screen.fill((255, 255, 255))
        screen.blit(background, (WIDTH//2 - background.get_width()//2, HEIGHT//2 - background.get_height()//2))
        
        current_result = results[current_index]
        screen.blit(current_result["splash_art"], 
                    (WIDTH//2 - current_result["splash_art"].get_width()//2, 
                    HEIGHT//2 - current_result["splash_art"].get_height()//2))
        
        counter_text = font.render(f"{current_index + 1}/{len(results)}", True, (255, 255, 255))
        screen.blit(counter_text, (WIDTH//2 - counter_text.get_width()//2, counter_y))
        
        # Afficher le nom du personnage
        char_name = button_font.render(current_result["character"]["name"], True, (255, 255, 255))
        screen.blit(char_name, (WIDTH//2 - char_name.get_width()//2, HEIGHT - name_y))
        
        # Instructions
        instruction = button_font.render("Clic ou Espace pour continuer - Echap pour quitter", True, (255, 255, 255))
        screen.blit(instruction, (WIDTH//2 - instruction.get_width()//2, HEIGHT - instruction_y))
        
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
title_y = int(HEIGHT * 20 / 900)
pity_y = int(HEIGHT * 20 / 900)
pity_y2 = int(HEIGHT * 60 / 900)
pity_x = int(HEIGHT * 20 / 900)
border_thickness = int(HEIGHT * 5 / 900)
border_radius = int(HEIGHT * 10 / 900)

while running:
    mouse_pos = pygame.mouse.get_pos()
    
    screen.fill((0, 0, 0))
    screen.blit(background, (WIDTH//2 - background.get_width()//2, HEIGHT//2 - background.get_height()//2))
    
    if wish_splash_art is None:
        border_rect = pygame.Rect(
            banner_border_w - border_thickness,
            banner_border_h - border_thickness,
            banniere.get_width() + (border_thickness * 2),
            banniere.get_height() + (border_thickness * 2)
        )
        pygame.draw.rect(screen, (178, 180, 166), border_rect, border_thickness, border_radius=border_radius)
        screen.blit(banniere, (banner_border_w, banner_border_h))
    else:
        screen.blit(wish_splash_art, (WIDTH//2 - wish_splash_art.get_width()//2, HEIGHT//2 - wish_splash_art.get_height()//2))
    
    # --- Boutons ---
    draw_button(screen, button_x1_rect, "Voeu x1", mouse_pos)
    draw_button(screen, button_x10_rect, "Voeu x10", mouse_pos)
    draw_left_buttons(screen, mouse_pos)
    
    # --- Texte Pity ---
    pity_text = button_font.render(f"Pity 5★: {pity_5_star}/{hard_pity}", True, (255, 215, 0))
    odd_5_star =(pity_5_star - soft_pity) * ((1 - 0.006) / (hard_pity - soft_pity)) + 0.006 if pity_5_star > soft_pity else 0.006
    pity_text_2 = button_font.render(f"Chance 5★: {min(odd_5_star*100, 100):.2f}%", True, (255, 215, 0))
    screen.blit(pity_text_2, (pity_x, pity_y2))
    screen.blit(pity_text, (pity_x, pity_y))
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            # --- Voeux ---
            if button_x1_rect.collidepoint(event.pos):
                result = faire_un_voeu(pity_5_star, pity_4_star, guaranteed_5_star, soft_pity, hard_pity, current_banner_index)
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
                    result = faire_un_voeu(pity_5_star, pity_4_star, guaranteed_5_star, soft_pity, hard_pity, current_banner_index)
                    results.append(result)
                    pity_5_star = result["new_pity_5_star"]
                    pity_4_star = result["new_pity_4_star"]
                    guaranteed_5_star = result["new_guaranteed_5_star"]

                rarete_priority = {"5_star":1,"5_star_perma":2,"4_star":3,"3_star":4}   
                best_result = min(results, key=lambda x: rarete_priority[x["rarete"]])
                if not play_video(best_result["animation"], screen, loop=False):
                    running = False
                continue_running, reset_to_banniere = afficher_resultats(results, screen)
                if not continue_running:
                    running = False
                if reset_to_banniere:
                    wish_rarete = None
                    wish_splash_art = None

            # --- Clic sur boutons bannière ---
            for i, (rect, name) in enumerate(left_buttons):
                if rect.collidepoint(event.pos):
                    current_banner_index = i
                    banniere_path = characters["5_star"][current_banner_index]["banniere"]
                    banniere = scale_with_borders(pygame.image.load(banniere_path).convert_alpha(), WIDTH, HEIGHT, border_percent=15)[0]
                    wish_splash_art = None  
                    
            if wish_splash_art is not None:
                wish_rarete = None
                wish_splash_art = None
    
    pygame.display.flip()
    delta_time = clock.tick(60)/1000
    delta_time = min(delta_time, 0.05)

pygame.quit()
sys.exit()