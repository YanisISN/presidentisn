import random
import os
import pygame as py
import time
from operator import attrgetter
from constantes import *
import pickle

py.init()
root = os.getcwd() #racine

fenetre = py.display.set_mode((880,700))
py.display.set_caption("Président")
icone = py.image.load(image_icone)
py.display.set_icon(icone)

fond= py.image.load(fond)




### FONCTIONS SAMUEL ###


#CLASS CARTES AVEC IMAGE, VALEUR, COORDONEES.
class Cartes:
    def __init__(self, img_carte, valeur,x,y):
        self.image = img_carte
        self.rect = self.image.get_rect()
        self.valeur = valeur
        self.rect.x = x
        self.rect.y = y
        
    def poser_carte(self, defausse, joueur): #on pose la carte dans la defausse
        self.rect.x = 400
        self.rect.y = 250
        defausse.append(self)
        joueur.remove(self) 
        
    def proposer_carte(self, joueur,before, compter, nb_max, y): #on  met la carte dans before

        if len(before)+1<=nb_max: 
            if compter>= 1:#si la before estt déjà rempli
                if before[-1].valeur == self.valeur: #on regarde si la valeur correpond bien a celle posé sur la before
                    self.rect.y = y
                    before.append(self)
                    joueur.remove(self)
            else: #si elle est vide on ajoute
                self.rect.y = y
                before.append(self)
                joueur.remove(self)
### COUPER UNE IMAGE OU AFFICHER DU TEXTES
def afficher_text(text, taille_police, x,y):
    police = py.font.Font(str(root)+'\\fonts\\BradBunR.ttf', taille_police)
    texte = police.render(text, True, WHITE)
    fenetre.blit(texte, [x,y])
    
### FONCTION AJOUTER DE BEFORE A LA DEFAUSSE    
   
def ajouter_prop_carte(defausse, before):
    x = 400

    len_before = len(before)
    for el in before:
        el.rect.x = x
        el.rect.y = 250
        defausse.append(el)
        x+=35
    
    before[:] = []
    return len_before
    
### NOMBRES DE CARTES POSSIBLES A JOUEUR POUR CHAQUE JOUEUR ###
def carte_possible(cartes, defausse, nb_joueur):
    cartes_possibles = 0
    liste_cartes = []

    if defausse: #pour IA et Joueur quand la defausse est remplie ducoup

        for el in cartes:
            if defausse[-1].valeur == 15:
                break
            elif el.valeur >= defausse[-1].valeur:
                cartes_possibles+=1
                liste_cartes.append(el)
            else: pass
    else: #pour IA... au début de partie quand la defausse est vide pour avoir toutes les cartes dans sa main
        for el in cartes:
            liste_cartes.append(el)
        
    return cartes_possibles, liste_cartes

def cartes_double(cartes_j2, defausse): #en ce qu'il s'agit des paires....
    copie = list(cartes_j2)
    structure = []
    val = []
    for objs in copie: #on met toutes les VALEUR es elements de cartes_j2 dans val
        val.append(objs.valeur)
    verif = []
    for el in copie: #pour tous les objets present dans cartes_j2
        old = el #on recupere l'ancienne carte
        valeur = el.valeur #la valeur est celle de la carte

        val.remove(el.valeur) #on la supprime de val si il y en a deux ils n'aura donc pas de probleme
        copie.remove(old) #on supprime la carte, pour pouvoir travailler sur le deuxieme element de la paire

        liste = []
       
        if valeur not in verif: #on veut que des paires, si la carte, c'est qu'on la déjà étudié alors on passe...
            if valeur in val:
                for cartes in copie: #pour toutes les cartes dans les cartes du joueur 2
                    if cartes.valeur == valeur: #si il existe une carte qui correspond a cette valeur alors qu'on en a supprimé une
                        liste.append(cartes) #on l'ajoute la DEUXIEME carte a la liste
                        verif.append(cartes.valeur) #on ajoute cette valeur a la liste, comme ca au prochain tour, si le joueur a encore des cartes de cete vvaleur on passe..
                        break
                    else:
                        pass
                liste.append(old) #on ajoute la PREMIERE carte supprimé du paquet a la liste 
                structure.append(liste)

            else:
                pass
    carte_possible_p = 0         
    if defausse:
        for groupes in structure:
            for element in groupes:
                if element.valeur >= defausse[-1].valeur:
                    carte_possible_p += 1
                    break
                else: pass
                
            
    return structure, carte_possible_p 





#Fonction qui intervient après chaque manche
def again():
    for ev in py.event.get():
        if ev.type == py.QUIT:
            quit()
            exit()
        if ev.type == py.KEYDOWN:
            return ev.key
        else:
            pass
    return None
        
def parti_end(gagnant, perdant):
    fenetre.blit(fond, (0,0))
    afficher_text("Le gagnant est "+str(gagnant)+" qui est maintenant President", 50,0,100)
    afficher_text("Le perdant est "+str(perdant)+" qui est maintenant Villageois", 50,0,200)
    afficher_text(". Tu peux rejouer en appuyant sur espace...", 30,200,400)
    afficher_text(". Tu peux modifier ton pseudo en appuyant sur F1...", 30,200,500)
    afficher_text(". Tu peux quitter en appuyant sur Echap...",30,200,600)
    
    py.display.flip()
    time.sleep(1)
    ok = False
    while ok == False:
        for ev in py.event.get():
            if ev.type == py.QUIT:
                py.quit()
                exit()
            if ev.type == py.KEYDOWN:
                if ev.key == py.K_SPACE:
                    continuer = 1
                    ok = True
                if ev.key == py.K_ESCAPE:
                    py.quit()
                    exit()
                if ev.key == py.K_F1:
                    continuer = 2
                    ok = True
    
    return continuer
    
def gagne_auto(joueur, num_joueur, joueur_adv, num_joueur_adv, defausse, tg, n_tour, mode_actuel): #SAMUEL ET ARTHUR

    game_over = 0

    if mode_actuel == 1:
                    
        cartes_possibles1 = carte_possible(joueur, defausse, num_joueur)
        cartes_possibles2 = carte_possible(joueur_adv, defausse, num_joueur_adv)
         

        if (len(defausse) >= 4 and defausse[-1].valeur == defausse[-2].valeur== defausse[-3].valeur == defausse[-4].valeur):    
            tg = False
            n_tour-=1
            game_over = 1
        else:
            if tg == False: #si il n'y a pas de tg, ni de carré magique 
                if cartes_possibles1[0] == 0: #on vérifie que le joueur qui doit jouer a bien des cartes
                    n_tour-=1
                    game_over = 1
            else: #sinon... si il y a TG
                nb_carte_p = 0
                for cartes in joueur: #on verifie qu'il peut jouer des cartes , lors du tg
                    if cartes.valeur == defausse[-1].valeur:
                        nb_carte_p+=1

                if nb_carte_p == 0: #si il ne peux pas pas jouer
                    if cartes_possibles2[0] != 0: #on vérifie que l'autre joueur puisse eventuellement jouer au prochain coup
                        tg = False #si oui on enelve le tg, 
                        n_tour-=1 #et le joueur adverse rejoue 
                    else: #sinon, c'est a nous de jouer, mais sans le tg, car le joueur adverse n'a pas moyen de répondre.
                        tg= False
                else: pass
                
    elif mode_actuel == 2: #développé par Arthur: vérifier après qu'un des joueurs est posé sa carte si l'autre peut jouer, cette fonction anticipe si l'autre joueur peut jouer... sinon game_over)
        cartes_a_jouer, nb_carte_possible = cartes_double(joueur, defausse)
        if nb_carte_possible == 0 or defausse[-1].valeur == 15:
            n_tour-=1
            game_over=1

    elif mode_actuel==3: #développé par Arthur
        l_cartes_possibles, peut_jouer = cartes_triples(joueur, defausse)
        
        if peut_jouer == False or defausse[-1].valeur == 15:
            n_tour-=1
            game_over = 1
    elif mode_actuel == 4:
        game_over = 1

    return n_tour, tg, game_over

#### FIN FONCTIONS SAMUEL


### FONCTIONS ARTHUR #######################

 #LE SYSTEME DE FIN DE PARTIE VILLAGEOIS-PRESIDENT DOIT ÊTRE FINI PAR ARTHUR
def echanger_carte(carte_perdant, carte_gagnant):
    
    valeur_test_1 = 0
    valeur_test_2 = 20
    
    for carte in carte_perdant:
        valeur = carte.valeur
        valeur = carte.valeur
        if valeur > valeur_test_1:
            valeur_test_1 = valeur
            carte_max = carte
        
    for carte in carte_gagnant:
        valeur = carte.valeur
        if valeur < valeur_test_2:
            valeur_test_2 = valeur
            carte_min = carte
     
    carte_perdant.remove(carte_max)
    carte_gagnant.remove(carte_min)
    
    carte_perdant.append(carte_min)
    carte_gagnant.append(carte_max)
    
    carte_renvoi_p = trie(carte_perdant)
    carte_renvoi_g = trie(carte_gagnant)
    
    return carte_renvoi_p, carte_renvoi_g
        
 #FONCTIONS IA TRIPLES-QUADRUPLES

def cartes_triples(main, defausse):
    if defausse:
        valeur_derniere = defausse[-1].valeur
    else:
        valeur_derniere = 0 

    l_valeur = []
    valeur_carte_possible = 20
    peut_jouer = False

    for carte in main: 
        l_valeur.append(carte.valeur)

    for valeur in l_valeur:
        if valeur >= valeur_derniere:
            nbre_carte_semblable = l_valeur.count(valeur)

            if nbre_carte_semblable >= 3:

                if valeur <= valeur_carte_possible:
                    valeur_carte_possible = valeur

                peut_jouer = True

    
    valeur_test = 0
    l_cartes_possibles = []

    if peut_jouer == True:
        for carte in main:
            if carte.valeur == valeur_carte_possible:
                l_cartes_possibles.append(carte)
        
        return l_cartes_possibles, peut_jouer

    else:
        return l_cartes_possibles, peut_jouer

def cartes_quadruple(main,defausse):
    if defausse:
        valeur_derniere = defausse[-1].valeur
    else:
        valeur_derniere = 0 

    l_valeur = []
    valeur_carte_possible = 20
    peut_jouer = False

    for carte in main: 
        l_valeur.append(carte.valeur)

    for valeur in l_valeur:

        if valeur >= valeur_derniere:

            nbre_carte_semblable = l_valeur.count(valeur)

            if nbre_carte_semblable == 4:

                if valeur <= valeur_carte_possible:
                    valeur_carte_possible = valeur

                peut_jouer = True

    
    valeur_test = 0
    l_cartes_possibles = []

    if peut_jouer == True:
        for carte in main:
            if carte.valeur == valeur_carte_possible:
                l_cartes_possibles.append(carte)
        
        return l_cartes_possibles, peut_jouer
    else:
        return l_cartes_possibles, peut_jouer





#TRIE, REMPLIR, DISTRIBUER

def trie(liste): #doit être perfectionné par arthur
    M = []    
    for el in list(liste):
        if el.valeur == 14 or el.valeur == 15:
            M.append(el)
            liste.remove(el)
        else:
            pass
    
    #On trie par rapport à la valeur pour l'objet        
    M1 = sorted(M, key=attrgetter("valeur"))
    liste1 = sorted(liste, key=attrgetter("valeur"))
    liste1.extend(M1)

    return liste1


def creer_paquet():
    signe = ["d", "h", "c", "s"]
    valeur = [3,4,5,6,7,8,9,10,11,12,13,14,15]
    paquet = []
    for i in signe:
        for j in valeur:
            paquet.append(str(j) + i) #le paquet fera des valeur un str et le i est déjà str pensez a convertir en (int)

    return paquet

def distribution(paquet, joueur1, joueur2):
    compter = 0
    for i in range(0,52):
        compter+=1
        carteT = random.choice(paquet)
        valeur = 0
        recup_int = carteT
        for el in carteT:
            try:
                el = int(el)
            except:
                recup_int = recup_int.replace(el, "")
        valeur = int(recup_int)
        img_carte = carteT+".jpg"
        img_carte = py.image.load(str(root)+"//data//cartes//"+img_carte)
        if compter==1:
            joueur1.append(Cartes(img_carte, valeur, 0,0))
        elif compter==2:
            joueur2.append(Cartes(img_carte, valeur, 0,0))
            compter=0
        paquet.remove(carteT)

    joueur1 = trie(joueur1)
    joueur2 = trie(joueur2)

    return joueur1, joueur2

def getScorePseudo (valeur):

    valeur = valeur.rstrip("\n")
    score = ""
    
    for chara in valeur:
        try:
            if chara == "0":
                score = score + chara
            elif int(chara):
                score = score + chara
            else:
                pass
        except ValueError:
            pass
       
    score = int(score)
    return score
    
    
def checkPseudo (varPseudo):
    
    scoresPris = False
    
    with open(root+"\\data\\scores.txt", "r") as fichier:

        for lignes in fichier:

            ligne = lignes.rstrip("\n")
            pseudoTest = ""

            for chara in ligne:
                try:
                    if chara == "0":
                        pass
                    elif int(chara):
                        pass
                    else:
                        pass
                except ValueError:
                    pseudoTest = pseudoTest + chara

            if (pseudoTest == varPseudo):
                scoresPris = True
                score_entier = ligne
                
                score = getScorePseudo(score_entier)
                returnPseudo = pseudoTest
            else:
                pass
      

    if scoresPris == False:

        returnPseudo = varPseudo
        score = 0
        fichier = open(root+"\\data\\scores.txt", "a")
        fichier.write(returnPseudo+ str(score)+"\n")
        fichier.close()
        
       
    returnPseudo = str(returnPseudo)  
    
    
    return returnPseudo, score

def refreshFichier(oldPseudo, newPseudo):

    s = open(root+"\\data\\scores.txt").read()
    s = s.replace(oldPseudo, newPseudo)
    f = open(root+"\\data\\scores.txt", 'w')
    f.write(s)
    f.close()

######################FIN FONCTIONS ARTHUR #######################################



#FONCTIONS YANIS

#yanis doit developper une fonction qui trie les scores du meilleur au pire 
#pour faire un classement dans son menu
def trie_liste_joueur():
    pseudo_score = {}

    with open(root+"\\data\\scores.txt", "r") as fichier_score:
        for lignes in fichier_score:
            score = ""
            pseudo =""
            for carac in lignes:
                try: #on test si c'est un chiffre en essayant de convertir le caractere en int() (chiffre)
                    if carac == "0":
                        score = score+"0"
                    elif int(carac):
                        carac = str(carac)
                        score = score+carac
                except ValueError: #si il y a une erreur c'est que c'est un str()  (lettre)
                    pseudo = pseudo + carac
            pseudo = pseudo.rstrip('\n') #on retirer le caractere \n du pseudo
    
            pseudo_score[pseudo] = score #on ajoute le pseudo et le score au dictionnaire
    pseudo_score = pseudo_score.items() #on converttir le tuple [('',''), ('','')]
    pseudo_trie = sorted(pseudo_score, key=lambda el: el[1], reverse=True)#fonction pour trier en fonction du 2 eme element des listes.
    return pseudo_trie #on retourne le tuple trié.