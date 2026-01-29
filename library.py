import pygame

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