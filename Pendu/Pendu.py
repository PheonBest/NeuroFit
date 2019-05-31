# -*- coding: utf-8 -*-
import codecs
import sys
g = sys.modules['__main__']
# On importe les variables globales du fichier 'Hub.py' qui sont des attributs du module 'Hub'
import unicodedata #Pour enlever les accents des mots
import numpy as np #Pour multiplier des matrices
import math
from random import randint #Pour choisir un mot aléatoire
from tkinter import *
import time

#Classes et fonctions ------------------------

#On défini la classe Titre:
class Title:
    def __init__(self,text_,x_,y_,size):

        self.text = text_

        #On enlève les accents:
        #On normalise la string sous forme NKFD,
        #c'est à dire décomposée de façon compatible
        self.normalizedText = unicodedata.normalize('NFKD', self.text)
        #On ajoute chaque lettre au mot
        self.normalizedText = u"".join([c for c in self.normalizedText if not unicodedata.combining(c)])
        #On met en minuscule le texte
        self.normalizedText = self.normalizedText.lower()

        self.titleSize = size
        self.currentText = ''
        for i in range(len(self.text)):
            if self.text[i] in excludedCharacters:
                self.currentText += self.text[i]
            else:
                self.currentText += '*' #Chaque lettre correspond à un '*' pour ne pas la dévoiler

        self.x = x_
        self.y = y_

        self.rect = [] #Rectangles sous les lettres
        self.allTexts = [] #Lettres

        self.draw(1) #On dessine les lettres et les rectangles sous celles-ci

    def delete(self, delRect=0):
        if (delRect):

            for i in range( len(self.rect) ):
                g.w.delete(self.rect[i])
            self.rect.clear()

        for i in range( len(self.allTexts) ):
            g.w.delete(self.allTexts[i])
        self.allTexts.clear()

    def draw(self, drawRect=0, color='white'):
        global interSpace
        separateLength = 0

        for i in range( len(self.text) ): #Pour chaque lettre du mot:

            if (drawRect):
                #En x0: on ajoute la taille d'un rectangle par itérations de la boucle     +L'espace cumulé
                #En y0: Constante
                #En x1: on ajoute la taille d'un rectangle par (itérations de la boucle + 1) +L'espace cumulé
                #En y1: Constante + Taille du rectangle/5
                if self.text[i] not in excludedCharacters:
                    self.rect.append( g.w.create_rectangle(self.x+self.titleSize*i+separateLength, self.y, self.x+self.titleSize*(i+1)+separateLength, self.y+self.titleSize/5, fill="white") )
            #En x: on ajoute la taille d'un rectangle par itérations de la boucle     +L'espace cumulé //+10 à cause d'un décalage//
            #En y: Taille du texte multiplié par 4/3 pour s'y adapter
            self.allTexts.append( g.w.create_text(self.x+self.titleSize*i+separateLength+ 10*g.prop[0], self.y-self.titleSize*(4/3)*g.prop[1], text=self.currentText[i], anchor='nw', fill=color, font=("Courier", int(self.titleSize)), justify='center') )
            #On cumule les espaces entre chaque lettre/rectangle
            separateLength += interSpace

    def isInTextAndReplace(self,newLetter):
        changed = False
        for i in range( len(self.text) ):

            if self.normalizedText[i] == newLetter:
                self.currentText = self.currentText[:i] + self.text[i] + self.currentText[i+1:]
                changed = True

        return changed


    def isEnded(self):
        ended = True
        for i in range(len(self.currentText)):
            if self.currentText[i] == '*':
                ended = False
        return ended

class Line:
    def __init__(self, ptA_, vector_, toRotate=0):

        self.ptA= ptA_ #Point d'application, c'est le premier point de la ligne
        self.ptA[0] *= g.prop[0] #Proportionnel à la largeur de la fenêtre
        self.ptA[1] *= g.prop[1] #Proportionnel à la hauteur de la fenêtre

        self.vector = vector_ #Distance ajoutée au point d'application pour obtenir le deuxième point de la ligne
        self.vector[0] *= g.prop[0] #Proportionnel à la largeur de la fenêtre
        self.vector[1] *= g.prop[1] #Proportionnel à la hauteur de la fenêtre

        self.toRotate = toRotate #Enregistre si la ligne sera tournée ou non

    def move(self, newVec):
        self.vector = newVec #On enregistre le nouveau vecture
        g.w.coords(self.line,self.ptA[0], self.ptA[1], self.ptA[0]+self.vector[0], self.ptA[1]+self.vector[1]) #On modifie les coordonnées de la ligne selon le nouveau vecteur

    def draw(self):
        global axis,totalTheta,color

        #On créée la ligne dans le canvas w
        self.line = g.w.create_line(self.ptA[0], self.ptA[1], self.ptA[0]+self.vector[0], self.ptA[1]+self.vector[1], fill=color)

        if self.toRotate == 1: #Si la ligne doit être mise en rotation
            M0 = M(axis, totalTheta) #On calcule la matrice de rotation selon l'axe y et selon l'angle déjà parcouru par les autres pièces en rotation
            self.move( np.dot(M0,self.vector) ) #On modifie les coordonnées de la ligne selon le produit vectoriel de la matrice de rotation et du vecteur
            toRotate.append(self) #On ajoute la ligne aux éléments en rotation

    def delete(self):
        try:
            g.w.delete(self.line)
        except:
            pass

class Circle:
    def __init__(self, ptA_, vector_, toRotate=0):
        self.vector = vector_ #Le vecteur correspond au rayon du cercle
        self.vector[0] *= g.prop[0]
        self.vector[1] *= g.prop[1]

        self.ptA= ptA_
        self.ptA[0] *= g.prop[0]
        self.ptA[1] *= g.prop[1]

        self.toRotate = toRotate

    def draw(self):
        global axis,totalTheta,color

        #On créée la ligne dans le canvas w
        self.circle = g.w.create_oval(self.ptA[0]-self.vector[0], self.ptA[1]-self.vector[1], self.ptA[0]+self.vector[0], self.ptA[1]+self.vector[1], fill=color, outline="")

        if self.toRotate == 1: #Si la ligne doit être mise en rotation
            M0 = M(axis, totalTheta) #On calcule la matrice de rotation selon l'axe y et selon l'angle déjà parcouru par les autres pièces en rotation
            self.move( np.dot(M0,self.vector) ) #On modifie les coordonnées de la ligne selon le produit vectoriel de la matrice de rotation et du vecteur
            toRotate.append(self) #On ajoute la ligne aux éléments en rotation

    def move(self, newRadius):
        self.vector = newRadius
        g.w.coords(self.circle, self.ptA[0]-self.vector[0], self.ptA[1]-self.vector[1], self.ptA[0]+self.vector[0], self.ptA[1]+self.vector[1])

    def delete(self):
        try:
            g.w.delete(self.circle)
        except:
            pass

def drawStickman(part):
    global globalIndex

    lines[part].draw() #On dessine l'élément correspondant aux hp restants du joueur

    if health == 5: #Si on dessine la tête, on met en rotation le stickman
        globalIndex +=1
        stickmanRotate(globalIndex) #Toutes les 1/60 secondes, on met en rotation les éléments appartenant à la liste toRotate

def M(axis, theta):
    #Retourne la matrice de rotation dans le sens trigonométrique
    #correspondant à un angle theta autour d'un axe donné.

    #Selon la formule d'Euler-Rodrigues, (https://en.wikipedia.org/wiki/Euler%E2%80%93Rodrigues_formula)
    #Les paramètres d'Euler sont déterminés selon l'axe de rotation, c'est à dire le vecteur unitaire:
    #On divise l'axe par sa norme pour avoir le vecteur unitaire
    axis = axis / np.sqrt( np.dot(axis, axis) )
    #Les paramètres d'Euler sont:
    a = math.cos(theta / 2.0)
    b,c,d = axis * math.sin(theta / 2.0)

    #On utilise alors la matrice de rotation donnée par la formule.
    #Pour plus de clarté, on défini a^2, b^2, c^2 et d^2:
    #                               b*c, a*d, a*b, b*d et c*d:
    aa, bb, cc, dd = a * a, b * b, c * c, d * d
    bc, ad, ac, ab, bd, cd = b * c, a * d, a * c, a * b, b * d, c * d
    #On retourne alors l'array correspondant à la matrice de rotation:
    return np.array([[aa + bb - cc - dd, 2 * (bc + ad), 2 * (bd - ac)],
                     [2 * (bc - ad), aa + cc - bb - dd, 2 * (cd + ab)],
                     [2 * (bd + ac), 2 * (cd - ab), aa + dd - bb - cc]])

def stickmanRotate(currentIndex):
    global v,axis,theta,M0,totalTheta,globalIndex

    for i in range(len(toRotate)):

        toRotate[i].move( np.dot(M0,toRotate[i].vector) )

    if currentIndex == globalIndex:
        totalTheta += theta
        g.fenetre.after(16, lambda i=currentIndex: stickmanRotate(i))

def returnToHub(direction = 'gameChoice'):
    global textChoiceButtons, Nbrtrouve, buttons, title, lines, myEntry

    for i in range(len(buttons)):
        buttons[i].destroy()
    buttons.clear()

    toRotate.clear()
    for i in range(len(lines)):
        lines[i].delete()
    if title is not None:
        title.delete(1)
        title = None
    try:
        myEntry.destroy()
        myEntry=None
    except:
        pass

    g.w.delete(Nbrtrouve)
    Nbrtrouve = None

    for i in range(len(textChoiceButtons)):
        textChoiceButtons[i].destroy()
    textChoiceButtons.clear()

    g.backToHub(direction)

falsePositiveClick = None
falsePositiveTimeDelay = 0.7 #secondes
def isItFalsePositiveClick(function_name, arg=None):
    if time.time() - falsePositiveClick > falsePositiveTimeDelay:
        if arg == None:
            function_name()
        else:
            function_name(arg)

def restartButtonAppear():
    global touches, buttons, indice, falsePositiveClick
    falsePositiveClick = time.time()

    for i in range(len(touches)):
        touches[i].destroy()
    touches.clear()

    try: #On utilise un try car si la difficulté est à 0, on ne donne pas d'indice
        indice.destroy()
        indice = None
    except:
        pass

    buttons.append( Button(g.w, text=g.translate('Hub'), command = lambda function_name=returnToHub, direction='gameChoice': isItFalsePositiveClick(function_name,direction), anchor = NW, font=( "Courier",int(20*g.prop[2]) )) )
    buttons[len(buttons)-1].place(x=100*g.prop[0], y=300*g.prop[1], width=200*g.prop[0], height=150*g.prop[1])

    buttons.append( Button(g.w, text=g.translate('Recommencer'), command = lambda function_name=restartAll: isItFalsePositiveClick(function_name), anchor = NW, font=( "Courier",int(20*g.prop[2]) )) )
    buttons[len(buttons)-1].place(x=300*g.prop[0], y=300*g.prop[1], width=200*g.prop[0], height=150*g.prop[1])

    buttons.append( Button(g.w, text=g.translate('Options'), command = lambda function_name=restartAll, i=True: isItFalsePositiveClick(function_name,i), anchor = NW, font=( "Courier",int(20*g.prop[2]) )) )
    buttons[len(buttons)-1].place(x=500*g.prop[0], y=300*g.prop[1], width=200*g.prop[0], height=150*g.prop[1])

    Nbrdemottrouve()

def restartAll(menu = False):
    global health, title, lines, liste, state, toRotate

    toRotate.clear()

    health = 11

    for i in range(len(lines)):
        lines[i].delete()
    title.delete(1)
    title = None

    for i in range(len(buttons)):
        buttons[i].destroy()
    buttons.clear()

    state = 1

    if menu:
        TextFileChoice()
        #DifficultyChoice
    else:
        if g.plaqueTournante:
            returnToHub('randomGame')
        else:
            wordChoice()

def saveVar(win=True):
    global beginTime, level, difficultyList

    elapsedTime = round(time.time() - beginTime, 3)
    timeList = g.profileVar('PEaverageTime')
    if timeList == 'None':
        timeList = []
    else:
        if isinstance(timeList, (list,)):
            pass
        else:
            timeList = timeList.split(',')
    timeList.append(elapsedTime)
    g.profileVar('PEaverageTime',timeList,True)

    difficultyList = g.profileVar('PEdifficulty')
    if difficultyList == 'None':
        difficultyList = []
    else:
        if isinstance(difficultyList, (list,)):
            pass
        else:
            difficultyList = difficultyList.split(',')
    if str(level) not in difficultyList:
        difficultyList.append(level)
        g.profileVar('PEdifficulty',difficultyList,True)

    if win:
        nbr = g.profileVar('PEvictories')
        if nbr == 'None':
            nbr = 0
        nbr=int(nbr)
        nbr+=1
        g.profileVar('PEvictories',str(nbr),True)
    else:
        nbrDefeats = g.profileVar('PEdefeats')
        if nbrDefeats == 'None':
            nbrDefeats = 0
        nbrDefeats=int(nbrDefeats)
        nbrDefeats+=1
        g.profileVar('PEdefeats',str(nbrDefeats),True)

def letterChoice(letter, index):
    global health, touches, title

    if health > 0:
        letter = letter.lower()
        if (title.isInTextAndReplace(letter)):
            if (title.isEnded()):
                saveVar()

                title.delete()
                title.draw(0, 'green')

                restartButtonAppear()

            else:
                title.delete()
                title.draw()

                touches[index].configure(state='disabled', bg='#4CAF50')
        else:

            health -= 1
            drawStickman(-health+10)

            if health == 0:
                saveVar(False)
                #On remplace les étoiles par les lettres du mot et les lettres connues par des espaces
                tmp_text = title.currentText
                for i in range( len(tmp_text) ):
                    if tmp_text[i]=='*':
                        tmp_text = tmp_text[:i] + title.text[i] + tmp_text[i+1:]
                    elif tmp_text[i]!=' ':
                        tmp_text = tmp_text[:i] + ' ' + tmp_text[i+1:]

                #On remplace les étoiles par des espaces
                title.currentText = title.currentText.replace('*',' ')

                title.delete()
                title.draw()

                title.currentText = tmp_text

                title.draw(0, 'red')

                restartButtonAppear()

            else:

                touches[index].configure(state='disabled', bg='#ff6b6b')

def Keyboard():
    global touches, letterSize
    for ligne in range(3):
        for colonne in range(touchesParLigne):
            if (ligne*touchesParLigne+colonne <= len(liste)-1):

                touches.append(Button(g.w, text=liste[ligne*touchesParLigne+colonne], command = lambda lettre=liste[ligne*touchesParLigne+colonne], index=ligne*touchesParLigne+colonne: letterChoice(lettre,index), anchor = NW))
                touches[len(touches)-1].place(x=50*g.prop[0] +letterSize*colonne, y=300*g.prop[1]+letterSize*ligne, width=letterSize, height=letterSize)

def wordChoice():
    global beginTime, words, word, level, title, interSpace, boutons, Nbrtrouve, indice

    g.w.delete(Nbrtrouve)
    Nbrtrouve = None

    intervalle = difficultyDict.get( orderedDifficulty[ level ] )

    if intervalle[1] == '∞':
        l = list(filter(lambda x: len(x) >= intervalle[0], words))
    else:
        l = list(filter(lambda x: len(x) >= intervalle[0], words))
        l = list(filter(lambda x: len(x) <= intervalle[1], l))
    rand = randint(0, len(l)-1)
    word = l[ rand ]

    del words[rand] #On le supprime de la liste pour ne pas retomber dessus

    # g.screeny[0]/2 - (len(word) * titlesize)/2 -interSpace*(len(word)-1)/2>= 0.20*g.screeny[0]/2

    TitleSize = ( 0.20*g.screeny[0]/2 - g.screeny[0]/2 +interSpace*(len(word)-1)/2 )*(-2)/len(word)
    if TitleSize > 100:
        TitleSize = 100

    title = Title(word, (g.screeny[0]/2-len(word)/2 * TitleSize - (interSpace*(len(word)-1))/2 )*g.prop[0], 150*g.prop[1], TitleSize)

    Keyboard()

    if level != 0:
        indice = Button(g.w, text=g.translate('Indice'), command = Indice, anchor = NW, font=( "Courier",int(20*g.prop[2]) ) )
        indice.place(x=50*g.prop[0], y=320*g.prop[1]+lineNumber*letterSize, width=170*g.prop[0], height=70*g.prop[1])

    beginTime = time.time()

def difficulty(newLevel):
    global level, buttons

    intervalle = difficultyDict.get( orderedDifficulty[ newLevel ] )

    if intervalle[1] == '∞':
        l = list(filter(lambda x: len(x) >= intervalle[0], words))
    else:
        l = list(filter(lambda x: len(x) >= intervalle[0], words))
        l = list(filter(lambda x: len(x) <= intervalle[1], l))
    if len(l) == 0:
        buttons[newLevel].configure(text=g.translate('Il n\'existe pas de mots correspondants à cette longueur !'), fg='white', bg='#ff6b6b', state='disabled',wraplength=170)
    else:
        level = newLevel

        for i in range(len(buttons)):
            buttons[i].destroy()
        buttons.clear()
        wordChoice()

def DifficultyChoice():
    global buttons, startButton, myEntry

    try:
        startButton.destroy()
        startButton = None
        myEntry.destroy()
        myEntry = None
    except:
        pass

    for i in range(3):
        intervalle = difficultyDict.get(orderedDifficulty[i])
        buttons.append(Button(g.w, text = g.translate(orderedDifficulty[i]) +'\n'+ str(intervalle[0])+' '+g.translate('à')+' '+str(intervalle[1])+' '+g.translate('lettres'), command = lambda i=i: difficulty(i), anchor = NW,font=("Courier",int(12*g.prop[2]))))
        buttons[len(buttons)-1].configure(fg='white', background='#111', activebackground = '#4CAF50', relief = RIDGE, justify='center')
        buttons[len(buttons)-1].place(x=g.screeny[0]/2-buttonSize*1.5 +buttonSize*i, y=g.screeny[1]/2-buttonSize/2, width=buttonSize, height=buttonSize)

def getInput(event):
    global myEntry, textChoiceButtonsDescription, words
    if (myEntry != None):

        result = myEntry.get()
        if (len(result) >=2 and result != '' and result != ' ' and result != '  ' and ',' not in result and ';' not in result):
            if len(words) == 4:
                startButton.configure(command = DifficultyChoice, bg='#111', text=g.translate('Commencer'))
            myEntry.delete(0, 'end')

            words.append(result)
            g.profileVar('PEpersonal', words, True)

def choseFile(file):
    global textChoiceButtons, startButton, words, startButton, myEntry

    for i in range(len(textChoiceButtons)):
        textChoiceButtons[i].destroy()
    textChoiceButtons.clear()

    if file == 'words.txt':
        #On ouvre le dossier 'words.txt' en mode lecture

        f=open(path+g.translate(file), "r")

        words = f.read().replace('\n','').split(',')

        f.close()

        DifficultyChoice()
    else:

        words = g.profileVar('PEpersonal')
        if words == 'None':
            words = []
        print(words)

        if (len(words) < 5):
            startButton = Button(g.w, text = g.translate('Il faut au moins 5 mots !'), anchor = NW, bg='#ff6b6b')
        else:
            startButton = Button(g.w, text = g.translate('Commencer'), command = DifficultyChoice, anchor = NW, bg='#111')
        startButton.configure(fg='white', activebackground = '#4CAF50', relief = FLAT, justify='center')
        startButton.place(x=g.screeny[0]/2-buttonSize, y=g.screeny[1]/2-buttonSize/2, width=buttonSize, height=buttonSize)

        myEntry = Entry(g.w, width=20)
        myEntry.place(x=g.screeny[0]/2-buttonSize +buttonSize, y=g.screeny[1]/2-buttonSize/2)

def TextFileChoice():
    global textChoiceButtons, buttons
    for i in range(2):

        textChoiceButtons.append(Button(g.w, text = textChoiceButtonsDescription[i][1], command = lambda i=textChoiceButtonsDescription[i][0]: choseFile(i), anchor = NW))
        textChoiceButtons[len(textChoiceButtons)-1].configure(fg='white', background='#111', activebackground = '#4CAF50', relief = FLAT, justify='center')
        textChoiceButtons[len(textChoiceButtons)-1].place(x=g.screeny[0]/2-buttonSize +buttonSize*i, y=g.screeny[1]/2-buttonSize/2, width=buttonSize, height=buttonSize)

    buttons.append(Button(g.w, text=g.translate("Retour"), command = lambda direction='gameChoice': returnToHub(direction), anchor = NW, font=("Courier",int(12*g.prop[2]))))
    buttons[len(buttons)-1].configure(fg='white', background='#111', activebackground = '#4CAF50', relief = RIDGE, justify='center')
    buttons[len(buttons)-1].place(x=g.screeny[0]-5/8*240*g.prop[0], y=g.screeny[1]-3/2*30*g.prop[1], width=240*g.prop[0]/2, height=30*g.prop[1])

def Nbrdemottrouve():
    global Nbrtrouve, nbr

    nbr = g.profileVar('PEvictories')
    if nbr == 'None':
        nbr = 0

    Nbrtrouve = g.w.create_text(15*g.prop[0], 10*g.prop[1], text=g.translate('Total de mots trouvés')+': '+str(nbr), anchor = NW, font=("Courier",int(17*g.prop[2])), fill='white')


def Indice():
    global health, liste, indice, healthPerIndice

    if health > healthPerIndice:

        possibleIndexes = [] #Endroits où une lettre est inconnue
        for i in range (len(title.currentText)):
            if title.currentText[i] == '*':
                possibleIndexes.append(i)

        letterToReveal = title.normalizedText[ possibleIndexes[ randint(0, len(possibleIndexes)-1) ] ]

        letterChoice( letterToReveal, liste.index( letterToReveal.upper() ) )

        for i in range(healthPerIndice):
            health -= 1
            drawStickman(-health+10)

    else:

        indice.configure(text=g.translate('Vous avez moins de 3 points de vie !'), fg='white', bg='#ff6b6b', state='disabled',wraplength=170, font=( "Courier",int(12*g.prop[2]) ))

#---------------------------------------------
path = g.resource_path('../Pendu/')

#Variables et exécution du programme
#Liste des caractères exclus, et donc automatiquement rêvélés à l'utilisateur
excludedCharacters = [':','-','.','œ','(',')',' ','’',"'",'_']

lineNumber = 3 #Nombre de lignes composant le clavier

startButton = None #Bouton 'Commencer' qui va mender aux options

myEntry = None #Zone de texte où on entre des mots qui pourront ensuite être choisis aléatoirement

#Liste des fichier texte contenant les mots à choisir
textChoiceButtonsDescription = [ ['words.txt',g.translate('Fichier de mots aléatoire')], ['personal.txt',g.translate('Fichier à remplir')] ]
textChoiceButtons = [] #Liste des boutons permettant de choisir un fichier texte contenant les mots à choisir

Nbrtrouve = None #Score correspondant au nombre de mots trouvés
healthPerIndice = 3 #Nombre de points de vie enlevés par indice

headRadius = 45 #Rayon de la tête du StickMan
border = (850,650) #Bord inférieur gauche de la figure
color = '#FFFFFF' #Couleur du Stickman

height = 370 #Hauteur de la potence
dist = 60 #Distance séparant le coin supérieur gauche de la potence et la planche de soutien

lines = [] #Liste des éléments composant le StickMan
lines.extend([
#Potence
Line([border[0],border[1],0], [320,0]) #0 Bas de la potence =10hp
,Line([border[0]+100,border[1],0], [0,-height,0]) #1 Poteau de la potence =9hp
,Line([border[0]+100,border[1]-height,0], [180,0,0]) #2 Planche vers la droite =8hp
,Line([border[0]+100,border[1]-height+dist,0], [dist,-dist,0]) #3 Planche de maintien de la potence =7hp
,Line([border[0]+280,border[1]-height,0], [0,30,0]) #4Crochet auqel est accroché la corde =6hp


#Stickman
,Circle([border[0]+280, border[1]-height+30+headRadius, 0], [headRadius,headRadius,0], 1) #5 Tête =5hp

,Line([border[0]+280,border[1]-height+30 +2*headRadius,0], [0,100,0], 1) #6 Corps =4hp

,Line([border[0]+280,border[1]-height+30 +2*headRadius,0], [-80,20,0], 1) #7 Bras gauche =3hp
,Line([border[0]+280,border[1]-height+30 +2*headRadius,0], [80,20,0], 1) #8 Bras droit =2hp

,Line([border[0]+280,border[1]-height+30 +2*headRadius+100,0], [-60,100,0], 1) #9 Jambe gauche =1hp
,Line([border[0]+280,border[1]-height+30 +2*headRadius+100,0], [60,100,0], 1) #10 ambe droite =0hp
])

toRotate = [] #Comprend les éléments à mettre en rotation

globalIndex = 0 #Permet de savoir si on continue de faire tourner le stickMan ou non

#L'axe est celui autour du quel se fait la rotation
#Theta est l'angle ajouté à chaque rotation
axis, theta = [0,1,0], 0.03

#On défini la matrice de rotation selon la formule d'Euler-Rodrigues
M0 = M(axis, theta)

#On enregistre l'angle total de rotation pour l'ajouter aux lignes apparaîssant postérieurement
totalTheta = 0

health = 11 #Points de vie du joueur
level = 0 #Niveau de difficulté
indice = None #Bouton qui donne un indice


initTitleSize=100*g.prop[2] #Taille de chaque lettre du titre
title = None #Titre
interSpace = 20*g.prop[0] #Espace entre chaque lettre du titre

#Liste des lettres
liste = [ "A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"]
letterSize=75*g.prop[2] #Taille de chaque lettre dans chaque bouton composant le clavier
touchesParLigne = 10 #Nombre de touches par ligne
touches = [] #Liste des touches

word = ''

buttons = []

buttonSize=150*g.prop[2] #Taille de chaque bouton

orderedDifficulty = ['Novice','Amateur','Extrême'] #Liste des difficultés
#Intervalles de lettres associés à chaque difficulté:
difficultyDict = {
    "Extrême": [2,4],
    "Amateur": [5,8],
    "Novice": [9,'∞']
}

Nbrdemottrouve()
if g.plaqueTournante:
    f=open(path+g.translate(textChoiceButtonsDescription[0][0]), "r")
    words = f.read().replace('\n','').split(',')
    f.close()

    level = randint(0,len(orderedDifficulty)-1)

    difficulty(level)
else:
    TextFileChoice()

g.fenetre.bind('<Return>', getInput)