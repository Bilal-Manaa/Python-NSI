import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageDraw, ImageTk
import os
import random
import ctypes
ctypes.windll.shcore.SetProcessDpiAwareness(1)

fenetre = tk.Tk()
fenetre.title("Jeu Zelda")
fenetre.geometry("1800x1034")

imageMapVillePIL  = Image.open("map1.png").resize((1800, 1038), Image.LANCZOS)
imageMapVille     = ImageTk.PhotoImage(imageMapVillePIL)
imageMapGrottePIL = Image.open("temple.png").resize((1800, 1038), Image.LANCZOS)
imageMapGrotte    = ImageTk.PhotoImage(imageMapGrottePIL)

ca   = tk.Canvas(fenetre, width=1800, height=1038)
ca.place(x=0, y=0)
fond = ca.create_image(900, 519, image=imageMapVille)

img = Image.open("sprt.png")
sprites = []
for ligne in range(4):
    row = []
    for colonne in range(6):
        x1, y1 = colonne*64, ligne*64
        crop = img.crop((x1, y1, x1+64, y1+64)).resize((128,128), Image.NEAREST)
        fname = f"temp_{ligne}_{colonne}.png"
        crop.save(fname)
        row.append(tk.PhotoImage(file=fname))
    sprites.append(row)

indexImage = 0
ligneSprite = 0
perso = ca.create_image(600, 300, image=sprites[0][0])

imageGardienPIL    = Image.open("gardien.png").resize((80,78), Image.LANCZOS)
imageGardien       = ImageTk.PhotoImage(imageGardienPIL)
gardien            = ca.create_image(900, 250, image=imageGardien)

imageCommercantPIL = Image.open("commercant.png").resize((60,90), Image.LANCZOS)
imageCommercant    = ImageTk.PhotoImage(imageCommercantPIL)
commercant         = ca.create_image(350, 600, image=imageCommercant)

imagebriquetPIL  = Image.open("briquet.png").resize((55,51), Image.LANCZOS)
imageBriquet     = ImageTk.PhotoImage(imagebriquetPIL)

imageTnPIL       = Image.open("tn.png").resize((80,47), Image.LANCZOS)
imageTn          = ImageTk.PhotoImage(imageTnPIL)

imageEpeePIL     = Image.open("epee.png").resize((45,50), Image.LANCZOS)
imageEpee        = ImageTk.PhotoImage(imageEpeePIL)

imagePistoletPIL = Image.open("pistolet.png").resize((55,55), Image.LANCZOS)
imagePistolet    = ImageTk.PhotoImage(imagePistoletPIL)

imageCoffrePIL   = Image.open("coffre.png").resize((80,80), Image.LANCZOS)
imageCoffre      = ImageTk.PhotoImage(imageCoffrePIL)

imageDragonPIL   = Image.open("dragon.png").resize((120,120), Image.LANCZOS)
imageDragon      = ImageTk.PhotoImage(imageDragonPIL)

imageManettePIL   = Image.open("manette.png").resize((80,47), Image.LANCZOS)
imageManette      = ImageTk.PhotoImage(imageManettePIL)

def FaireBouleDeFeu():
    fb = Image.new("RGBA",(24,24),(0,0,0,0))
    d  = ImageDraw.Draw(fb)
    d.ellipse([2,2,22,22],  fill=(255,140,0))
    d.ellipse([5,5,19,19],  fill=(255,200,50))
    d.ellipse([8,8,16,16],  fill=(255,255,150))
    return ImageTk.PhotoImage(fb)

def FaireBalle():
    b = Image.new("RGBA",(14,14),(0,0,0,0))
    d = ImageDraw.Draw(b)
    d.ellipse([1,1,13,13], fill=(220,200,50))
    d.ellipse([3,3,11,11], fill=(255,240,120))
    return ImageTk.PhotoImage(b)


tn_sol      = None
coffre_obj  = None
dragon_obj  = None
manette_sol  = None


a_briquet     = False
a_tn          = False
a_epee        = False
a_pistolet    = False
a_manette      = False
boss_actif    = False
boss_vaincu   = False
dans_grotte   = False
dragon_vivant = False
dragon_parle  = False
entree_temple = False
coffre_ouvert = False
pistolet_donne= False
gardien_parle    = False
commercant_parle = False
manette_spawned   = False

BouleDeFeu = []
balles    = []

inv_label = tk.Label(fenetre, text="Inventaire : (vide)",
                     bg="black", fg="white",
                     font=("Courier",12), anchor="w", justify="left",
                     padx=6, pady=4)
inv_label.place(x=10, y=10)

def maj_inv():
    items = []
    if a_briquet:  items.append("Briquet")
    if a_tn:       items.append("TN")
    if a_epee:     items.append("Epee")
    if a_manette:   items.append("Manette PS5")
    if a_pistolet: items.append("Pistolet [N]")
    inv_label.config(text="Inventaire :\n"+("\n".join(f"- {i}" for i in items) if items else "(vide)"))

fenetre.after(500, lambda: messagebox.showinfo("Bienvenue",
    "Tu es enfin arrive dans cette ville dont on t'a tant parle.\n"
    "Rends-toi au temple pour trouver ce qu'il te faut !"))


def verif_contact_boss():
    global gardien, boss_actif, boss_vaincu
    if gardien is None or not boss_actif: return
    xP,yP = ca.coords(perso); xG,yG = ca.coords(gardien)
    if abs(xP-xG)<65 and abs(yP-yG)<65:
        if a_epee:
            ca.delete(gardien); gardien=None; boss_actif=False; boss_vaincu=True
            messagebox.showinfo("Gardien vaincu !",
                "Heureusement que j'avais une épée pour me defendre !\n"
                "Je devrais rentrer dans ce temple pour voir ce qu'il renferme.")
        else:
            messagebox.showinfo("Vous etes mort",
                "Vous auriez du recuperer l'epee avant d'affronter le Gardien !")
            fenetre.destroy()

def verif_approche_boss(x,y):
    if not boss_actif or gardien is None: return
    xG,yG = ca.coords(gardien)


TEMPLE_X,TEMPLE_Y,TEMPLE_RAYON = 900,200,80

def verif_entree_temple(x,y):
    global entree_temple, dans_grotte, coffre_obj, dragon_obj, dragon_vivant
    if not boss_vaincu or entree_temple: return
    if abs(x-TEMPLE_X)<TEMPLE_RAYON and abs(y-TEMPLE_Y)<TEMPLE_RAYON:
        entree_temple=True
        rep = messagebox.askyesno("Temple",
            "Vous vous appretez a entrer dans le temple.\nSouhaitez-vous vraiment y entrer ?")
        if not rep:
            messagebox.showinfo("Temple","Revenez quand vous serez pret.")
            entree_temple=False; return
        overlay = ca.create_rectangle(0,0,1800,1038,fill="black",outline="")
        fenetre.update(); fenetre.after(800)
        ca.itemconfig(fond, image=imageMapGrotte)
        ca.delete(overlay)
        if gardien is not None: ca.itemconfig(gardien, state='hidden')
        ca.coords(commercant,300,900); ca.itemconfig(commercant,state='normal')
        ca.coords(perso,900,880)
        dans_grotte=True; dragon_vivant=True
        coffre_obj = ca.create_image(900,185,image=imageCoffre)
        dragon_obj = ca.create_image(900,185,image=imageDragon)
        ca.itemconfig(dragon_obj,state='hidden')
        messagebox.showinfo("Grotte",
            "Tu entres dans les profondeurs du temple...\n"
            "Un tresor t'attend, mais quelque chose rode dans l'obscurite.")
        boucle_dragon()


def boucle_dragon():
    if not dans_grotte or not dragon_vivant or dragon_obj is None: return
    x,y = ca.coords(dragon_obj)
    dx,dy = random.choice([-15,-8,0,8,15]), random.choice([-15,-8,0,8,15])
    ca.coords(dragon_obj, max(150,min(1650,x+dx)), max(130,min(400,y+dy)))
    if random.random()<0.1: lancer_BouleDeFeu(*ca.coords(dragon_obj))
    verif_dragon_touche_perso()
    fenetre.after(500, boucle_dragon)

def lancer_BouleDeFeu(dx,dy):
    fb_tk = FaireBouleDeFeu()
    vx = random.randint(-3,3)*4
    fb = ca.create_image(dx,dy,image=fb_tk)
    t  = {'id':fb,'x':dx,'y':dy,'vx':vx,'vy':18,'img':fb_tk}
    BouleDeFeu.append(t); animer_BouleDeFeu(t)

def animer_BouleDeFeu(t):
    if t not in BouleDeFeu: return
    t['x']+=t['vx']; t['y']+=t['vy']
    ca.coords(t['id'],t['x'],t['y'])
    if t['y']>1060 or t['x']<0 or t['x']>1800:
        ca.delete(t['id'])
        if t in BouleDeFeu: BouleDeFeu.remove(t); return
    xP,yP = ca.coords(perso)
    if abs(t['x']-xP)<40 and abs(t['y']-yP)<40:
        ca.delete(t['id'])
        if t in BouleDeFeu: BouleDeFeu.remove(t)
        messagebox.showinfo("Brule vif !",
            "Une boule de feu t'a touche !\n"
            "Retourne voir le commercant, il doit avoir quelque chose pour t'aider.")
        ca.coords(perso,900,880); return
    fenetre.after(40, lambda: animer_BouleDeFeu(t))

def verif_dragon_touche_perso():
    if dragon_obj is None or not dragon_vivant: return
    xP,yP = ca.coords(perso); xD,yD = ca.coords(dragon_obj)
    if abs(xP-xD)<80 and abs(yP-yD)<80:
        messagebox.showinfo("Brule vif !",
            "Le dragon t'a attrape !\nRetourne voir le commercant pour obtenir de l'aide.")
        ca.coords(perso,900,880)

def verif_approche_coffre(x,y):
    global dragon_parle
    if coffre_obj is None or not dragon_vivant: return
    xC,yC = ca.coords(coffre_obj)
    if abs(x-xC)<200 and abs(y-yC)<200:
        if dragon_obj is not None: ca.itemconfig(dragon_obj,state='normal')
        if not dragon_parle:
            dragon_parle=True
            messagebox.showinfo("DRAGON !",
                "ROOOOAAR ! Un dragon surgit de l'obscurite !\n"
                "Ton epee ne suffit pas...\n"
                "Retourne voir le commercant, il doit avoir quelque chose pour t'aider !")

def verif_coffre(x,y):
    global coffre_ouvert, coffre_obj
    if coffre_obj is None or coffre_ouvert or dragon_vivant: return
    xC,yC = ca.coords(coffre_obj)
    if abs(x-xC)<70 and abs(y-yC)<70:
        coffre_ouvert=True; ca.delete(coffre_obj); coffre_obj=None
        messagebox.showinfo("Tresor !",
            "Le coffre s'ouvre dans un eclat de lumiere !\n"
            "Tu as trouve le tresor legendaire du temple !")
        afficher_credits()

def tuer_dragon():
    global dragon_vivant, dragon_obj
    if dragon_obj is None or not dragon_vivant: return
    for fb in BouleDeFeu[:]: ca.delete(fb['id'])
    BouleDeFeu.clear()
    ca.delete(dragon_obj); dragon_obj=None; dragon_vivant=False
    messagebox.showinfo("Dragon vaincu !",
        "Le dragon s'effondre dans un rugissement !\n"
        "La voie est libre... Approche-toi du tresor !")


def tirer_pistolet():
    if not a_pistolet: return
    x,y = ca.coords(perso)
    if ligneSprite==2:   vx,vy=12,0
    elif ligneSprite==1: vx,vy=-12,0
    elif ligneSprite==3: vx,vy=0,-12
    else:                vx,vy=0,12
    b_tk = FaireBalle()
    b    = ca.create_image(x,y,image=b_tk)
    t    = {'id':b,'x':x,'y':y,'vx':vx,'vy':vy,'img':b_tk}
    balles.append(t); animer_balle(t)

def animer_balle(t):
    if t not in balles: return
    t['x']+=t['vx']; t['y']+=t['vy']
    ca.coords(t['id'],t['x'],t['y'])
    if t['x']<0 or t['x']>1800 or t['y']<0 or t['y']>1038:
        ca.delete(t['id'])
        if t in balles: balles.remove(t); return
    if dragon_obj is not None and dragon_vivant:
        xD,yD = ca.coords(dragon_obj)
        if abs(t['x']-xD)<70 and abs(t['y']-yD)<70:
            ca.delete(t['id'])
            if t in balles: balles.remove(t)
            tuer_dragon(); return
    fenetre.after(30, lambda: animer_balle(t))


def parler_commercant():
    global commercant_parle,a_briquet,a_epee,tn_sol,a_pistolet,pistolet_donne,manette_sol,a_manette,manette_spawned,manette_img
    if commercant_parle: return
    commercant_parle=True

    if not a_briquet and tn_sol is None and not a_tn:
        messagebox.showinfo("Commercant","Tiens, prends ce briquet, j'en ai pas besoin.")
        a_briquet=True; maj_inv()
        messagebox.showinfo("Commercant",
            "J'ai aussi autre chose qui pourrait t'etre utile...\n"
            "Mes TN ont disparu quelque part dans la ville.\n"
            "Ramene-les moi et je te recompenserai !")
        tn_sol = ca.create_image(random.randint(1100,1650),random.randint(300,850),image=imageTn)

    elif a_tn and not a_epee:
        messagebox.showinfo("Commercant",
            "Mes TN ! Magnifique merci !\nTiens, prends cette epee. Bonne chance.")
        a_epee=True; maj_inv()

    elif a_epee and dragon_parle and not pistolet_donne:
        if not manette_spawned:
            messagebox.showinfo("Commercant",
                "Ah, le dragon... Je m'en doutais.\n"
                "J'ai un pistolet qui pourrait t'aider.\n"
                "Mais il me faut une manette de PS5 en echange.\n"
                "J'en ai vu une trainer dans la grotte, bonne chance !")
           
            manette_sol = ca.create_image(random.randint(300,700),random.randint(550,820),image=imageManette)
            manette_spawned=True; commercant_parle=False
        elif a_manette:
            messagebox.showinfo("Commercant",
                "La Manette ! Parfait.\n"
                "Tiens, prends ce pistolet. Appuie sur N pour tirer.\n"
                "Bonne chance contre le dragon !")
            a_pistolet=True; pistolet_donne=True; maj_inv()
        else:
            messagebox.showinfo("Commercant","Ramene-moi la Manette d'abord !")
            commercant_parle=False

    elif a_pistolet:
        messagebox.showinfo("Commercant","Bonne chance contre le dragon, t'en auras besoin !")
    else:
        commercant_parle=False

def verif_manette(x,y):
    global manette_sol,a_manette
    if manette_sol is None: return
    xPi,yPi = ca.coords(manette_sol)
    if abs(x-xPi)<65 and abs(y-yPi)<65:
        ca.delete(manette_sol); manette_sol=None; a_manette=True; maj_inv()
        messagebox.showinfo("Manette de PS5 !",
            "Tu as ramasse la Manette de PS5 !\nRetourne voir le commercant.")


def afficher_credits():
    rep = messagebox.askokcancel(
        "FIN DU JEU",
        " GG ! Tu as fini le jeu !\n\n"
        "Crédits :\n"
        "Bilal Manaa\n\n"
        "Cliquer sur OK pour quitter."
    )
    if rep:
        fenetre.destroy()

def parler_gardien():
    global gardien_parle,boss_actif,a_briquet
    if boss_actif or gardien_parle: return
    gardien_parle=True
    if not a_briquet:
        messagebox.showinfo("Gardien du Temple",
            "Je ne te laisserai pas entrer sans un briquet.\n"
            "Va voir le commercant, il devrait en avoir un.")
    else:
        messagebox.showinfo("Gardien du Temple",
            "Tu as le briquet... Tu n'aurais pas du me faire confiance.")
        a_briquet=False; maj_inv(); boss_actif=True
        if not a_epee:
            messagebox.showinfo("Vous etes morts",
                "Vous auriez du recuperer l'epee avant d'affronter le Gardien !")
            fenetre.destroy()

def verif_tn(x,y):
    global tn_sol,a_tn
    if tn_sol is None: return
    xT,yT = ca.coords(tn_sol)
    if abs(x-xT)<65 and abs(y-yT)<65:
        ca.delete(tn_sol); tn_sol=None; a_tn=True; maj_inv()
        messagebox.showinfo("TN !","Tu as ramasse les TN !\nRetourne voir le commercant.")

def verif_eau(x,y):
    if x<130 or x>1670 or y<100 or y>950:
        messagebox.showinfo("Noyade",
            "Vous ne savez pas nager...\n"
            "Vous auriez du aller plus souvent a la piscine.\n\nVous etes mort.")
        fenetre.destroy()

def verif_eloignement(x,y):
    global gardien_parle,commercant_parle
    if gardien is not None:
        xG,yG = ca.coords(gardien)
        if abs(x-xG)>130: gardien_parle=False
    xC,yC = ca.coords(commercant)
    if abs(x-xC)>130: commercant_parle=False


def clavier(event):
    global perso,indexImage,ligneSprite
    x,y = ca.coords(perso)

    if event.char in ('n','N'):
        tirer_pistolet(); return
    if event.keysym=='Escape':
        maj_inv(); return

    indexImage=(indexImage+1)%6

    if event.char=='d':   ligneSprite=2; x+=5
    elif event.char=='q': ligneSprite=1; x-=5
    elif event.char=='z': ligneSprite=3; y-=5
    elif event.char=='s': ligneSprite=0; y+=5
    else: return

    x=max(45,min(1755,x)); y=max(45,min(993,y))
    ca.delete(perso)
    perso=ca.create_image(x,y,image=sprites[ligneSprite][indexImage])

    if not dans_grotte:
        verif_eau(x,y)
        verif_tn(x,y)
        verif_eloignement(x,y)
        if boss_actif:
            verif_approche_boss(x,y)
            verif_contact_boss()
        if gardien is not None and not boss_actif:
            xG,yG = ca.coords(gardien)
            if abs(x-xG)<65 and abs(y-yG)<65: parler_gardien()
        xC,yC = ca.coords(commercant)
        if abs(x-xC)<40 and abs(y-yC)<40: parler_commercant()
        verif_entree_temple(x,y)
    else:
        verif_approche_coffre(x,y)
        verif_coffre(x,y)
        verif_manette(x,y)
        xC,yC = ca.coords(commercant)
        if abs(x-xC)<40 and abs(y-yC)<40: parler_commercant()

fenetre.bind("<Any-KeyPress>", clavier)
fenetre.mainloop()

for ligne in range(4):
    for colonne in range(6):
        fname=f"temp_{ligne}_{colonne}.png"
        if os.path.exists(fname): os.remove(fname)
