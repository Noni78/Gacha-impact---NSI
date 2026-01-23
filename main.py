import customtkinter as ctk
import random
from PIL import Image


# ---------------- FENÊTRE ----------------
height_ = 600
dimensions = (int((16 / 10) * height_), height_)
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")
fenetre = ctk.CTk()
fenetre.title("Gacha Impact")
fenetre.geometry(f"{dimensions[0]}x{dimensions[1]}")
fenetre.resizable(False, False)
content_frame = ctk.CTkFrame(
    fenetre,
    fg_color="transparent",
    bg_color="transparent"
)

# ---------------- PITY ----------------
pity_5_star = 80
pity_4_star = 0
soft_pity = 70
hard_pity = 90
wish_state = "ready"
guaranteed_5_star = False


# ---------------- PERSONNAGES ----------------
characters = {
    "5★": [
        {"name": "Columbina", "image": "doc/5_star/Columbina.png"},
        {"name": "Zhongli", "image": "doc/5_star/Zhongli.png"},
    ],
    "5★ permanent": [
        {"name": "Qiqi", "image": "doc/5_star/Qiqi.png"},
    ],

    "4★": [
        {"name": "Bennett", "image": "doc/4_star/Bennett.png"},
    ],

    "3★": [
        {"name": "Thrilling Tale of Dragon Slayer", "image": "doc/3_star/TTDS.png"},
        {"name": "Ferrous Shadow", "image": "doc/3_star/Ferrous_Shadow.png"},
    ]
}


# ---------------- UTILS ----------------

def get_random_character(rarity):
    return random.choice(characters[rarity])

def resize_image(path, max_w, max_h):
    img = Image.open(path)
    img.thumbnail((max_w, max_h), Image.Resampling.LANCZOS)
    return img

def load_character_image(path):
    img = resize_image(
        path,
        dimensions[0],
        int(dimensions[1] * 0.88)
    )
    return ctk.CTkImage(img, size=img.size)

def resize_gif_frames(path, max_w, max_h):

    frames = []

    try:
        gif = Image.open(path)

        while True:

            frame = gif.copy()
            frame.thumbnail((max_w, max_h), Image.Resampling.LANCZOS)

            frames.append(
                ctk.CTkImage(
                    light_image=frame,
                    size=(max_w, max_h)
                )
            )

            gif.seek(len(frames))

    except:
        pass

    return frames


# ---------------- RARETÉ ----------------

def rarete():

    global pity_5_star, pity_4_star

    w5 = 0.006
    w4 = 0.051


    # Hard pity
    if pity_5_star >= hard_pity:

        pity_5_star = 0
        pity_4_star += 1

        return "5★"


    # Pity 4*
    if pity_4_star >= 10:

        pity_4_star = 0
        pity_5_star += 1

        return "4★"


    # Soft pity
    if pity_5_star > soft_pity:

        w5 += (pity_5_star - soft_pity) * (
            (1 - 0.006) / (hard_pity - soft_pity)
        )


    w5 = min(w5, 1 - w4)
    w3 = 1 - w4 - w5


    tirage = random.choices(
        ["5★", "4★", "3★"],
        [w5, w4, w3]
    )[0]


    if tirage == "5★":
        pity_5_star = 0
        pity_4_star += 1

    elif tirage == "4★":
        pity_4_star = 0
        pity_5_star += 1

    else:
        pity_5_star += 1
        pity_4_star += 1


    return tirage


# ---------------- ANIMATION ----------------

def play_animation(i, rarity, frames):

    if i < len(frames):

        image_label.configure(
            image=frames[i],
            text=""
        )

        fenetre.after(
            33,
            lambda: play_animation(i + 1, rarity, frames)
        )

    else:
        show_splash(rarity)


# ---------------- WISH ----------------

def voeu():

    global wish_state

    wish_state = "in_progress"

    rarity = rarete()

    wish_button.pack_forget()


    if rarity == "5★":
        frames = wishing_animation_5_stars

    elif rarity == "4★":
        frames = wishing_animation_4_stars

    else:
        frames = wishing_animation_3_stars
    if frames:
        play_animation(0, rarity, frames)

    else:
        if rarity == "5★" and not guaranteed_5_star and random.random() < 0.5:
            perso = get_random_character("5★ permanent")
            guaranteed_5_star = True
            show_splash("5★ permanent", perso)
        else:
            perso = get_random_character(rarity)
            guaranteed_5_star = False
            show_splash(rarity, perso)

# ---------------- RESULTAT ----------------

def show_splash(rarity, perso=None):

    global wish_state

    wish_state = "finished"

    if perso is None:
        if rarity == "5★" and random.random() < 0.5:
            perso = get_random_character("5★ permanent")
            actual_rarity = "5★ permanent"
        else:
            perso = get_random_character(rarity)
            actual_rarity = rarity
    else:
        actual_rarity = rarity

    image = load_character_image(perso["image"])

    image_label.configure(
        image=image,
        text=f'{actual_rarity}  -  {perso["name"]}',
        compound="top",         
        anchor="n",             
        justify="center"
    )

    image_label.image = image


def hide_splash():

    global wish_state

    if wish_state == "finished":

        wish_state = "ready"

        image_label.configure(
            image="",
            text=f"Pity : {pity_5_star}"
        )

        wish_button.pack(pady=10)


# ---------------- GIFS ----------------

wishing_animation_5_stars = resize_gif_frames(
    "doc/5_star/animation_5.gif",
    dimensions[0],
    int(dimensions[1] * 0.88)
)

wishing_animation_4_stars = resize_gif_frames(
    "doc/4_star/animation_4.gif",
    dimensions[0],
    int(dimensions[1] * 0.88)
)

wishing_animation_3_stars = resize_gif_frames(
    "doc/3_star/animation_3.gif",
    dimensions[0],
    int(dimensions[1] * 0.88)
)


# ---------------- UI ----------------

image_label = ctk.CTkLabel(
    fenetre,
    text="Bienvenue dans Gacha Impact",
    font=("Cinzel", 16),
    width=dimensions[0],
    height=int(dimensions[1] * 0.88)
)

image_label.pack(fill="both", expand=True)
image_label.bind("<Button-1>", lambda e: hide_splash())

wish_button = ctk.CTkButton(
    content_frame,
    text="Faire un vœu",
    width=200,
    height=50,
    font=("Cinzel", 16, "bold"),
    command=voeu
)

wish_button.pack(pady=10)
content_frame.pack(fill="both", expand=True)


# ---------------- START ----------------

fenetre.mainloop()