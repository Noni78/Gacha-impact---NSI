import customtkinter as ctk
import random
from PIL import Image

dimensions = (800, 450)
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

fenetre = ctk.CTk()
fenetre.title("Gacha Impact")
fenetre.geometry(f"{dimensions[0]}x{dimensions[1]}")
fenetre.resizable(False, False)

# --- Paramètres pity ---
pity_5_star = 0
pity_4_star = 0
soft_pity = 70
hard_pity = 90
in_wish = False

# --- Charger images ---
try:
    splash_5_star = ctk.CTkImage(light_image=Image.open("doc/5_star/Columbina.png"), size=dimensions)
    splash_4_star = splash_5_star  
    splash_3_star = splash_5_star  
    
    
    animation_gif = Image.open("doc/5_star/animation_5.gif")
    
    frames = []
    try:
        while True:
            frame = animation_gif.copy()
            frames.append(ctk.CTkImage(light_image=frame, size=dimensions))
            animation_gif.seek(len(frames))
    except EOFError:
        pass
except FileNotFoundError as e:
    splash_5_star = splash_4_star = splash_3_star = None
    frames = []
    print(f"Erreur : fichier manquant - {e}")

# --- Label images et GIF ---
image_label = ctk.CTkLabel(fenetre,
                            text="Bienvenue dans Gacha Impact!",
                            text_color="white",
                            font=("Cinzel", 14),
                            image=None,
                            width=dimensions[0],
                            height=int(dimensions[1] * 0.88))
image_label.pack(fill="both", expand=True, padx=5, pady=5)
image_label.bind("<Button-1>", lambda e: hide_image())

# --- Bouton voeu ---
wish_button_1 = ctk.CTkButton(
    fenetre,
    text="Faire un vœu",
    width=200,
    height=50,
    corner_radius=20,
    fg_color="#4f6ef7",
    hover_color="#6f8eff",
    text_color="white",
    font=("Cinzel", 16, "bold"),
    border_width=2,
    border_color="#2e4fb8"
)
wish_button_1.pack(pady=10)
wish_button_1.bind("<ButtonRelease-1>", lambda e: voeu())

# --- Fonctions ---
def rarete():
    """Détermine la rareté du tirage et met à jour le pity."""
    global pity_5_star, pity_4_star
    rarete_tirage = ""
    weight_5_star = 0.006
    weight_4_star = 0.051
    pity = pity_5_star

    # Hard pity
    if pity_5_star >= hard_pity:
        rarete_tirage = "5★"
        pity_5_star = 0
        pity_4_star += 1
    # 4★ guarantee
    elif pity_4_star >= 10:
        rarete_tirage = "4★"
        pity_4_star = 0
        pity_5_star += 1
    else:
        # Soft pity pour 5★
        if pity_5_star > soft_pity:
            weight_5_star = 0.006 + (pity_5_star - soft_pity) * ((1.0 - 0.006) / (hard_pity - soft_pity))
        weight_5_star = min(weight_5_star, 1.0 - weight_4_star)
        weight_3_star = 1.0 - weight_4_star - weight_5_star

        tirage = random.choices(
            population=["5★", "4★", "3★"],
            weights=[weight_5_star, weight_4_star, weight_3_star],
            k=1
        )[0]
        rarete_tirage = tirage

        if tirage == "5★":
            pity_5_star = 0
            pity_4_star += 1
        elif tirage == "4★":
            pity_4_star = 0
            pity_5_star += 1
        else:
            pity_5_star += 1
            pity_4_star += 1

    return rarete_tirage, pity

def voeu():
    """Lancer un tirage et afficher l'animation / splash."""
    global in_wish
    if in_wish:  # éviter spam
        return
    in_wish = True
    rarete_tirage, pity = rarete()
    wish_button_1.pack_forget()
    image_label.configure(image=None, text=f"Rareté : {rarete_tirage}\nPity : {pity}")

    if frames:
        play_animation(0, rarete_tirage)
    else:
        fenetre.after(1000, lambda: show_splash(rarete_tirage))

def play_animation(frame_index, rarete_tirage):
    """Jouer le GIF frame par frame."""
    if frame_index < len(frames):
        image_label.configure(image=frames[frame_index], text="")
        fenetre.after(100, lambda: play_animation(frame_index + 1, rarete_tirage))
    else:
        show_splash(rarete_tirage)

def show_splash(rarete_tirage):
    """Afficher le splash final selon la rareté."""
    global in_wish
    if rarete_tirage == "5★":
        image_label.configure(image=splash_5_star, text="")
    elif rarete_tirage == "4★":
        image_label.configure(image=splash_4_star, text="")
    else:
        image_label.configure(image=splash_3_star, text="")
    wish_button_1.pack(pady=10)
    in_wish = False

def hide_image():
    """Réinitialiser l'affichage au clic."""
    global in_wish
    if in_wish:
        return
    image_label.configure(image=None, text="Appuyez sur le bouton pour relancer!")


fenetre.mainloop()
