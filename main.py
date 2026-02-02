import pygame
import sys
from library import *
from character import *
from settings import *

#########################
# --- Initalisation --- #
#########################

pygame.init()
background = scale_to_height(pygame.image.load("img/background.png").convert_alpha(), HEIGHT)
background_wishing = scale_to_height(pygame.image.load("img/background_wishing.png").convert_alpha(), HEIGHT)
banniere, banner_border_w, banner_border_h = scale_with_borders(pygame.image.load(banniere_path).convert_alpha(), WIDTH, HEIGHT, border_percent=15)

#########################################
# --- Fonctions (non délocalizable) --- #
########################################

def actualiser_text_pity():
    pity_text = button_font.render(f"Pity 5★: {pity_5_star}/{hard_pity}", True, (255, 215, 0))
    odd_5_star =(pity_5_star - soft_pity) * ((1 -(proba_effective_5_star)) / (hard_pity - soft_pity)) + (proba_effective_5_star) if pity_5_star > soft_pity else (proba_effective_5_star)
    pity_text_2 = button_font.render(f"chance 5★: {min(odd_5_star*100, 100):.2f}%", True, (255, 215, 0))
    pity_text_3 = button_font.render(f"5★ limité garanti: {garanti}", True, (255, 215, 0))
    capture_radiance = button_font.render(f"Stack: {stack_capture_radiance}", True, (255, 215, 0))
    screen.blit(pity_text, (pity_x, pity_y))
    screen.blit(pity_text_2, (pity_x, pity_y2))
    screen.blit(pity_text_3, (pity_x, pity_y3))
    screen.blit(capture_radiance, (capture_radiance_x, capture_radiance_y))
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

def afficher_resultats(results, screen,type): 
    """
    Affiche les résultats un par un puis écran multi final
    """
    current_index = 0
    showing_results = True
    clock = pygame.time.Clock()
    animation_progress = 0.0  
    name_y = int(HEIGHT * 100 / 900)
    instruction_y = int(HEIGHT * 50 / 900)

    while showing_results:

        screen.fill((255, 255, 255))
        screen.blit(
            background_wishing,
            (WIDTH//2 - background_wishing.get_width()//2,
            HEIGHT//2 - background_wishing.get_height()//2)
        )
        if type == "multi":
            current_result = results[current_index]
        else:
            current_result = results

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
            animation_progress
        )

        if animation_progress < 1.0:
            animation_progress += 0.08  
        if type == "multi":
            counter_y = int(HEIGHT * 50 / 900)
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
                if type == "multi":
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
                else:
                    if event.key in [pygame.K_SPACE, pygame.K_RIGHT,pygame.K_ESCAPE]: 
                        animation_progress = 0.0
                        return True, True

            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    if type == "multi":
                        current_index += 1
                        animation_progress = 0.0  
                        if current_index >= len(results):
                            ok = ecran_multi(results, screen)
                            if not ok:
                                return False, False

                            return True, True
                    else:
                        animation_progress = 0.0
                        return True,True


        pygame.display.flip()
        clock.tick(60)

    return True, True

def boutons():
    draw_button(screen, button_x1, "Voeu x1", mouse_pos,button_hover_color,button_color,button_font)
    draw_button(screen, button_multi, f"Voeu x{multi}", mouse_pos,button_hover_color,button_color,button_font)
    draw_button(screen, button_save, f"save", mouse_pos,button_hover_color,button_color,button_font)
    draw_banniere_buttons(screen, mouse_pos,banniere_buttons,button_font)
    return

#############################
# --- Boucle principale --- #
#############################

running = True

while running:
    mouse_pos = pygame.mouse.get_pos()
    screen.blit(background, (WIDTH//2 - background.get_width()//2, HEIGHT//2 - background.get_height()//2))
    if wish_splash_art is None:
        afficher_banniere()
    boutons()
    actualiser_text_pity()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            if button_x1.collidepoint(event.pos):
                result = wish(pity_5_star, pity_4_star, garanti, current_banner_index,stack_capture_radiance, soft_pity, hard_pity) 
                wish_rarete = result["rarete"]
                wish_splash_art = result["splash_art"]
                animation_progress = 0.0  
                pity_5_star = result["new_pity_5_star"]
                pity_4_star = result["new_pity_4_star"]
                garanti = result["new_garanti"]
                stack_capture_radiance = result["new_stack_capture_radiance"]
                if not play_video(result["animation"], screen, loop=False):
                    running = False
                continue_running, reset_to_banniere = afficher_resultats(result, screen, type= "single")
                if not continue_running:
                    running = False
                if reset_to_banniere:
                    wish_rarete = None
                    wish_splash_art = None
                    animation_progress = 0.0  

            elif button_multi.collidepoint(event.pos):
                results = []
                for _ in range(multi):
                    result = wish(pity_5_star, pity_4_star, garanti, current_banner_index,stack_capture_radiance, soft_pity, hard_pity)
                    results.append(result)
                    pity_5_star = result["new_pity_5_star"]
                    pity_4_star = result["new_pity_4_star"]
                    garanti = result["new_garanti"]
                    stack_capture_radiance = result["new_stack_capture_radiance"]

                rarete_priority = {"5_star":1,"5_star_perma":2,"4_star":3,"3_star":4}   
                best_result = min(results, key=lambda x: rarete_priority[x["rarete"]])
                if not play_video(best_result["animation"], screen, loop=False):
                    running = False
                continue_running, reset_to_banniere = afficher_resultats(results, screen,type = "multi")
                if not continue_running:
                    running = False
                if reset_to_banniere:
                    wish_rarete = None
                    wish_splash_art = None
                    animation_progress = 0.0

            elif button_save.collidepoint(event.pos):
                sauvegarder(pity_5_star,pity_4_star,garanti,current_banner_index,stack_capture_radiance)
            
            elif wish_splash_art is not None:
                wish_rarete = None
                wish_splash_art = None
                animation_progress = 0.0
            else:
                for i, (rect, name) in enumerate(banniere_buttons):
                    if rect.collidepoint(event.pos):
                        current_banner_index = i
                        banniere_path = characters["5_star"][current_banner_index]["banniere"]
                        banniere = scale_with_borders(pygame.image.load(banniere_path).convert_alpha(), WIDTH, HEIGHT, border_percent=15)[0]
                        wish_splash_art = None
                        animation_progress = 0.0

    
    if use_custom_cursor:
        afficher_souris()
        
    pygame.display.flip()
    delta_time = clock.tick(60)/1000
    delta_time = min(delta_time, 0.05)

pygame.quit()
sys.exit()