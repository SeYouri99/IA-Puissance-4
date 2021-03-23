import time
import os
from copy import deepcopy
from random import shuffle

# Rouge     = '\033[1;31;40m'
# Rouge_2  = '\033[0;31;47m'
# Bleu_2 = '\033[0;34;47m'
# Jaune  = '\033[1;33;40m'
# Bleu    = '\033[1;34;40m'
# Magenta = '\033[1;35;40m'
# Noir    = '\033[0;30;40m'

largeur = 12
hauteur = 6
ia = 'o'
humain = 'x'
pions_dispos=42

#crée un tableau de jeu vide
def initialiser_tableau():
    tableau = []
    for i in range(hauteur):
        tableau.append([])
        for j in range(largeur):
            tableau[i].append(' ')
    return tableau

#regarde si une colonne est remplie ou non
def colonne_valide(tableau, colonne):
    if tableau[0][colonne] == ' ':
        return True
    return False

#regarde si on ne sort pas de la grille de jeu
def coordonees_valides(ligne, colonne):
    if ligne >= 0 and colonne >= 0 and ligne < hauteur and colonne < largeur:
        return True
    return False

#retourne toute les colonnes non remplies du tableau de jeu
def Actions(tableau):
    colonnes = []
    for colonne in range(largeur):
        if colonne_valide(tableau, colonne):
            colonnes.append(colonne)
    return colonnes

#place le pion du joueur dans la colonne choisie
def Result(tableau, colonne, joueur):
    tab = deepcopy(tableau)
    for ligne in range(5,-1,-1):
        if tab[ligne][colonne] == ' ':
            tab[ligne][colonne] = joueur
            return tab, ligne, colonne

#regarde si le coup joué est dans une colonne vide  ou non
def coup_valide(colonne, tableau):
    for ligne in range(hauteur):
        if tableau[ligne][colonne] == ' ':
            return True
    return False

#regarde si le plateau est rempli
def plateau_rempli(tableau):
    #regarde si 42 pions sont placés
    c=0
    for ligne in range(hauteur):
        for colonne in range(largeur):
            if tableau[ligne][colonne]!=' ': c+=1
    if c==pions_dispos:
        return True

#regarde si il y a 4 signes similaires de suite dans la grille
def quatre_a_la_suite(tableau):

    def victoire_verticale(ligne, colonne):
        victoire = False
        count = 0
        for l in range(ligne, hauteur):
            if tableau[l][colonne] == tableau[ligne][colonne]:
                count += 1
            else:
                break

        if count >= 4:
            victoire = True

        return victoire, count

    def victoire_horizontale(ligne, colonne):
        victoire = False
        count = 0
        for c in range(colonne, largeur):
            if tableau[ligne][c] == tableau[ligne][colonne]:
                count += 1
            else:
                break

        if count >= 4:
            victoire = True

        return victoire, count

    def victoire_diagonale_positive(ligne,colonne):

        pente = None
        count = 0
        c = colonne
        for l in range(ligne, hauteur):
            if c > largeur-1:
                break
            elif tableau[l][c] == tableau[ligne][colonne]:
                count += 1
            else:
                break
            c += 1

        if count >= 4:
            pente = 'pos'

        return pente, count

    def victoire_diagonale_negative(ligne,colonne):

        pente = None
        count = 0
        c = colonne
        for l in range(ligne, -1, -1):
            if c > largeur-1:
                break
            elif tableau[l][c] == tableau[ligne][colonne]:
                count += 1
            else:
                break
            c += 1

        if count >= 4:
            pente = 'neg'

        return pente, count

    def victoire_diagonale(ligne,colonne):
        pente_positive , c1 = victoire_diagonale_positive(ligne,colonne)
        pente_negative , c2 = victoire_diagonale_negative(ligne,colonne)

        if   pente_positive == 'pos' and pente_negative == 'neg':
            quatre_a_la_suite = True
            pente = 'posneg'
        elif pente_positive == None and pente_negative == 'neg':
            quatre_a_la_suite = True
            pente = 'neg'
        elif pente_positive == 'pos' and pente_negative == None:
            quatre_a_la_suite = True
            pente = 'pos'
        else:
            quatre_a_la_suite = False
            pente = None

        return quatre_a_la_suite, pente, c1, c2

    #mets la ligne gagnante en majuscule
    def majuscule_gagnante(ligne, colonne, direction):
        if direction == 'verticale':
            for l in range(verticalCount):
                tableau[ligne+l][colonne] = tableau[ligne+l][colonne].upper()
        elif direction == 'horizontale':
            for c in range(horizontalCount):
                tableau[ligne][colonne+c] = tableau[ligne][colonne+c].upper()
        elif direction == 'diagonale':
            if pente == 'pos' or pente == 'posneg':
                for d in range(positiveCount):
                    tableau[ligne+d][colonne+d] = tableau[ligne+d][colonne+d].upper()
            elif pente == 'neg' or pente == 'posneg':
                for d in range(negativeCount):
                    tableau[ligne-d][colonne+d] = tableau[ligne-d][colonne+d].upper()

    #initialisation des variables
    quatre = False #cette variable indique si il y a quatre à la suite
    pente = None
    verticalCount   = 0
    horizontalCount = 0
    positiveCount   = 0
    negativeCount   = 0
    for l in range(hauteur):
        for c in range(largeur):
            if tableau[l][c] != ' ':
                # regarde si une victoire verticale commence à [l,c]
                quatre_a_la_suite, verticalCount = victoire_verticale(l, c)
                if quatre_a_la_suite:
                    majuscule_gagnante(l, c, 'verticale')
                    quatre = True

                quatre_a_la_suite, horizontalCount =victoire_horizontale(l, c)
                # regarde si une victoire horizontale commence à [l,c]
                if quatre_a_la_suite:
                    majuscule_gagnante(l, c, 'horizontale')
                    quatre = True
                # regarde si une victoire diagonale commence à [l,c]
                # et prend sa pente
                quatre_a_la_suite, pente , positiveCount, negativeCount = victoire_diagonale(l, c)
                if quatre_a_la_suite:
                    majuscule_gagnante(l, c, 'diagonale')
                    quatre = True

    return quatre
#donne le nombre d'emplacements vides où il est possible de jouer
def emplacements_vides(tableau):
    emplacements_vides = 0
    for ligne in range(hauteur):
        for colonne in range(largeur):
            if tableau[ligne][colonne] == ' ':
                emplacements_vides += 1
    return emplacements_vides

def afficher_tableau(tableau):
    #on clear la console
    os.system('cls' if os.name == 'nt' else 'clear')
    emplacements = 72 - emplacements_vides(tableau)
    print('')
    print( '         TOUR #' + str(emplacements) , end=" ")   #affiche le tour auquel nous sommes
    print("\n\n  1   2   3   4   5   6   7   8   9   10  11  12")

    for i in range(0, hauteur, 1):
        for j in range(largeur):
            if str(tableau[i][j]) == 'x':
                print("| " +str(tableau[i][j]) , end=" ")   #affiche une croix
            elif str(tableau[i][j]) == 'o':
                print("| " +str(tableau[i][j]) , end=" ")   #afficher un rond 
            elif str(tableau[i][j]) == 'X':
                print("| " +str(tableau[i][j]) , end=" ")
            elif str(tableau[i][j]) == 'O':
                print("| " + str(tableau[i][j]) , end=" ")
            else:
                print("| " + str(tableau[i][j]), end=" ")

        print("|")
    print('')
def compte_suite(tableau, joueur, longueur):
    """ Selon l'état actuel du tableau , le joueur actuel et la longueur chosie de la suite que l'on veut compter
        ça retourne le nombre de suite de la longueur choisie
    """
    def suite_verticale(ligne, colonne):
        """retourne 1 si ça trouve une suite verticale de la bonne longueur
        """
        count = 0
        for l in range(ligne, hauteur):
            if tableau[l][colonne] == tableau[ligne][colonne]:
                count += 1
            else:
                break
        if count >= longueur:
            return 1
        else:
            return 0

    def suite_horizontale(ligne, colonne):
        """return 1 si ça trouve une suite horizontale de la bonne longueur
        """
        count = 0
        for c in range(colonne, largeur):
            if tableau[ligne][c] == tableau[ligne][colonne]:
                count += 1
            else:
                break
        if count >= longueur:
            return 1
        else:
            return 0

    def suite_diagonale_negative(ligne, colonne):
        """return 1 si ça trouve une suite diagonale négative de la bonne longueur
        """
        count = 0
        c = colonne
        for l in range(ligne, -1, -1):
            if c > largeur-1:
                break
            elif tableau[l][c] == tableau[ligne][colonne]:
                count += 1
            else:
                break
            c += 1 #incremente la colonne quand la ligne est  incrementee
        if count >= longueur:
            return 1
        else:
            return 0

    def suite_diagonale_positive(ligne, colonne):
        """return 1 si ça trouve une suite diagonale positive de la bonne longueur
        """
        count = 0
        c = colonne
        for l in range(ligne, hauteur):
            if c > largeur-1:
                break
            elif tableau[l][c] == tableau[ligne][colonne]:
                count += 1
            else:
                break
            c += 1 #incremente la colonne quand la ligne est  incrementee
        if count >= longueur:
            return 1
        else:
            return 0

    totalCount = 0
    # pour chaque piece dans le tableau
    for ligne in range(hauteur):
        for colonne in range(largeur):
            # jouée par le joueur que l'on cherche
            if tableau[ligne][colonne] == joueur:
                # regarde si une suite verticale commence à (ligne, colonne)
                totalCount += suite_verticale(ligne, colonne)
                # regarde si une suite horizontale commence à (ligne, colonne)
                totalCount += suite_horizontale(ligne, colonne)
                # # regarde si une suite diagonale commence à (ligne, colonne)
                totalCount += (suite_diagonale_positive(ligne, colonne) + suite_diagonale_negative(ligne, colonne))
    # return the sum of sequences of length 'length'
    return totalCount

def Utility(tableau, joueur):
    """la fonction utility évalue l'état du tableau et le report à la fonction appelée,
        la valeur utility est définie comme le score du joueurqui apelle la focntion - score du joueur adverse ,
        le score de chque joueur est la somme de chque suite trouvée pour ce joeur multipliées par un plus grand facteur pour les suite les plus lonngues.
    """
    if joueur == humain: adversaire = ia
    else: adversaire = humain

    suite_4_joueur    = compte_suite(tableau, joueur, 4)
    suite_3_joueur  = compte_suite(tableau, joueur, 3)
    suite_2_joueur    = compte_suite(tableau, joueur, 2)
    score_joueur    = suite_4_joueur*99999 + suite_3_joueur*999 + suite_2_joueur*99

    suite_4_adversaire    = compte_suite(tableau, adversaire, 4)
    suite_3_adversaire  = compte_suite(tableau, adversaire, 3)
    suite_2_adversaire = compte_suite(tableau, adversaire, 2)
    score_adversaire    = suite_4_adversaire*99999 + suite_3_adversaire*999 + suite_2_adversaire*99

    if suite_4_adversaire > 0:
        #cela signifie que le joueur actuel a perdu la partie
        #on retourne alors la plus grande valeur négative
        return float('-inf')
    else:
        #retourne le score du joueur moins le score de l'aversaire
        return score_joueur - score_adversaire


def est_finie(tableau):
    """regarde si il y a un gagnant dans l'état actuel de la partie
    """
    if compte_suite(tableau, humain, 4) >= 1:
        return True
    elif compte_suite(tableau, ia, 4) >= 1:
        return True
    else:
        return False

def min_max_alpha_beta(tableau, profondeur, joueur):
    # obtiens le tableau des coups valides
    coups_legaux = Actions(tableau)
    shuffle(coups_legaux)
    meilleur_coup  = coups_legaux[0]
    meilleur_score = float("-inf")

    # initialisation de alpha et beta
    alpha = float("-inf")
    beta = float("inf")

    if joueur == ia: adversaire = humain
    else: adversaire = ia

    # parcours tous ces tableaux
    for coup in coups_legaux:
        # crée un nouveau tableau à partie de coup
        tab = Result(tableau, coup, joueur)[0]
        # appelle min sur ce nouveau tableau
        tableau_score = min(tab, profondeur-1, alpha, beta, joueur, adversaire)
        if tableau_score > meilleur_score:
            meilleur_score = tableau_score
            meilleur_coup = coup
    return meilleur_coup

def min(tableau, profondeur, a, b, joueur , adversaire):
    coups_legaux = []
    for colonne in range(largeur):
        #si la colonne "colonne" est un coup légal
        if coup_valide(colonne, tableau):
            # faire le coup "colonne pour le joueur actuel
            tab = Result(tableau, colonne, joueur)[2]
            coups_legaux.append(tab)

    # on regarde si la partie est finie
    if profondeur == 0 or len(coups_legaux) == 0 or est_finie(tableau):
        return Utility(tableau, joueur)

    coups_legaux= Actions(tableau)
    beta = b

    # # si on atteint la fin de l'arbre, on evalue le score
    for coup in coups_legaux:
        tableau_score = float("inf")
        # sinon on continue à descendre l'arbre jusqu'a rencontrer la condition alpha beta
        if a < beta:
            tabbis = Result(tableau, coup, adversaire)[0]
            tableau_score = max(tabbis, profondeur - 1, a, beta, joueur, adversaire)

        if tableau_score < beta:
            beta = tableau_score
    return beta

def max(tableau, profondeur, a, b, joueur, adversaire):
    coups_legaux = []
    for colonne in range(largeur):
        # si la colonne "colonne" est un coup legal
        if coup_valide(colonne, tableau):
            #faire le coup "colonne" pour le joueur actuel
            temp = Result(tableau, colonne, joueur)[2]
            coups_legaux.append(temp)
    #on regarde si la partie est finie
    if profondeur == 0 or len(coups_legaux) == 0 or est_finie(tableau):
        return Utility(tableau, joueur)

    alpha = a
    # si on atteint la fin de l'arbre, on evalue le score
    for coup in coups_legaux:
        tableau_score = float("-inf")
        if alpha < b:
            temptableau = Result(tableau, coup, joueur)[0]
            tableau_score = min(temptableau, profondeur - 1, alpha, b, joueur, adversaire)

        if tableau_score> alpha:
            alpha = tableau_score
    return alpha

dir_path = os.getcwd()
os.chdir(dir_path)

def tour_du_joueur(tableau):
    colonne = input('choisir une colonne entre 1 et 12 : '  )
    if not(colonne.isdigit()):
        print("la colonne doit être un entier" )
        return tour_du_joueur(tableau)

    coup_du_joueur = int(colonne) - 1

    if coup_du_joueur < 0 or coup_du_joueur > 12:
        print("la colonne doit etre entre 1 et 12!" )
        return tour_du_joueur(tableau)

    if not(colonne_valide(tableau, coup_du_joueur)):
        print("la colonne choisie est remplie"  )
        return tour_du_joueur(tableau)


    tableau = Result(tableau, coup_du_joueur, humain)[0]
    joueur_quatre_a_la_suite  = quatre_a_la_suite(tableau)
    return tableau, coup_du_joueur, joueur_quatre_a_la_suite

def humain_gagne(tableau):
    afficher_tableau(tableau)
    print('                    '"humain gagne !\n" )
    rejouer = True if input('rejouer (o/n)?').lower() == 'o' else False
    if rejouer:
        Main()
    return 0

def tour_de_ia(tableau,profondeur):
    debut= time.time()
    coup_de_ia  = min_max_alpha_beta(tableau, profondeur, ia)
    fin = time.time()
    temps=round(fin - debut, 7)
    tableau = Result(tableau, coup_de_ia, ia)[0]
    quatre_a_la_suite_ia  = quatre_a_la_suite(tableau)

    return  tableau, coup_de_ia, quatre_a_la_suite_ia,temps


def ia_gagne(tableau):
    afficher_tableau(tableau)
    print('                     '"ia gagne!\n" )
    rejouer = True if input('rejouer (o/n)?').lower() == 'o' else False
    if rejouer:
        Main()
    return 0

def obtenir_profondeur():
    profondeur = input('entrer difficulté (1-5) '  )
    if not(profondeur.isdigit()):
        print('la difficulté doit être un entier' )
        return obtenir_profondeur()

    profondeur = int(profondeur,10)

    if profondeur < 1 or profondeur > 5:
        print("la difficulté doit être entre 1 et 5"  )
        return obtenir_profondeur()

    return profondeur

def Main():
    tableau = initialiser_tableau()
    os.system('cls' if os.name == 'nt' else 'clear')
    afficher_tableau(tableau)
    profondeur = obtenir_profondeur()
    i = 1
    qui_commence = True if input('voulez-vous commencer (o/n)? '  ).lower() == 'o' else False
    tableau = initialiser_tableau()

    while(i):
        if plateau_rempli(tableau) :
            print("fin de partie\n")
            break

        if qui_commence:
            #humain
            tableau,coup_humain,joueur_quatre_a_la_suite = tour_du_joueur(tableau)

            if joueur_quatre_a_la_suite:
                i = humain_gagne(tableau)
                if i ==0:
                    break
            afficher_tableau(tableau)
            print("\t""le joueur a joué la colonne " +str(coup_humain+1))


            #ia
            tableau, coup_ia, quatre_a_la_suite_ia,temps = tour_de_ia(tableau,profondeur)
            if quatre_a_la_suite_ia:
                i = ia_gagne(tableau)
                if i ==0:
                    break
            afficher_tableau(tableau)
            print("\t""l'ia a joué la colonne "+str(coup_ia+1) )
            print("\t""temps mis par l'ia: "+str(temps))
        else:
            #ia
            tableau,coup_ia,quatre_a_la_suite_ia,temps = tour_de_ia(tableau,profondeur)
            if quatre_a_la_suite_ia:
                i = ia_gagne(tableau)
                if i ==0:
                    break
            afficher_tableau(tableau)
            print("\t""l'ia a joué la colonne "+ str(coup_ia+1))
            print("\t""temps mis par l'ia: "+str(temps))

            #humain
            tableau,coup_humain, joueur_quatre_a_la_suite = tour_du_joueur(tableau)
            if joueur_quatre_a_la_suite:
                i = humain_gagne(tableau)

                if i ==0:
                    break

            afficher_tableau(tableau)
            print("\t""le joueur a joué la colonne "+str(coup_humain+1))

Main()
