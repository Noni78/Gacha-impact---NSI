import pygame
import random
import cv2
# --- Affichage ---
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

def draw_left_buttons(screen, mouse_pos, left_buttons,button_font):
    for rect, name in left_buttons:
        color = (140, 140, 110) if rect.collidepoint(mouse_pos) else (178, 180, 140)
        pygame.draw.rect(screen, color, rect, border_radius=5)
        text_surf = button_font.render(name, True, (78, 80, 40))
        text_rect = text_surf.get_rect(center=rect.center)
        screen.blit(text_surf, text_rect)

def animer_splash_art(screen, splash_art, WIDTH, HEIGHT,progress=1.0):
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

def play_video(video_path, screen, WIDTH, HEIGHT, loop=False):
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

# --- Calculs ---
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
