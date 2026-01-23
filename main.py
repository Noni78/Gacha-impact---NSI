import customtkinter as ctk
import random
from PIL import Image

# --- Paramètres fenêtre ---
height_ = 600
dimensions = (int((16/10)*height_), height_)
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")
fenetre = ctk.CTk()
fenetre.title("Gacha Impact")
fenetre.geometry(f"{dimensions[0]}x{dimensions[1]}")
fenetre.resizable(False, False)

# --- Paramètres voeu ---
pity_5_star = 0
pity_4_star = 9
soft_pity = 70
hard_pity = 90
in_wish = False


# --- Fonctions ---
def rarete():
    """Détermine rareté"""
    global pity_5_star, pity_4_star

    weight_5_star = 0.006
    weight_4_star = 0.051

    # Hard pity 5★
    if pity_5_star >= hard_pity:
        rarete_tirage = "5★"
        pity_5_star = 0
        pity_4_star += 1

    # Pity 4★
    elif pity_4_star >= 10:
        rarete_tirage = "4★"
        pity_4_star = 0
        pity_5_star += 1

    else:
        # Soft pity
        if pity_5_star > soft_pity:
            weight_5_star += (pity_5_star - soft_pity) * (
                (1.0 - 0.006) / (hard_pity - soft_pity)
            )

        weight_5_star = min(weight_5_star, 1.0 - weight_4_star)
        weight_3_star = 1.0 - weight_4_star - weight_5_star

        tirage = random.choices(
            ["5★", "4★", "3★"],
            [weight_5_star, weight_4_star, weight_3_star]
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

    return rarete_tirage, pity_5_star


def resize_image(image_path, max_width, max_height):
    img = Image.open(image_path)
    img.thumbnail((max_width, max_height), Image.Resampling.LANCZOS)
    return img


def resize_gif_frames(path, max_width, max_height):
    frames = []

    try:
        gif = Image.open(path)

        while True:
            frame = gif.copy()
            frame.thumbnail((max_width, max_height), Image.Resampling.LANCZOS)

            frames.append(
                ctk.CTkImage(
                    light_image=frame,
                    size=(max_width, max_height)
                )
            )

            gif.seek(len(frames))

    except EOFError:
        pass
    except FileNotFoundError:
        pass

    return frames


def voeu():
    global in_wish

    if in_wish:
        return

    in_wish = True

    rarete_tirage, pity = rarete()

    wish_button_1.pack_forget()

    if rarete_tirage == "5★":
        frames = frames_5
    elif rarete_tirage == "4★":
        frames = frames_4
    else:
        frames = frames_3

    if frames:
        play_animation(0, rarete_tirage, frames, pity)
    else:
        fenetre.after(500, lambda: show_splash(rarete_tirage, pity))


def play_animation(frame_index, rarete_tirage, frames, pity):

    if frame_index < len(frames):

        image_label.configure(
            image=frames[frame_index],
            text=""
        )

        fenetre.after(
            33,
            lambda: play_animation(
                frame_index + 1,
                rarete_tirage,
                frames,
                pity
            )
        )

    else:
        show_splash(rarete_tirage, pity)


def show_splash(rarete_tirage, pity):
    global in_wish

    if rarete_tirage == "5★":
        image_label.configure(image=splash_5_star, text="")

    elif rarete_tirage == "4★":
        image_label.configure(image=splash_4_star, text="")

    else:
        image_label.configure(image=splash_3_star, text="")

    pity_label.configure(text=f"Pity : {pity}")

    pity_label.place(
        x=dimensions[0] - 150,
        y=20,
        width=130,
        height=50
    )

    wish_button_1.pack(pady=10)

    in_wish = False


def hide_image():
    global in_wish

    if in_wish:
        in_wish = False
        image_label.configure(
            image="",
            text="Bienvenue dans Gacha Impact!"
            )

        pity_label.place_forget()
    wish_button_1.pack(pady=10)


# --- Charger images ---
try:
    img_5 = resize_image(
        "doc/5_star/Columbina.png",
        dimensions[0],
        int(dimensions[1] * 0.88)
    )

    img_4 = resize_image(
        "doc/4_star/Bennett.png",
        dimensions[0],
        int(dimensions[1] * 0.88)
    )

    img_3 = resize_image(
        "doc/3_star/TTDS.png",
        dimensions[0],
        int(dimensions[1] * 0.88)
    )

    splash_5_star = ctk.CTkImage(img_5, size=img_5.size)
    splash_4_star = ctk.CTkImage(img_4, size=img_4.size)
    splash_3_star = ctk.CTkImage(img_3, size=img_3.size)

    frames_5 = resize_gif_frames(
        "doc/5_star/animation_5.gif",
        dimensions[0],
        int(dimensions[1] * 0.88)
    )

    frames_4 = resize_gif_frames(
        "doc/4_star/animation_4.gif",
        dimensions[0],
        int(dimensions[1] * 0.88)
    )

    frames_3 = resize_gif_frames(
        "doc/3_star/animation_3.gif",
        dimensions[0],
        int(dimensions[1] * 0.88)
    )

except FileNotFoundError:

    splash_5_star = splash_4_star = splash_3_star = None
    frames_5 = frames_4 = frames_3 = []


# --- Label principal ---
image_label = ctk.CTkLabel(
    fenetre,
    text="Bienvenue dans Gacha Impact!",
    text_color="white",
    font=("Cinzel", 14),
    image=None,
    width=dimensions[0],
    height=int(dimensions[1] * 0.88),
    fg_color="transparent"
)

image_label.pack(fill="both", expand=True, padx=5, pady=5)

image_label.bind("<Button-1>", lambda e: hide_image())


# --- Label pity ---
pity_label = ctk.CTkLabel(
    fenetre,
    text="Pity : 0",
    text_color="white",
    font=("Cinzel", 16, "bold"),
    fg_color="#1a1a1a",
    corner_radius=10
)


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


# --- Lancement ---
fenetre.mainloop()
