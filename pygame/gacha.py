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

#image de fond
background = scale_to_height(pygame.image.load("pygame/img/background.png").convert_alpha(), HEIGHT)

# Définir le bouton
button_rect = pygame.Rect(WIDTH//2 - 100, HEIGHT - 80, 200, 60)
button_color = (100, 150, 255)
button_hover_color = (150, 200, 255)

# Paramètres Gacha
pity_5_star =90
pity_4_star = 0
soft_pity = 70
hard_pity = 90
guaranteed_5_star = False
wish_rarete = None

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
    if pity_4_star >= 10:
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
    pygame.draw.rect(screen, (0, 0, 0), rect, 3, border_radius=30) 
    
    button_text = button_font.render(text, True, (0, 0, 0))
    text_rect = button_text.get_rect(center=rect.center)
    screen.blit(button_text, text_rect)

# --- Boucle principale ---
running = True
clock = pygame.time.Clock()
delta_time = 0.1

while running:
    mouse_pos = pygame.mouse.get_pos()
    
    screen.fill((255, 255, 255))
    text = font.render("Not Genshin Impact", True, (0, 0, 0))
    screen.blit(background, (WIDTH//2 - background.get_width()//2, HEIGHT//2 - background.get_height()//2))
    if wish_rarete:
        screen.blit(wish_splash_art, (WIDTH//2 - wish_splash_art.get_width()//2, HEIGHT//2 - wish_splash_art.get_height()//2))
        
    screen.blit(text, (WIDTH//2 - text.get_width()//2, 20))
    
    draw_button(screen, button_rect, "Voeu x1", mouse_pos)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1: 
                if button_rect.collidepoint(event.pos):
                    wish_rarete = rarete(pity_5_star, pity_4_star)
                    if wish_rarete == "5_star":
                        pity_5_star = 0
                        pity_4_star += 1
                        wish_animation = "pygame/videos/pull_" + wish_rarete + ".mp4"
                        if not guaranteed_5_star and random.random() < 0.5:
                            guaranteed_5_star = True
                            wish_rarete = "5_star_perma"
                    elif wish_rarete == "4_star":
                        wish_animation = "pygame/videos/pull_" + wish_rarete + ".mp4"
                        pity_4_star = 0
                        pity_5_star += 1
                    else:
                        wish_animation = "pygame/videos/pull_" + wish_rarete + ".mp4"
                        pity_5_star += 1
                        pity_4_star += 1
                    wish_result_character = random.choice(characters[wish_rarete])
                    wish_splash_art = scale_to_height(pygame.image.load(wish_result_character["image"]).convert_alpha(), HEIGHT)
                    
                    if not play_video(wish_animation, screen, loop=False):
                        running = False 
                    
    pygame.display.flip()
    delta_time = clock.tick(60)/1000
    delta_time = min(delta_time, 0.05)

pygame.quit()
sys.exit()
