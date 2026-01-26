import pygame
import sys
import random
import cv2

# --- Paramètres Voeu ---
pity_5_star = 80
pity_4_star = 0
soft_pity = 73
hard_pity = 90
guaranteed_5_star = False
wish_rarete = None
wish_splash_art = None
animation_progress = 0.0 
characters = {
    "5_star": [
        {#Columbina
            "name": "Columbina", 
            "image": "pygame/img/5_star/Columbina.png", 
            "banniere": "pygame/img/banniere/Columbina.jpg",
            "featured_4_star": ["Ifa", "Sethos", "Fischl"],
            "type": None
        },
        {#Zhongli
            "name": "Zhongli", 
            "image": "pygame/img/5_star/Zhongli.png", 
            "banniere": "pygame/img/banniere/Zhongli.jpg",
            "featured_4_star": ["Rosaria", "Lan Yan", "Yun Jin"],
            "type": None
        },
        {#Skirk
            "name": "Skirk", 
            "image": "pygame/img/5_star/Skirk.png", 
            "banniere": "pygame/img/banniere/Skirk.jpg",
            "featured_4_star": ["Diona", "Candace", "Dahlia"],
            "type": None
        },
        {#Mavuika
            "name": "Mavuika", 
            "image": "pygame/img/5_star/Mavuika.png", 
            "banniere": "pygame/img/banniere/Mavuika.jpg",
            "featured_4_star": ["Xiangling", "Yaoyao", "Iansan"],
            "type": None
        },
        {#Citlali
            "name": "Citlali", 
            "image": "pygame/img/5_star/Citlali.png", 
            "banniere": "pygame/img/banniere/Citlali.jpg",
            "featured_4_star": ["Diona", "Kachina", "Bennett"],
            "type": None
        },
    ],
    "5_star_perma": [
        {"name": "Qiqi", "image": "pygame/img/5_star/Qiqi.png","type": None},
        {"name": "Dehya", "image": "pygame/img/5_star/Dehya.png","type": None},
        {"name": "Diluc", "image": "pygame/img/5_star/Diluc.png", "type": None},
        {"name": "Jean", "image": "pygame/img/5_star/Jean.png", "type": None},
        {"name": "Keqing", "image": "pygame/img/5_star/Keqing.png", "type": None},
        {"name": "Mona", "image": "pygame/img/5_star/Mona.png", "type": None},
        {"name": "Tighnari", "image": "pygame/img/5_star/Tighnari.png", "type": None},
        {"name": "Yumemizuki Mizuki", "image": "pygame/img/5_star/Yumemizuki_Mizuki.png", "type": None},
    ],
    "4_star": [
        {"name": "Bennett", "image": "pygame/img/4_star/Bennett.png", "type": None},
        {"name": "Sethos", "image": "pygame/img/4_star/Sethos.png", "type": None},
        {"name": "Candace", "image": "pygame/img/4_star/Candace.png", "type": None},
        {"name": "Dahlia", "image": "pygame/img/4_star/Dahlia.png", "type": None},
        {"name": "Diona", "image": "pygame/img/4_star/Diona.png", "type": None},
        {"name": "Fischl", "image": "pygame/img/4_star/Fischl.png", "type": None},
        {"name": "Ifa", "image": "pygame/img/4_star/Ifa.png", "type": None},
        {"name": "Iansan", "image": "pygame/img/4_star/Iansan.png", "type": None},
        {"name": "Kachina", "image": "pygame/img/4_star/Kachina.png", "type": None},
        {"name": "Lan Yan", "image": "pygame/img/4_star/Lan_Yan.png", "type": None},
        {"name": "Rosaria", "image": "pygame/img/4_star/Rosaria.png", "type": None},
        {"name": "Yun Jin", "image": "pygame/img/4_star/Yun_Jin.png", "type": None},
        {"name": "Yaoyao", "image": "pygame/img/4_star/Yaoyao.png", "type": None},
        {"name": "Xiangling", "image": "pygame/img/4_star/Xiangling.png", "type": None},
    ],
    "3_star": [
        {"name": "Thrilling Tale of Dragon Slayer", "image": "pygame/img/3_star/Thrilling_Tale_of_Dragon_Slayer.png", "type": "catalyst"},
        {"name": "Ferrous Shadow", "image": "pygame/img/3_star/Ferrous_Shadow.png","type": "claymore"},
        {"name": "Slingshot", "image": "pygame/img/3_star/Slingshot.png", "type": "bow"},
        {"name": "Black Tassel", "image": "pygame/img/3_star/Black_tassel.png", "type": "polearm"},
        {"name": "Cool Steel", "image": "pygame/img/3_star/Cool_Steel.png", "type": "sword"},  
    ]
}
# --- Initalisation ---
pygame.init()
HEIGHT = 660
WIDTH = int(HEIGHT*16/9)
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Totally not a Genshin Impact wishing replica")
pygame.display.set_icon(pygame.image.load("pygame/img/icon.png").convert_alpha())
font_size = int(HEIGHT * 40 / 900)  
font = pygame.font.Font("pygame/font/genshin.ttf", font_size)
button_font_size = int(HEIGHT * 30 / 900)
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

background = scale_to_height(pygame.image.load("pygame/img/background.png").convert_alpha(), HEIGHT)
background_wishing = scale_to_height(pygame.image.load("pygame/img/background_wishing.png").convert_alpha(), HEIGHT)
# --- Initialisation bannière ---
current_banner_index = 0  
banniere_path = characters["5_star"][current_banner_index]["banniere"]
banniere, banner_border_w, banner_border_h = scale_with_borders(pygame.image.load(banniere_path).convert_alpha(), WIDTH, HEIGHT, border_percent=15)
# --- Boutons Voeux ---
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

def afficher_splash_art(screen, splash_art, progress=1.0):
    """
    'anime' le splash art
    
    Args:
        screen: surface pygame
        splash_art: image du personnage
        progress (float): progression de l'animation de 0 à 1
    """
    scale_factor = 1.8 - (0.5 * min(progress, 1))
    
    new_width = int(splash_art.get_width() * scale_factor)
    new_height = int(splash_art.get_height() * scale_factor)
    scaled_splash = pygame.transform.scale(splash_art, (new_width, new_height))
    
    x = WIDTH // 2 - scaled_splash.get_width() // 2
    y = HEIGHT // 2 - scaled_splash.get_height() // 2
    
    alpha = int(255 * min(progress, 1))
    scaled_splash.set_alpha(alpha)
    screen.blit(scaled_splash, (x, y))

def rarete(pity_5_star, pity_4_star, soft_pity=70, hard_pity=90,w5=0.006,w4=0.08):
    """
    Calcule la rareté d'un tirage sans modifier les compteurs de pity.
    
    Args:
        pity_5_star (int): compteur actuel pity 5★
        pity_4_star (int): compteur actuel pity 4★
        soft_pity (int, optional): début de la soft pity pour 5★. Défaut 70
        hard_pity (int, optional): hard pity pour 5★. Défaut 90

    Returns:
        str: "5_star", "4_star" ou "3_star" selon le tirage aléatoire pondéré.
    """

    if pity_5_star >= hard_pity:
        return "5_star"
    if pity_4_star >= 9:
        return "4_star"
    if pity_5_star > soft_pity:
        w5 += (pity_5_star - soft_pity) * ((1 - 0.006) / (hard_pity - soft_pity))

    w5 = min(w5, 1 - w4)
    w3 = 1 - w4 - w5
    tirage = random.choices(
        ["5_star", "4_star", "3_star"],
        [w5, w4, w3]
        )[0]
    return tirage

def wish(pity_5_star, pity_4_star, guaranteed_5_star, soft_pity=70, hard_pity=90, current_banner_index=0):
    """
    Effectue 1 voeuu et retourne tous les résultats.
    
    Args:
        pity_5_star,pity_4_star (int): compteur actuel pity 5★ et 4★
        guaranteed_5_star (bool): True si le prochain 5★ est garanti 
        soft_pity (int, optional): soft pity 5★. Défaut 70
        hard_pity (int, optional): hard pity 5★. Défaut 90
        current_banner_index (int): index de la bannière actuelle
    
    Returns:
        dict: {
            "rarete": str,  # "5_star", "5_star_perma", "4_star" ou "3_star"
            "character": dict,  # le personnage obtenu
            "animation": str,  # chemin d'animaton de voeu
            "splash_art": pygame.Surface,  #image du personnage
            "new_pity_5_star": int,  # nouvelle pity 5★
            "new_pity_4_star": int,  # nouvelle pity 4★
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
        "new_guaranteed_5_star": new_guaranteed_5_star
    }

def play_video(video_path, screen, loop=False):
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
    """Dessine bouton"""
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

def weapon_background_path(weapon):
    """
    Donne le chemin de l'image de fond selon le type d'arme.
    Args:
        weapon (str): type d'arme ("sword", "claymore", "polearm", "bow", "catalyst")
    """
    return pygame.image.load(f"pygame/img/Weapon_Background/{weapon}.png").convert_alpha()

def darken(rgb, coefficient=0.5):
        """
        Assombrit une couleur

        Args:
            rgb (tuple): couleur à assombrir
        """
        return tuple(int(i * coefficient) for i in rgb)

def get_color(rare:str):

        if rare in ["5_star", "5_star_perma"]:
            return (220, 190, 20)

        if rare == "4_star":
            return (120, 60, 185)

        return (80, 140, 225)

def ecran_multi(results, screen, radius=60,border=5,ecart=5):
    """
    Écran résumé de la multi
    """

    clock = pygame.time.Clock()
    running = True
    rarete_priority = {"5_star": 1, "5_star_perma": 2, "4_star": 3, "3_star": 4}
    results = sorted(results, key=lambda x: rarete_priority[x["rarete"]])
    images = []
    raretes = []
    for res in results:
        name = res["character"]["name"].replace(" ", "_")
        rarete = res["rarete"]
        if rarete in ["5_star", "5_star_perma"]:
            path = f"pygame/img/5_star/multi/{name}.png"
        elif rarete == "4_star":
            path = f"pygame/img/4_star/multi/{name}.png"
        else:
            path = f"pygame/img/3_star/{name}.png"
        try:
            img = pygame.image.load(path).convert_alpha()
            images.append(img)
        except:
            images.append(None)
        raretes.append(rarete)
    
    cell_width = WIDTH // 11
    scaled_images = []
    for img in images:
        if img is None:
            scaled_images.append(None)
            continue
        scale = cell_width / img.get_width()
        new_w = cell_width
        new_h = int(img.get_height() * scale)
        img = pygame.transform.scale(img, (new_w, new_h))
        scaled_images.append(img)

    while running:
        screen.fill((0, 0, 0))
        screen.blit(
            background_wishing,
            (WIDTH//2 - background_wishing.get_width()//2,
            HEIGHT//2 - background_wishing.get_height()//2)
        )
        max_h = max(img.get_height() for img in scaled_images if img)
        y = HEIGHT//2 - max_h//2
        x = (WIDTH - (cell_width * len(scaled_images) + 5 * (len(scaled_images) -1))) // 2

        for i, img in enumerate(scaled_images):
            color = get_color(raretes[i])
            border_color = darken(color)
            panel = pygame.Surface(
                (cell_width, max_h),
                pygame.SRCALPHA
            )
            pygame.draw.rect(
                panel,
                color,
                panel.get_rect(),
                border_radius=radius
            )

            if img:
                mask = pygame.Surface(
                    (cell_width, max_h),
                    pygame.SRCALPHA
                )
                pygame.draw.rect(
                    mask,
                    (255, 255, 255, 255),
                    mask.get_rect(),
                    border_radius=radius
                )
                img_surface = pygame.Surface(
                    (cell_width, max_h),
                    pygame.SRCALPHA
                )
                img_x = (cell_width - img.get_width()) // 2
                img_y = max_h - img.get_height()
                img_surface.blit(img, (img_x, img_y))
                img_surface.blit(mask, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
                panel.blit(img_surface, (0, 0))

            pygame.draw.rect(
                panel,
                border_color,
                panel.get_rect(),
                border,
                border_radius=radius
            )
            screen.blit(panel, (x, y))

            x += cell_width + ecart

        text = button_font.render(
            "Clic / Espace ==> continuer",
            True,
            (255, 255, 255)
        )

        screen.blit(
            text,
            (WIDTH//2 - text.get_width()//2,
            HEIGHT - 45)
        )

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                return False

            if event.type == pygame.KEYDOWN:
                if event.key in [pygame.K_SPACE, pygame.K_ESCAPE]:
                    return True

            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    return True

        pygame.display.flip()
        clock.tick(60)

    return True

def afficher_resultats(results, screen): 
    """
    Affiche les résultats un par un puis écran multi final
    """
    current_index = 0
    showing_results = True
    clock = pygame.time.Clock()
    animation_progress = 0.0  
    counter_y = int(HEIGHT * 50 / 900)
    name_y = int(HEIGHT * 100 / 900)
    instruction_y = int(HEIGHT * 50 / 900)

    while showing_results:

        screen.fill((255, 255, 255))
        screen.blit(
            background_wishing,
            (WIDTH//2 - background_wishing.get_width()//2,
            HEIGHT//2 - background_wishing.get_height()//2)
        )
        current_result = results[current_index]

        if current_result["character"]["type"] is not None:
            weapon_BG = scale_to_height(
                weapon_background_path(
                    current_result["character"]["type"]
                ),
                HEIGHT//2.5
            )
            screen.blit(
                weapon_BG,
                (WIDTH//2 - weapon_BG.get_width()//2,
                HEIGHT//2 - weapon_BG.get_height()//2)
            )
        
        afficher_splash_art(
            screen,
            current_result["splash_art"],
            animation_progress
        )

        if animation_progress < 1.0:
            animation_progress += 0.08  

        counter_text = font.render(
            f"{current_index + 1}/{len(results)}",
            True,
            (255, 255, 255)
        )

        screen.blit(
            counter_text,
            (WIDTH//2 - counter_text.get_width()//2,
            counter_y)
        )

        char_name = button_font.render(
            current_result["character"]["name"],
            True,
            (255, 255, 255)
        )

        screen.blit(
            char_name,
            (WIDTH//2 - char_name.get_width()//2,
            HEIGHT - name_y)
        )

        instruction = button_font.render(
            "Clic / Espace / Echap => quitter",
            True,
            (255, 255, 255)
        )

        screen.blit(
            instruction,
            (WIDTH//2 - instruction.get_width()//2,
            HEIGHT - instruction_y)
        )

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False, False
            if event.type == pygame.KEYDOWN:
                if event.key in [pygame.K_SPACE, pygame.K_RIGHT]:
                    current_index += 1
                    animation_progress = 0.0 
                    if current_index >= len(results):
                        ok = ecran_multi(results, screen)
                        if not ok:
                            return False, False

                        return True, True
                    
                elif event.key == pygame.K_LEFT and current_index > 0:
                    current_index -= 1
                    animation_progress = 0.0
                elif event.key == pygame.K_ESCAPE:
                    ok = ecran_multi(results, screen)
                    if not ok:
                        return False, False

                    return True, True

            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    current_index += 1
                    animation_progress = 0.0  
                    if current_index >= len(results):
                        ok = ecran_multi(results, screen)
                        if not ok:
                            return False, False

                        return True, True


        pygame.display.flip()
        clock.tick(60)

    return True, True

# --- Boucle principale ---
running = True
clock = pygame.time.Clock()
delta_time = 0.1
pity_y = int(HEIGHT * 10 / 900)
pity_y2 = int(HEIGHT * 50 / 900)
pity_y3 = int(HEIGHT * 90 / 900)
pity_x = int(HEIGHT * 20 / 900)
border_thickness = int(HEIGHT * 5 / 900)
border_radius = int(HEIGHT * 10 / 900)
while running:
    mouse_pos = pygame.mouse.get_pos()
    # --- Affichage background et banniere---
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
        screen.blit(background_wishing, (WIDTH//2 - background_wishing.get_width()//2, HEIGHT//2 - background_wishing.get_height()//2))
        afficher_splash_art(screen, wish_splash_art, animation_progress)
        
        if animation_progress < 1.0:
            animation_progress += 0.08
    
    # --- Boutons ---
    draw_button(screen, button_x1_rect, "Voeu x1", mouse_pos)
    draw_button(screen, button_x10_rect, "Voeu x10", mouse_pos)
    draw_left_buttons(screen, mouse_pos)
    
    # --- Texte Pity ---
    pity_text = button_font.render(f"Pity 5★: {pity_5_star}/{hard_pity}", True, (255, 215, 0))
    odd_5_star =(pity_5_star - soft_pity) * ((1 - 0.006) / (hard_pity - soft_pity)) + 0.006 if pity_5_star > soft_pity else 0.006
    pity_text_2 = button_font.render(f"Chance 5★: {min(odd_5_star*100, 100):.2f}%", True, (255, 215, 0))
    pity_text_3 = button_font.render(f"5★ limité garanti: {guaranteed_5_star}", True, (255, 215, 0))
    screen.blit(pity_text, (pity_x, pity_y))
    screen.blit(pity_text_2, (pity_x, pity_y2))
    screen.blit(pity_text_3, (pity_x, pity_y3))
    # --- Gestion events (boutons et souris) ---
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            if button_x1_rect.collidepoint(event.pos):
                result = wish(pity_5_star, pity_4_star, guaranteed_5_star, soft_pity, hard_pity, current_banner_index)
                wish_rarete = result["rarete"]
                wish_splash_art = result["splash_art"]
                animation_progress = 0.0  # Reset animation
                pity_5_star = result["new_pity_5_star"]
                pity_4_star = result["new_pity_4_star"]
                guaranteed_5_star = result["new_guaranteed_5_star"]
                if not play_video(result["animation"], screen, loop=False):
                    running = False

            elif button_x10_rect.collidepoint(event.pos):
                results = []
                for _ in range(10):
                    result = wish(pity_5_star, pity_4_star, guaranteed_5_star, soft_pity, hard_pity, current_banner_index)
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
                    animation_progress = 0.0

            elif wish_splash_art is not None:
                wish_rarete = None
                wish_splash_art = None
                animation_progress = 0.0
            else:
                for i, (rect, name) in enumerate(left_buttons):
                    if rect.collidepoint(event.pos):
                        current_banner_index = i
                        banniere_path = characters["5_star"][current_banner_index]["banniere"]
                        banniere = scale_with_borders(pygame.image.load(banniere_path).convert_alpha(), WIDTH, HEIGHT, border_percent=15)[0]
                        wish_splash_art = None
                        animation_progress = 0.0
    # --- Mettre à jour écran + gerer framerate constant ---
    pygame.display.flip()
    delta_time = clock.tick(60)/1000
    delta_time = min(delta_time, 0.05)

pygame.quit()
sys.exit()