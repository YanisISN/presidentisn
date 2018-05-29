import os
root = os.getcwd()#"\\\MAL-FILER\\USER$\\gaudemers.MALHERBE\\Desktop\\Jeu_Mixe" #racine

os.chdir(root)

from constantes import * 
from fonctions import *
import pygame as py
import time

#Init variables
score_bot = 0
pseudo_bot = "bot"

n_tour = 0
continuer = 1
img_dos = py.image.load(str(root)+"//data//cartes//dos.png")


### FONCTIONS QUI CHARGES  OU RECHARGES LES VARIABLES DU JEUX (d'où la necessité d'être dans main.py car dans les fichier import, impossible 
### de modifier des variables, car ces derniers crée une copie des variables. On pourrait tout passer en arguement, faire les traitemetns, et tout ressortir en return, mais c'est plus simple de faire un global


######################################################################

def load():
    global continuer, mode_actuel, cartes_j1, cartes_j2, pos_x, defausse, before, tg, n_tour, continuer, msgAdmin, cartes_possibles1, cartes_possibles2, timer, paquet, clock, echange
    

    paquet = creer_paquet()
    
    echange = False

    clock = py.time.Clock() 

    cartes_j1 = []
    cartes_j2 = []
    pos_x = []
    for x in range(0,832,32):
        pos_x.append(x)
    defausse = []
    before = []
    mode_actuel = 0
    tg = False

    
    msgAdmin = ""
    cartes_possibles1 = -1
    cartes_possibles2 = -1
    timer =0
    
    cartes_j1, cartes_j2 = distribution(paquet, cartes_j1, cartes_j2)



def refreshJeu(pseudo, pseudo_bot, score, score_bot, msgAdmin):
    ### AFFICHAGE DU JEU ###
    global color_skip1

    afficher_text(msgAdmin, 60, 550,300)


    afficher_text(str(pseudo), 40, 10,560)
    afficher_text(str(pseudo_bot), 40,10,100)

    afficher_text("Score : "+str(score), 30,780,560)
    afficher_text("Score : "+str(score_bot), 30,780,100)

    if n_tour%2==0:
        afficher_text("AU TOUR DE",60,50,235)
        afficher_text(str(pseudo), 80, 50,280)
        if n_tour != 0 and color_skip1 != 0:
            skip1 = py.draw.rect(fenetre, color_skip1, py.Rect(750,400,150,80), 0)
            afficher_text("Passer", 40,772,415)
    else:
        afficher_text("AU TOUR DE",60,50,235)
        afficher_text(str(pseudo_bot), 80, 50, 280)


    #ON AFFICHE TOUT LE JEU     

    for obj in defausse:
        fenetre.blit(obj.image, (obj.rect.x, obj.rect.y))#la carte choisi
    prop_x = 400
    for obj in before:
        fenetre.blit(obj.image, (prop_x, obj.rect.y))
        prop_x += 50


    for obj, x in zip (cartes_j1,pos_x): #le jeu du joueur
        fenetre.blit(obj.image, (x,obj.rect.y))
    for obj2, x in zip (cartes_j2, pos_x): #le jeu du joueur 2
        fenetre.blit(img_dos, (x,0))
    py.display.flip()


    
def game_over(defausse, n_tour, gagnant): #a chaque fin de manche
    global score, score_bot, pseudo, pseudo_bot, msgAdmin, color_skip1
    msgAdmin = ""
    if gagnant == str(pseudo):
        score+=1
    elif gagnant == str(pseudo_bot):
        score_bot+=1
    for obj in cartes_j1:
        obj.rect.y = 605

    afficher_text(gagnant,70,600,250)
    afficher_text("GAGNE LA MANCHE",50,590,315)
    afficher_text("APPUYEZ SUR UNE TOUCHE POUR CONTINUER...",30,450,400)
    color_skip1 = 0

    refreshJeu(pseudo, pseudo_bot, score, score_bot, msgAdmin)

    time.sleep(1)

    while again() == None:
        clock.tick()

def parti_fini(gagnant, perdant): #traitement quand la partie est terminée définitivement
    global defausse, pseudo_bot,n_tour, tg,old_score, pseudo, score, echange
    if defausse[-1].valeur == 15:
        fenetre.fill((BLACK))
        afficher_text("VOUS VENEZ DE FINIR",80,50,280)
        afficher_text("AVEC LA CARTE 2, C'EST DONC",70,60,350)
        afficher_text("PERDU POUR VOUS "+str(gagnant),70,100,450)
        ancien_gagnant = gagnant
        ancien_perdant = perdant
        perdant = ancien_gagnant
        gagnant = ancien_perdant
        py.display.flip()
        time.sleep(2)
        continuer = parti_end(gagnant, perdant) #la partie est fini et invite a recommencer
    else:
        n_tour-=1
        continuer = parti_end(gagnant, perdant)
    change_name = False
    if continuer == 1:
        pass
    elif continuer == 2:
        pseudoInput = menu()
        pseudo, score = checkPseudo(pseudoInput)
        old_score = score #on initialise le score du départ pour le remplacer apres
        change_name = True
    load()
    
    if change_name == False:
        echange = True
 
    if gagnant == pseudo_bot:
        n_tour = 0
    else:
        n_tour = 1
        
    return echange,gagnant,perdant

######################################################################



### TRAVAIL YANIS MENU POUR ENTRER PSEUDO ... ###    
def menu():
    pseudo = 0
    pseudo_trie = trie_liste_joueur()

    fond = py.image.load(str(root)+"\\data\\menu.jpg").convert()
    fenetre.blit(fond, (0,0))
    def print_lettre(lettre,x):
        font = py.font.Font(None,100)
        text = font.render(lettre,1,(255,255,255))
        fenetre.blit(text, (x,300))
    
    def recup_nom(liste):
        pseudo= ""
        for lettre in liste:
            pseudo = pseudo+lettre
        return pseudo
    
    
    #BOUCLE INFINIE
    continuer = 1
    
    liste = []
    x=110
    while continuer:
        
        fenetre.blit(fond, (0,0))
        
        for event in py.event.get():
            if event.type == py.QUIT:
                continuer = 0
            if event.type == py.KEYDOWN:
                if event.key == py.K_BACKSPACE:
                    if liste:
                        del liste[-1]

                else:    
                    lettre = event.unicode
                    if lettre != "" and str(lettre):
                        lettre.lower()
                        liste.append(lettre)
                
            elif event.type == py.MOUSEBUTTONDOWN:
                event = py.mouse.get_pos()
                perso_x = event[0]
                perso_y = event[1]
                if  841 > perso_x > 741 and 595 < perso_y <667 :
                    pseudo = recup_nom(liste)
                    continuer = 0
                elif 50<perso_x<323 and 595<perso_y<667:
                    image = 1
                    didac = py.image.load(str(root)+"\\data\\didac.png").convert()
                    while image:

                        fenetre.blit(didac, (0,0)) #il faudra mettre l'image du dictatiel
                        for ev in py.event.get():
                            if ev.type == py.QUIT:
                                image = 0
                                continuer = 0
                                exit()
                            if ev.type == py.MOUSEBUTTONDOWN:
                                event = py.mouse.get_pos()
                                perso_x = event[0]
                                perso_y = event[1]
                                if  785 < perso_x < 865 and 20 < perso_y <90:
                                    image=0.
                        py.display.flip()
                       
        x=170
        for el in liste:
            x+=45
            print_lettre(el,x)
        
        nbr_j=0
        for el in pseudo_trie:
            nbr_j+=1
        y=0

        for j in range(0,nbr_j):#commence à 0 et doit parcourir 8 élements, 0,1,2,3,4,5,6,7 = 8 element
            afficher_text(pseudo_trie[j][1], 20,0,y)
            afficher_text(pseudo_trie[j][0], 20,20,y)
            
            y+=20
        py.display.flip()
    return pseudo
    




### FONCTION PRINCIPALE DU JEU ###
def main():
    global continuer, old_score, pseudo, score,mode_actuel, color_skip1, cartes_j1, cartes_j2, pos_x, defausse, before, tg, n_tour, continuer, msgAdmin, cartes_possibles1, cartes_possibles2, timer, paquet, clock, pseudo, echange
    
    while continuer:
        
        fenetre.blit(fond, (0,0))
        pos_souris = py.mouse.get_pos()
        

        #BOUTON ECHANGE CARTE: Arthur
        if echange == True:

            b_echange = py.draw.rect(fenetre, WHITE , py.Rect(350,250,300,100), 0)
            police = py.font.Font(str(root)+'\\fonts\\BradBunR.ttf', 40)
            texte = police.render("Echanger les cartes", True, BLACK)
            fenetre.blit(texte, [360,280])

            if 250 <= pos_souris[1] <= 350:
                if 350 <= pos_souris[0] <= 650:
                    for event_mouse1 in py.event.get():
                        if event_mouse1.type == py.MOUSEBUTTONDOWN:
                            if gagnant == pseudo_bot:
                                carte_gagnant = cartes_j2
                                carte_perdant = cartes_j1
                                cartes_j1, cartes_j2 = echanger_carte(carte_perdant,carte_gagnant)
                            else:
                                carte_gagnant = cartes_j1
                                carte_perdant = cartes_j2
                                cartes_j2, cartes_j1 = echanger_carte(carte_perdant,carte_gagnant)
                             
                            echange = False
                            
        #METTRE EN EVIDENCE UNE CARTE
        for obj in cartes_j1:
            obj.rect.y = 605
        if pos_souris[1] > 605:
            k = int(pos_souris[0]/32)
            if k <= len(cartes_j1)+1 and len(cartes_j1) != 0:
                if k == len(cartes_j1):
                    k-=1
                elif k == len(cartes_j1)+1:
                    k-=2
                cartes_j1[k].rect.y = 585
            else:pass

        #BOUTON POUR PASSER
        color_skip1 = VERT

        if mode_actuel == 1:
            carte_dispo2 = carte_possible(cartes_j2, defausse,2)
            carte_dispo2 = carte_dispo2[0]
        elif mode_actuel == 2:
            variable_nul, carte_dispo2 = cartes_double(cartes_j2, defausse)
        elif mode_actuel == 3:
            variable_nul, carte_dispo2 = cartes_triples(cartes_j2, defausse)
            if carte_dispo2 == False:
                carte_dispo2 = 0
        else:
            carte_dispo2 = 0

        if 400 <= pos_souris[1] <= 480 and n_tour != 0 and carte_dispo2 != 0 and n_tour%2 == 0:
            if 750 <= pos_souris[0] <= 900:
                color_skip1 = BLACK
                for even_mouse in py.event.get():
                    if even_mouse.type == py.MOUSEBUTTONDOWN:
                        n_tour+=1
                        msgAdmin = ""
                        carte_transfert = before
                        for el in carte_transfert:
                            el.rect.y = 605
                            cartes_j1.append(el)
                        before = []
                            
                        cartes_j1 = trie(cartes_j1)#pour mettre sa paire, ou son triple dans la defausse

        for ev in py.event.get():

            if ev.type == py.QUIT:
                #on actualise le pseudo avec le score
                newPseudo = pseudo + str(score)
                oldpseudo = pseudo + str(old_score)
                #Et on actualise le fichier pour qu'il enregistre le nouveau à la place de l'ancien
                refreshFichier(oldpseudo, newPseudo) 
                
                continuer = 0
                
             ### JOUEUR 1 BY SAMUEL ###

            if n_tour % 2 == 0 and echange == False:
                    #si le joueur souhaite mettre plus d'une carte les bouton s'activent
                if ev.type == py.KEYDOWN:
                    if ev.key == py.K_BACKSPACE: #pour supprimer une carte
                        if before:
                            carte_transfert = before[-1]
                            carte_transfert.rect.y = 605
                            before.remove(before[-1])
                            cartes_j1.append(carte_transfert)
                            cartes_j1 = trie(cartes_j1)#pour mettre sa paire, ou son triple dans la defausse
                    if ev.key == py.K_SPACE:
                        if before:
                            if mode_actuel == len(before) or not defausse or len(before)== 4:
                                
                                if before[-1].valeur == 15 and len(cartes_j1) != 0 or len(before) == 4: #si la carte posé est le 2 ou que le mec met un quadruple
                                    mode_actuel= ajouter_prop_carte(defausse, before)
                               
                                    game_over(defausse, n_tour, pseudo)
                                    mode_actuel = 0
                                    defausse = []
                                    n_tour = 0
                                else:
                                    mode_actuel= ajouter_prop_carte(defausse, before)
                                    n_tour +=1
                            else: pass
                if ev.type == py.MOUSEBUTTONDOWN:
                        pos_souris = py.mouse.get_pos()

                        if pos_souris[1] > 560: #si la position de la souris correpond a la position des cartes
                            k = int(pos_souris[0]/32) #on récuperer l'entier correspondant a la position de la carte dans la liste (une carte = 32 pixels)
                            

                            count = len(cartes_j1)
                            compter = len(before)
                            if compter < 4:
                                if k <= count or k == count+1:
                                    if k == count:
                                        k = k-1
                                    if k == count+1:
                                        k = k-2
                                    if not defausse: #premier tour
                                        cartes_j1[k].proposer_carte(cartes_j1,before, compter,4,535) #la paire ou le triple
                                    elif mode_actuel >= 2:

                                        if  cartes_j1[k].valeur < defausse[-1].valeur: #MAUVAIS COUP
                                            msgAdmin = "Mauvais coup !"
                                        else:
                                            cartes_j1[k].proposer_carte(cartes_j1,before, compter,4,535)
                                            msgAdmin = ""
                                    else:
                                        if tg == False:

                                            if cartes_j1[k].valeur == 15: #si la carte posé est le 2
                                                if len(cartes_j1) <= 1:#si c'est pour la fin de la partie
                                                    cartes_j1[k].poser_carte(defausse, cartes_j1)
                                                    n_tour+=1
                                                    msgAdmin = ""
                                                else:
                                                    cartes_j1[k].poser_carte(defausse, cartes_j1)
                                                    game_over(defausse, n_tour,pseudo)
                                                    mode_actuel = 0
                                                    defausse = []
                                                    n_tour = 0
                                              
                                                    msgAdmin = ""
                                            elif cartes_j1[k].valeur < defausse[-1].valeur: #MAUVAIS COUP
                                                msgAdmin = "Mauvais coup !"

                                            else:
                                                if defausse[-1].valeur == cartes_j1[k].valeur:
                                                    tg = True
                                                cartes_j1[k].poser_carte(defausse, cartes_j1)
                                                n_tour += 1
                                                msgAdmin = ""

                                        elif tg == True:
                                            if defausse[-1].valeur != cartes_j1[k].valeur:
                                                msgAdmin = "Mauvais coup !"
                                            else:
                                                cartes_j1[k].poser_carte(defausse, cartes_j1)
                                                n_tour += 1
                                          
                                                msgAdmin = ""




        
       ### JOUEUR 2 - BOT - BY ARTHUR & SAMUEL ### 
        if n_tour % 2 != 0 and echange == False:
            if timer<25: #ON LAISSE UN TEMPS 
                timer+=1

            else:

                
                #FONCTIONS D INTELLIGENCE
                if not defausse: #samuel + Arthur


                    cartes_a_jouer, nb_carte_possible = cartes_double(cartes_j2, defausse) #on check les doubles possibles
                    if len(cartes_a_jouer) == 0: #si pas de double alors on met une simple
                        mode = 0
                    else:
                        mode = 1

                    l_carte_possible, peut_jouer = cartes_triples(cartes_j2, defausse)
                    if peut_jouer == True:
                        mode = 2

                    l_carte_possible, peut_jouer = cartes_quadruple(cartes_j2, defausse)
                    if peut_jouer == True:
                        mode = 3

                    
                    
                    if mode==0: #~mode simple
                        cartes = carte_possible(cartes_j2, defausse,2) #on regarde les cartes possible a joueur
                        cartes_a_jouer = cartes[1] #on met dans uen liste

                        carte_prise = random.choice(cartes_a_jouer)
                        before.append(carte_prise)
                        cartes_j2.remove(carte_prise)
                    elif mode == 1: #mode double
                        cartes_a_jouer, nb_carte_possible = cartes_double(cartes_j2, defausse)
                        carte_prise1 = cartes_a_jouer[0][0] #la carte 1, est la carte dans la liste k, et le numer 0
                        carte_prise2 = cartes_a_jouer[0][1] #la carte 2,e st al carte dans la liste k , et le numero 1
                        before.append(carte_prise1)
                        before.append(carte_prise2)
                        cartes_j2.remove(carte_prise1)
                        cartes_j2.remove(carte_prise2)
                    elif mode == 2: #mode triple
                        l_carte_possible, peut_jouer = cartes_triples(cartes_j2, defausse)

                        before.append(l_carte_possible[0])
                        before.append(l_carte_possible[1])
                        before.append(l_carte_possible[2])
                        cartes_j2.remove(l_carte_possible[0])
                        cartes_j2.remove(l_carte_possible[1])
                        cartes_j2.remove(l_carte_possible[2])
                    elif mode == 3: #mode quadruple
                        l_carte_possible, peut_jouer = cartes_quadruple(cartes_j2, defausse)
                            
                        before.append(l_carte_possible[0])
                        before.append(l_carte_possible[1])
                        before.append(l_carte_possible[2])
                        before.append(l_carte_possible[3])
                        cartes_j2.remove(l_carte_possible[0])
                        cartes_j2.remove(l_carte_possible[1])
                        cartes_j2.remove(l_carte_possible[2])
                        cartes_j2.remove(l_carte_possible[3])

                    mode_actuel = ajouter_prop_carte(defausse, before) #on ajoute tout ca a la defausse


                elif mode_actuel == 1: #si il n'y a que des simples #SamueL..
                    cartes = carte_possible(cartes_j2, defausse,2) #on regarde les cartes possible a joueur
                    cartes_a_jouer = cartes[1] #on met dans uen liste
                    autre_que_2 = 0
                    for cartes in cartes_a_jouer:
                        if cartes.valeur != 15: #si il n'a que des 2 a joeur alors il joueur des 2 sinon il joueu autre chose
                            autre_que_2+=1

                    if autre_que_2 ==0:
                        carte_prise = cartes_a_jouer[0]
                        k = cartes_j2.index(carte_prise)
                        cartes_j2[k].poser_carte(defausse, cartes_j2)
         
                    else:

                        if tg==False:

                            carte_prise_valeur = 15
                            while carte_prise_valeur == 15:
                                carte_prise = random.choice(cartes_a_jouer)
                                carte_prise_valeur = carte_prise.valeur
                            k = cartes_j2.index(carte_prise)
                            if defausse[-1].valeur == cartes_j2[k].valeur:
                                tg = True
                            cartes_j2[k].poser_carte(defausse, cartes_j2)


                        else:

                            carte_prise_valeur = 0
                            while carte_prise_valeur != defausse[-1].valeur:
                                carte_prise = random.choice(cartes_a_jouer)
                                carte_prise_valeur = carte_prise.valeur
                         
                            carte_prise.poser_carte(defausse, cartes_j2)
                elif mode_actuel == 2:  #double..
                    cartes_a_jouer, nb_carte_possible = cartes_double(cartes_j2, defausse) #on met dans une liste [[3,3,], [4,4], [5,5]] toutes les paires possibles du jeu
                    num_liste = -1
                    quitter = 0
                    for listes in cartes_a_jouer: #on parcours ces listes
                        num_liste+=1
                        for el in listes: #en parcourant les elements dans la liste on regarde si ils sont = ou > a ce qui est dans la defausse
                            if el.valeur >= defausse[-1].valeur: #si c'est le cas on quitte toute la boucle avec le numero de la list
                                quitter = 1
                                break

                        if quitter:
                            break
                    carte_prise1 = cartes_a_jouer[num_liste][0] #la carte 1, est la carte dans la liste k, et le numer 0
                    carte_prise2 = cartes_a_jouer[num_liste][1] #la carte 2,e st al carte dans la liste k , et le numero 1
                    before.append(carte_prise1)
                    before.append(carte_prise2)
                    cartes_j2.remove(carte_prise1)
                    cartes_j2.remove(carte_prise2)
                    mode_actuel = ajouter_prop_carte(defausse, before) #on ajoute toute ca a la defausse  

                elif mode_actuel == 3: #Arthur
                               
                    l_carte_possible, peut_jouer = cartes_triples(cartes_j2, defausse)

                    if peut_jouer == True:
                        
                        before.append(l_carte_possible[0])
                        before.append(l_carte_possible[1])
                        before.append(l_carte_possible[2])
                        cartes_j2.remove(l_carte_possible[0])
                        cartes_j2.remove(l_carte_possible[1])
                        cartes_j2.remove(l_carte_possible[2])

                        mode_actuel = ajouter_prop_carte(defausse, before) #on ajoute tout ca a la defausse
    
                timer=0
                n_tour+=1     
                
             
       ## CARTES POSSIBLES ET GAGNER AUTOMATIQUEMENT        
        if len(before) == 0: # TEST PARTI FINI !
        
            if len(cartes_j1) == 0 or len(cartes_j2) == 0:
                if len(cartes_j1) != 0: #bot a gagné
                    echange,gagnant,perdant  = parti_fini(pseudo_bot, pseudo)
                elif len(cartes_j2) != 0: #joueur1 a gagné
                    echange,gagnant,perdant = parti_fini(pseudo, pseudo_bot)

        #Test pour gagner automatiquement si un joueur n'a plus de carte; les magique si on joue 4 fois, et la gestion des tg, si un joueur doit rejouer ou peut rejouer
        if not before:
            if n_tour % 2 == 0:

                n_tour, tg, perdu = gagne_auto(cartes_j1, 1, cartes_j2, 2, defausse, tg, n_tour,mode_actuel)
                if perdu == 1:
                    game_over(defausse, n_tour,"bot")
                    mode_actuel = 0
                    n_tour = 1
                    defausse = []
                else:pass
            if n_tour % 2 != 0:
                n_tour, tg, perdu = gagne_auto(cartes_j2, 2, cartes_j1, 1, defausse, tg, n_tour,mode_actuel)
                if perdu == 1:
                    game_over(defausse, n_tour,pseudo)
                    mode_actuel = 0
                    n_tour = 0
                    defausse = []
                else:pass




        


        refreshJeu(pseudo, pseudo_bot, score, score_bot, msgAdmin)
        py.time.wait(10)


pseudoInput = menu()
if pseudoInput != 0:
    pseudo, score = checkPseudo(pseudoInput)
    old_score = score #on initialise le score du départ pour le remplacer apres

    load()
    
    main()