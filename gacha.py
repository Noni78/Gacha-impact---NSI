import pygame
import sys
import random
import cv2
from library import *

# --- Paramètres Voeu ---
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
characters = {
    "5_star": [
        {#Columbina
            "name": "Columbina", 
            "image": "img/5_star/Columbina.png", 
            "banniere": "img/banniere/Columbina.png",
            "featured_4_star": ["Ifa", "Sethos", "Fischl"],
            "type": None
        },
        {#Zhongli
            "name": "Zhongli", 
            "image": "img/5_star/Zhongli.png", 
            "banniere": "img/banniere/Zhongli.png",
            "featured_4_star": ["Rosaria", "Lan Yan", "Yun Jin"],
            "type": None
        },
        {#Skirk
            "name": "Skirk", 
            "image": "img/5_star/Skirk.png", 
            "banniere": "img/banniere/Skirk.png",
            "featured_4_star": ["Diona", "Candace", "Dahlia"],
            "type": None
        },
        {#Mavuika
            "name": "Mavuika", 
            "image": "img/5_star/Mavuika.png", 
            "banniere": "img/banniere/Mavuika.png",
            "featured_4_star": ["Xiangling", "Yaoyao", "Iansan"],
            "type": None
        },
        {#Citlali
            "name": "Citlali", 
            "image": "img/5_star/Citlali.png", 
            "banniere": "img/banniere/Citlali.png",
            "featured_4_star": ["Diona", "Kachina", "Bennett"],
            "type": None
        },
        {#Xilonen
            "name": "Xilonen", 
            "image": "img/5_star/Xilonen.png", 
            "banniere": "img/banniere/Xilonen.png",
            "featured_4_star": ["Faruzan", "Beidou", "Yanfei"],
            "type": None
        },
        {#Shenhe
            "name": "Shenhe", 
            "image": "img/5_star/Shenhe.png", 
            "banniere": "img/banniere/Shenhe.png",
            "featured_4_star": ["Sucrose", "Mika", "Diona"],
            "type": None
        },
        {#Arlechinno
            "name": "Arlecchino", 
            "image": "img/5_star/Arlecchino.png", 
            "banniere": "img/banniere/Arlecchino.png",
            "featured_4_star": ["Lynette", "Freminet", "Xiangling"],
            "type": None
        },
    ],
    "5_star_perma": [
        {"name": "Qiqi", "image": "img/5_star/Qiqi.png","type": None},
        {"name": "Dehya", "image": "img/5_star/Dehya.png","type": None},
        {"name": "Diluc", "image": "img/5_star/Diluc.png", "type": None},
        {"name": "Jean", "image": "img/5_star/Jean.png", "type": None},
        {"name": "Keqing", "image": "img/5_star/Keqing.png", "type": None},
        {"name": "Mona", "image": "img/5_star/Mona.png", "type": None},
        {"name": "Tighnari", "image": "img/5_star/Tighnari.png", "type": None},
        {"name": "Yumemizuki Mizuki", "image": "img/5_star/Yumemizuki_Mizuki.png", "type": None},
    ],
    "4_star": [
        {"name": "Aino", "image": "img/4_star/Aino.png", "type": None},
        {"name": "Amber", "image": "img/4_star/Amber.png", "type": None},
        {"name": "Barbara", "image": "img/4_star/Barbara.png", "type": None},
        {"name": "Beidou", "image": "img/4_star/Beidou.png", "type": None},
        {"name": "Bennett", "image": "img/4_star/Bennett.png", "type": None},
        {"name": "Candace", "image": "img/4_star/Candace.png", "type": None},
        {"name": "Charlotte", "image": "img/4_star/Charlotte.png", "type": None},
        {"name": "Chevreuse", "image": "img/4_star/Chevreuse.png", "type": None},
        {"name": "Chongyun", "image": "img/4_star/Chongyun.png", "type": None},
        {"name": "Collei", "image": "img/4_star/Collei.png", "type": None},
        {"name": "Dahlia", "image": "img/4_star/Dahlia.png", "type": None},
        {"name": "Diona", "image": "img/4_star/Diona.png", "type": None},
        {"name": "Dori", "image": "img/4_star/Dori.png", "type": None},
        {"name": "Faruzan", "image": "img/4_star/Faruzan.png", "type": None},
        {"name": "Fischl", "image": "img/4_star/Fischl.png", "type": None},
        {"name": "Freminet", "image": "img/4_star/Freminet.png", "type": None},
        {"name": "Gaming", "image": "img/4_star/Gaming.png", "type": None},
        {"name": "Gorou", "image": "img/4_star/Gorou.png", "type": None},
        {"name": "Ifa", "image": "img/4_star/Ifa.png", "type": None},
        {"name": "Iansan", "image": "img/4_star/Iansan.png", "type": None},
        {"name": "Jahoda", "image": "img/4_star/Jahoda.png", "type": None},
        {"name": "Kachina", "image": "img/4_star/Kachina.png", "type": None},
        {"name": "Kaeya", "image": "img/4_star/Kaeya.png", "type": None},
        {"name": "Kaveh", "image": "img/4_star/Kaveh.png", "type": None},
        {"name": "Kirara", "image": "img/4_star/Kirara.png", "type": None},
        {"name": "Kujou Sara", "image": "img/4_star/Kujou_Sara.png", "type": None},
        {"name": "Kuki Shinobu", "image": "img/4_star/Kuki_Shinobu.png", "type": None},
        {"name": "Lan Yan", "image": "img/4_star/Lan_Yan.png", "type": None},
        {"name": "Layla", "image": "img/4_star/Layla.png", "type": None},
        {"name": "Lisa", "image": "img/4_star/Lisa.png", "type": None},
        {"name": "Lynette", "image": "img/4_star/Lynette.png", "type": None},
        {"name": "Mika", "image": "img/4_star/Mika.png", "type": None},
        {"name": "Ningguang", "image": "img/4_star/Ningguang.png", "type": None},
        {"name": "Noelle", "image": "img/4_star/Noelle.png", "type": None},
        {"name": "Ororon", "image": "img/4_star/Ororon.png", "type": None},
        {"name": "Razor", "image": "img/4_star/Razor.png", "type": None},
        {"name": "Rosaria", "image": "img/4_star/Rosaria.png", "type": None},
        {"name": "Sayu", "image": "img/4_star/Sayu.png", "type": None},
        {"name": "Sethos", "image": "img/4_star/Sethos.png", "type": None},
        {"name": "Shikanoin Heizou", "image": "img/4_star/Shikanoin_Heizou.png", "type": None},
        {"name": "Sucrose", "image": "img/4_star/Sucrose.png", "type": None},
        {"name": "Thoma", "image": "img/4_star/Thoma.png", "type": None},
        {"name": "Xiangling", "image": "img/4_star/Xiangling.png", "type": None},
        {"name": "Xingqiu", "image": "img/4_star/Xingqiu.png", "type": None},
        {"name": "Xinyan", "image": "img/4_star/Xinyan.png", "type": None},
        {"name": "Yun Jin", "image": "img/4_star/Yun_Jin.png", "type": None},
        {"name": "Yaoyao", "image": "img/4_star/Yaoyao.png", "type": None},
        {"name": "Yanfei", "image": "img/4_star/Yanfei.png", "type": None},
        
    ],
    "3_star": [
        {"name": "Thrilling Tale of Dragon Slayer", "image": "img/3_star/Thrilling_Tale_of_Dragon_Slayer.png", "type": "catalyst"},
        {"name": "Emerald Orb", "image": "img/3_star/Emerald_Orb.png", "type": "catalyst"},
        {"name": "Guide de magie", "image": "img/3_star/Magic_Guide.png", "type": "catalyst"},
        {"name": "Ferrous Shadow", "image": "img/3_star/Ferrous_Shadow.png","type": "claymore"},
        {"name": "Debate Club", "image": "img/3_star/Debate_Club.png","type": "claymore"},
        {"name": "Bloodtainted Greatsword", "image": "img/3_star/Bloodtainted_Greatsword.png","type": "claymore"},
        {"name": "Slingshot", "image": "img/3_star/Slingshot.png", "type": "bow"},
        {"name": "Arc du corbeau", "image": "img/3_star/Raven_Bow.png", "type": "bow"},
        {"name": "Sharpshooter's Oath", "image": "img/3_star/Sharpshooter's_Oath.png", "type": "bow"},
        {"name": "Black Tassel", "image": "img/3_star/Black_tassel.png", "type": "polearm"},
        {"name": "Lame froide", "image": "img/3_star/Cool_Steel.png", "type": "sword"},  
        {"name": "Messager de l'Aube", "image": "img/3_star/Harbinger_of_Dawn.png", "type": "sword"}, 
        {"name": "Syrider Sword", "image": "img/3_star/Skyrider_Sword.png", "type": "sword"}, 
    ]
}

# --- Initalisation ---
pygame.init()
HEIGHT = 300 #   <------------------------------------------------------------------------------ ici height
WIDTH = int(HEIGHT*16/9)
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Totally not a Genshin Impact wishing replica")
pygame.display.set_icon(pygame.image.load("img/icon.png").convert_alpha())
font_size = int(HEIGHT * 40 / 900)  
font = pygame.font.Font("font/genshin.ttf", font_size)
button_font_size = int(HEIGHT * 30 / 900)
button_font = pygame.font.Font("font/genshin.ttf", button_font_size)
try:
    cursor_img = pygame.image.load("img/Cursor.png").convert_alpha()
    cursor_size = int(HEIGHT * 32 / 900)
    cursor_img = pygame.transform.scale(cursor_img, (cursor_size, cursor_size))
    pygame.mouse.set_visible(False)
    use_custom_cursor = True
except:
    use_custom_cursor = False
wish_rarete = None
wish_splash_art = None
animation_progress = 0.0 

background = scale_to_height(pygame.image.load("img/background.png").convert_alpha(), HEIGHT)
background_wishing = scale_to_height(pygame.image.load("img/background_wishing.png").convert_alpha(), HEIGHT)
# --- Initialisation bannière ---
current_banner_index = random.randint(0,7) # l'index correspond aux 5 étoiles non perma dans l'ordre ou ils sont dans le dictionnaire character, ici c'est aléatoire
banniere_path = characters["5_star"][current_banner_index]["banniere"]
banniere, banner_border_w, banner_border_h = scale_with_borders(pygame.image.load(banniere_path).convert_alpha(), WIDTH, HEIGHT, border_percent=15)
# --- Boutons Voeux ---
button_height = int(HEIGHT * 60 / 900)
button_width = int(HEIGHT * 200 / 900)
button_spacing = int(HEIGHT * 20 / 900)
button_bottom_margin = int(HEIGHT * 80 / 900)
button_x1_rect = pygame.Rect(WIDTH//2 - button_width - button_spacing//2, HEIGHT - button_bottom_margin, button_width, button_height)
button_multi_rect = pygame.Rect(WIDTH//2 + button_spacing//2, HEIGHT - button_bottom_margin, button_width, button_height)
button_color = (255, 255, 230)
button_hover_color = (200, 200, 170)
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


def rarete(pity_5_star, pity_4_star, soft_pity=70, hard_pity=90,weight_5_star=proba_effective_5_star,weight_4_star=proba_init_4_star*(chance_globale)):
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
        weight_5_star += (pity_5_star - soft_pity) * ((1 - proba_init_5_star) / (hard_pity - soft_pity))

    weight_5_star = min(weight_5_star, 1 - weight_4_star)
    weight_3_star = 1 - weight_4_star - weight_5_star
    tirage = random.choices(
        ["5_star", "4_star", "3_star"],
        [weight_5_star, weight_4_star, weight_3_star]
        )[0]
    return tirage

def wish(pity_5_star, pity_4_star, guaranteed_5_star, soft_pity=70, hard_pity=90, current_banner_index=0):
    """
    Effectue 1 voeu et retourne tous les résultats.
    
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
    return pygame.image.load(f"img/Weapon_Background/{weapon}.png").convert_alpha()




def afficher_souris():
    mouse_pos = pygame.mouse.get_pos()
    cursor_x = mouse_pos[0] - cursor_img.get_width() // 2 
    cursor_y = mouse_pos[1] - cursor_img.get_height() // 2
    screen.blit(cursor_img, (cursor_x, cursor_y))

def ecran_multi(results, screen, border=5, ecart=int(5*10/multi)):
    """
    Écran résumé de la multi avec masque personnalisé
    """
    clock = pygame.time.Clock()
    running = True
    rarete_priority = {"5_star": 1, "5_star_perma": 2, "4_star": 3, "3_star": 4}
    results = sorted(results, key=lambda x: rarete_priority[x["rarete"]])
    
    try:
        mask_template = pygame.image.load("img/Mask.png").convert_alpha()
    except:
        print("Erreur: Impossible de charger img/Mask.png")
        mask_template = None
    try:
        background_multi = pygame.image.load("img/background_multi.png").convert_alpha()
        background_multi.set_alpha(170)
    except:
        background_multi = None
    
    images = []
    raretes = []
    for res in results:
        name = res["character"]["name"].replace(" ", "_")
        path_weapon = res["character"]["image"]
        rarete = res["rarete"]
        if rarete in ["5_star", "5_star_perma"]:
            path = f"img/5_star/multi/{name}.png"
        elif rarete == "4_star":
            path = f"img/4_star/multi/{name}.png"
        else:
            path = path_weapon
        try:
            img = pygame.image.load(path).convert_alpha()
            images.append(img)
        except:
            images.append(None)
        raretes.append(rarete)
    
    cell_width = WIDTH // (multi + 1)
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
        x = (WIDTH - (cell_width * len(scaled_images) + ecart * (len(scaled_images) - 1))) // 2

        for i, img in enumerate(scaled_images):
            color = get_color(raretes[i])
            border_color = darken(color)
            
            panel = pygame.Surface((cell_width, max_h), pygame.SRCALPHA)
            
            if mask_template is not None:
                mask_scaled = pygame.transform.scale(mask_template, (cell_width, max_h))
                
                border_surface = pygame.Surface((cell_width, max_h), pygame.SRCALPHA)
                border_surface.fill(border_color)
                border_surface.blit(mask_scaled, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
                panel.blit(border_surface, (0, 0))
                
                inner_width = cell_width - border * 2
                inner_height = max_h - border * 2
                if inner_width > 0 and inner_height > 0:
                    mask_inner = pygame.transform.scale(mask_template, (inner_width, inner_height))
                    
                    inner_surface = pygame.Surface((inner_width, inner_height), pygame.SRCALPHA)
                    inner_surface.fill(color)
                    inner_surface.blit(mask_inner, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
                    panel.blit(inner_surface, (border, border))
                    
                    if img:
                        img_surface = pygame.Surface((inner_width, inner_height), pygame.SRCALPHA)

                        # --- Background derrière l'image ---
                        if background_multi:
                            bg = pygame.transform.scale(background_multi, (inner_width, inner_height))
                            img_surface.blit(bg, (0, 0))

                        # --- Image du perso ---
                        img_x = (inner_width - img.get_width()) // 2
                        img_y = inner_height - img.get_height()
                        img_surface.blit(img, (img_x, img_y))

                        # --- Masque ---
                        img_surface.blit(mask_inner, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)

                        panel.blit(img_surface, (border, border))

            else:
                pygame.draw.rect(panel, color, panel.get_rect(), border_radius=140)
                if img:
                    mask = pygame.Surface((cell_width, max_h), pygame.SRCALPHA)
                    pygame.draw.rect(mask, (255, 255, 255, 255), mask.get_rect(), border_radius=140)
                    img_surface = pygame.Surface((cell_width, max_h), pygame.SRCALPHA)
                    img_x = (cell_width - img.get_width()) // 2
                    img_y = max_h - img.get_height()
                    img_surface.blit(img, (img_x, img_y))
                    img_surface.blit(mask, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
                    panel.blit(img_surface, (0, 0))
                pygame.draw.rect(panel, border_color, panel.get_rect(), border, border_radius=140)
            
            screen.blit(panel, (x, y))
            x += cell_width + ecart

        text = button_font.render("Clic / Espace ==> continuer", True, (255, 255, 255))
        screen.blit(text, (WIDTH//2 - text.get_width()//2, HEIGHT - 45))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                if event.key in [pygame.K_SPACE, pygame.K_ESCAPE]:
                    return True
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    return True

        if use_custom_cursor:
            afficher_souris()
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
                HEIGHT
            )
            screen.blit(
                weapon_BG,
                (WIDTH//2 - weapon_BG.get_width()//2,
                HEIGHT//2 - weapon_BG.get_height()//2)
            )
        
        animer_splash_art(
            screen,
            current_result["splash_art"],
            WIDTH,
            HEIGHT,
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

def actualiser_text_pity():
    pity_text = button_font.render(f"Pity 5★: {pity_5_star}/{hard_pity}", True, (255, 215, 0))
    odd_5_star =(pity_5_star - soft_pity) * ((1 -(proba_effective_5_star)) / (hard_pity - soft_pity)) + (proba_effective_5_star) if pity_5_star > soft_pity else (proba_effective_5_star)
    pity_text_2 = button_font.render(f"chance 5★: {min(odd_5_star*100, 100):.2f}%", True, (255, 215, 0))
    pity_text_3 = button_font.render(f"5★ limité garanti: {guaranteed_5_star}", True, (255, 215, 0))
    screen.blit(pity_text, (pity_x, pity_y))
    screen.blit(pity_text_2, (pity_x, pity_y2))
    screen.blit(pity_text_3, (pity_x, pity_y3))
    return 

def boutons():
    draw_button(screen, button_x1_rect, "Voeu x1", mouse_pos)
    draw_button(screen, button_multi_rect, f"Voeu x{multi}", mouse_pos)
    draw_left_buttons(screen, mouse_pos,left_buttons,button_font)
    return

def afficher_banniere():
    border_rect = pygame.Rect(
            banner_border_w - border_thickness,
            banner_border_h - border_thickness,
            banniere.get_width() + (border_thickness * 2),
            banniere.get_height() + (border_thickness * 2))
    pygame.draw.rect(screen, (178, 180, 166), border_rect, border_thickness, border_radius=border_radius)
    screen.blit(banniere, (banner_border_w, banner_border_h))
    return

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
        afficher_banniere()
    else:
        screen.blit(background_wishing, (WIDTH//2 - background_wishing.get_width()//2, HEIGHT//2 - background_wishing.get_height()//2))
        animer_splash_art(screen, wish_splash_art, WIDTH,HEIGHT,animation_progress)
        
        if animation_progress < 1.0:
            animation_progress += 0.1
    
    boutons()
    actualiser_text_pity()
    
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

            elif button_multi_rect.collidepoint(event.pos):
                results = []
                for _ in range(multi):
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

    
    if use_custom_cursor:
        afficher_souris()
    # --- Mettre à jour écran + gerer vitesse constanteh ---
    pygame.display.flip()
    delta_time = clock.tick(60)/1000
    delta_time = min(delta_time, 0.05)

pygame.quit()
sys.exit()