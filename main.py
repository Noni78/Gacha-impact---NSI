import customtkinter as tk
import random 

fenetre = tk.Tk()
fenetre.title("Gacha Impact")
fenetre.geometry("400x400")
fenetre.resizable(False, False)

#paramètres pity
pity_5_star = 0
pity_4_star = 0
soft_pity = 70
hard_pity = 90

def voeu():
    rarete()

def rarete(event):
    global pity_5_star, pity_4_star, soft_pity, hard_pity
    rarete = ""
    weight_5_star = 0.006
    weight_4_star = 0.051
    pity = pity_5_star

    # Hard pity
    if pity_5_star >= hard_pity:
        rarete = "5★"
        pity_5_star = 0
        pity_4_star += 1

    # 4★ guarantee
    elif pity_4_star >= 10:
        rarete = "4★"
        pity_4_star = 0
        pity_5_star += 1


    else:
        # weight 5 star
        if pity_5_star > soft_pity:
            weight_5_star = 0.006 + (pity_5_star - soft_pity) * ((1.0 - 0.006) / (hard_pity - soft_pity))
        else:
            weight_5_star = 0.006

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

    label.config(text=f"Vous avez obtenu un objet de rareté : {rarete_tirage}\nPity : {pity}")



label = tk.Label(fenetre, text="Bienvenue dans Gacha Impact!")
label.pack()

wish_button_1 = tk.Button(
    fenetre,
    text="Faire un vœu",
    width=20,    
    height=2,
    bg='#4f6ef7',  
    fg='white',     
    font=('Cinzel', 16, 'bold'), 
    activebackground='#6f8eff',  
    activeforeground='white',
    bd=3,          
    relief='raised', 
    highlightthickness=0
)
wish_button_1.pack()
wish_button_1.bind("<ButtonRelease-1>", rarete)

fenetre.mainloop()