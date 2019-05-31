# -*- coding: utf-8 -*-
import io
import sys
import random
import os

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    back = '.'
    if relative_path[:3] == "../":
        relative_path = relative_path[3:]
        back = '..'
    # PyInstaller creates a temp folder and stores path in _MEIPASS
    base_path = getattr(sys, '_MEIPASS', os.path.abspath(back))
    return os.path.join(base_path, relative_path)

sys.path.insert(0, resource_path('steganography/'))
from lire import getKey

def Cesar(message, key, decode=0):
    message = message.lower() #On met tous les caractères en minuscule
    longueur = len(message)
    s = []
    for i in range(longueur): #Pour chaque lettre:

        if (ord(message[i])<97 or ord(message[i])>122): #Si le caractère étudiée n'est pas dans l'alphabet:
            s.append(message[i]) #On l'écrit tel quel dans le résultat du décodage
            continue #On passe à la prochaine lettre
        else:

            if decode == 1:
                tmp = ord(message[i]) - key[i%len(key)] #On décale la lettre vers la gauche
            else:
                tmp = ord(message[i]) + key[i%len(key)] #On décale la lettre vers la droite

        if tmp>122: #Quand la lettre dépasse de l'alphabet (vers la droite)
            tmp = tmp-26 #-26=-97+123 <=> On place la lettre à l'autre extrémite de l'alphabet
        elif tmp<97: #Quand la lettre dépasse de l'alphabet (vers la guache)
            tmp = tmp+26 #26=122-96 <=> On place la lettre à l'autre extrémite de l'alphabet
        s.append(chr(tmp))

    return "".join(s) #On transforme la liste s en string

path = resource_path('steganography/')

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import matplotlib

from math import pi, ceil

from collections import OrderedDict

import numpy as np

from tkinter import *
import  tkinter as Tk
from PIL import Image, ImageTk

fenetre = Tk.Tk()
#On initialise la fenêtre
tmpScreenWidth = int(2*fenetre.winfo_screenwidth()/3)
screeny = [tmpScreenWidth, tmpScreenWidth*(720/1280)] #Taille de la fenêtre

backgroundColor = '#333'
graphColor = "silver"
insideGraphColor = "b"

#On défini le canvas
w = Tk.Canvas(fenetre,
            width=screeny[0],
            height=screeny[1],
            background=backgroundColor,
            highlightthickness=0,
            borderwidth=0)
#On place le canvas
w.grid(row=0,column=0)

#On défini les rapports de proportionnalité pour passer d'une résolution de 1280*720 à celle de l'utilisateur
prop = [screeny[0]/1280, screeny[1]/720, (screeny[0]*screeny[1])/(1280*720)]

statsByGame = OrderedDict()
statsByGame["Geometry Accuracy"] = ["GAspeedRecord","GAaverageDestroyedPlatforms","GAgameNumber"]
statsByGame["PhotoQuiz"] = ["PHthemes","PHvictories","PHaverageTime"]
statsByGame["Pendu"] = ["PEdifficulty","PEvictories","PEdefeats","PEaverageTime"]

length = 100
#['mission', 'Description', 'Variables']
failureQuotes = ["C'est dur d'échouer, mais c'est pire de n'avoir jamais essayé de réussir. Theodore Roosevelt",
                "Le succès c'est d'aller d'échec en échec sans perdre son enthousiasme. Churchill",
                "L'échec est la mère du succès",
                "L'échec est l'épice qui donne sa saveur au succès. Truman Capote",
                "Mériter le succès plutôt qu'y parvenir. Pearson, Lest B",
                "Un échec est un succès si on en retient quelque chose. Malcolm Forbes"]
successQuotes = ["La motivation est source de succès",
                "Tout simplement inarrêtable !",
                "Vaincre n'est rien, il faut profiter du succès. Napoléon Bonaparte",
                "Le succès, c'est l'échec de l'échec. Delphine Lamotte",
                "Le succès fut toujours un enfant de l'audace. Prosper Crébillon",
                "Le succès n'est pas un but mais un moyen de viser plus haut. Pierre de Coubertin"]

def missionsSetup():
    global failureQuotes, successQuotes, missions
    for i in range(len(failureQuotes)):
        failureQuotes[i] = translate(failureQuotes[i])
    for i in range(len(successQuotes)):
        successQuotes[i] = translate(failureQuotes[i])

#Valeurs à atteindre dans les missions:
missionsValues = [0,0,0,0,0,0,0,0,100]
missions = [["translate('Première partie')", "translate('En espérant que ce ne soit pas la dernière !')",
               'GAgameNumber>0 or PHvictories>0 or PHdefeats>0 or PEvictories>0 or PEdefeats>0',
               'first.png','Global', "str('completed')"],

               ["translate('Jouer et gagner ')+str(missionNumber)+translate(' partie(s) sur les trois jeux')", 'random.choice(successQuotes)',
               'GAgameNumber>=missionNumber and PHvictories>=missionNumber and PEvictories>=missionNumber', 'victory.png', 'Global', 'missionsNumbers[i]+25'],

               ["translate('Gagner ')+str(missionNumber)+translate(' partie(s) sur le jeu du Pendu')", 'random.choice(successQuotes)',
               'PEvictories>=missionNumber', 'victory.png', 'Pendu', 'missionsNumbers[i]+25'],

               ["translate('Gagner ')+str(missionNumber)+translate(' partie(s) sur PhotoQuiz')", 'random.choice(successQuotes)',
               'PHvictories>=missionNumber', 'victory.png', 'PhotoQuiz', 'missionsNumbers[i]+25'],

               ["translate('Jouer et perdre ')+str(missionNumber)+translate(' partie(s) sur les trois jeux')", 'random.choice(failureQuotes)',
               'GAgameNumber>=missionNumber and PHdefeats>=missionNumber and PEdefeats>=missionNumber', 'defeat.png', 'Global', 'missionsNumbers[i]+25'],

               ["translate('Perdre ')+str(missionNumber)+translate(' partie(s) sur le jeu du Pendu')", 'random.choice(failureQuotes)',
               'PEdefeats>=missionNumber', 'defeat.png', 'Pendu', 'missionsNumbers[i]+25'],

               ["translate('Perdre ')+str(missionNumber)+translate(' partie(s) sur PhotoQuiz')", 'random.choice(failureQuotes)',
               'PHdefeats>=missionNumber', 'defeat.png', 'PhotoQuiz', 'missionsNumbers[i]+25'],

               ["translate('Jouer ')+str(missionNumber)+translate(' partie(s) sur Geometry Accuracy')", 'random.choice(successQuotes)',
               'GAgameNumber>=missionNumber', 'victory.png', 'Geometry Accuracy', 'missionsNumbers[i]+25'],

               ["translate('Reach ')+str(missionNumber)+'% '+translate('de vitesse sur Geometry Accuracy')", 'random.choice(successQuotes)',
               'GAspeedRecord*100>=missionNumber', 'level.png', 'Geometry Accuracy', 'missionsNumbers[i]+25']
               ]
def readCsv():
    global lines,header
    try:
        fichier=io.open(resource_path("../input/stats.csv"), 'r', encoding='utf8')
    except:

        lines = [['Profil', 'gamePlayed', 'GAspeedRecord',
                  'GAaverageDestroyedPlatforms', 'GAgameNumber', 'PHthemes',
                  'PHvictories', 'PHdefeats', 'PHaverageTime', 'PEdifficulty',
                  'PEvictories', 'PEdefeats', 'PEaverageTime', 'PEpersonal',
                  'Mot de passe', 'langage', 'completedMissions'],

                 ['Maximum', ['Pendu', 'Geometry Accuracy', 'PhotoQuiz'],
                  'max', 'moy/max', 'max',
                 ['cook','space','animals','technology','home furniture','games'],
                  'max', 'min', 'moy/min', ['0', '1', '2'], 'max', 'min',
                  'moy/min', 'None', 'None', 'None'], 'None', 'None']
        writeCsv()
        fichier=io.open(resource_path("../input/stats.csv"), 'r', encoding='utf8')

    lines=fichier.readlines()
    fichier.close()

    for i in range(len(lines)):
        lines[i] = lines[i].replace('\n','')
        lines[i] = lines[i].replace('\r','')
        lines[i] = lines[i].split(';')
        for j in range(len(lines[i])):
            lines[i][j] = lines[i][j].split(",")
            if (len(lines[i][j]) == 1):
                lines[i][j] = lines[i][j][0]

    header = lines[0]

def writeCsv():
    global lines
    fichier=io.open(resource_path("../input/stats.csv"), 'w', encoding='utf8')
    for i in range(len(lines)):
        toWrite = ""
        for j in range(len(lines[i])):
            varToWrite = ""
            if isinstance(lines[i][j], (list,)):
                for k in range(len(lines[i][j])):
                    varToWrite = varToWrite + str(lines[i][j][k])
                    if k < len(lines[i][j])-1:
                        varToWrite = varToWrite+','
            else:
                varToWrite = str(lines[i][j])
            if j == len(lines[i])-1:
                toWrite = toWrite + varToWrite
            else:
                toWrite = toWrite + varToWrite + ";"

        if i < len(lines)-1:
            toWrite = toWrite + "\n"

        fichier.write(toWrite)

    fichier.close()

missionButtons = []
missionImage = None

def missionClear():
    global missionButtons, missionImage, missionsToShow

    for i in range(len(missionButtons)):
        missionButtons[i].destroy()
    missionButtons.clear()
    if len(missionsToShow) != 0:
        showMission(missionsToShow[0][0],missionsToShow[0][1])
        missionsToShow.pop(0)
    else:
        verifyMissions() #Si le joueur a par exemple passé les 100% et 125% de vitesse en une partie,
                         #on doit relancer la vérification pour prendre en compte 2 missions complétées.

resolution = 16 #La translation progressive se fait par tranche de 16 milisecondes
animationTime = 1200 #La translation dure 1 secondes
waitTime = 7000 #Temps de pause

def Translation(item, time, distVector, initialCoords, reverse=False, totalIterations=None, currentIterations=None, somme=None):

    if totalIterations is None:
        totalIterations=int(time/resolution)
        currentIterations=1
        somme = initialCoords

    try:
        somme[0]=float(somme[0])+distVector[0]/(time)*resolution
        somme[1]=float(somme[1])+distVector[1]/(time)*resolution
        item.place(x=somme[0],y=somme[1])
    except Exception as e: #Si l'objet à translater a été supprimé, on stoppe la fonction
        return

    if (currentIterations != totalIterations):
        currentIterations+=1
        fenetre.after(resolution, lambda item_=item,time_=time,distVector_=distVector, reverse_=reverse, totalIterations_=totalIterations,currentIterations_=currentIterations, somme_=somme: Translation(item_,time_,distVector_, None, reverse, totalIterations_,currentIterations_,somme_) )
    elif reverse is True:
        reverse = False
        distVector[0] = -distVector[0]
        distVector[1] = -distVector[1]
        initialCoords = somme
        fenetre.after(waitTime, lambda item_=item, time_=time, distVector_=distVector, reverse_=reverse, totalIterations_=None, currentIterations_=None, somme_=None: Translation(item_,time_,distVector_, initialCoords, reverse, totalIterations_,currentIterations_,somme_) )
    else:
        missionClear()

def showMission(textToShow, imgToShow):

    missionButtons.append(Button(w, text=textToShow, command = lambda direction='profiles': missionClear(), anchor = CENTER, font=("Courier",int(12*prop[2])),wraplengt=2*buttonSize[0]))
    missionButtons[len(missionButtons)-1].configure(fg='white', background='#2f3542', activebackground = '#4CAF50', relief = RIDGE, justify='center')
    missionButtons[len(missionButtons)-1].place(x=0, y=0, width=2*buttonSize[0], height=2*buttonSize[1])
    Translation(missionButtons[len(missionButtons)-1],animationTime, [-19/8*buttonSize[0], 0], [screeny[0]+2/8*buttonSize[0],screeny[1]-7/2*buttonSize[1]], True)

    img = Image.open(resource_path('questsIcons/')+imgToShow)
    width, height = img.size

    imgHeight = 2*buttonSize[1]
    newSize = [int(width*imgHeight/height),int(imgHeight)]
    if [width,height] != newSize:
        try:
            img = img.resize(newSize, Image.ANTIALIAS)
            img.save(resource_path('questsIcons/')+imgToShow,"PNG", quality=100)

        except IOError:
            print("Impossible de redimensionner l'image "+imgToShow+" !")
            exit()
    photo = ImageTk.PhotoImage(img)
    missionButtons.append( Label(image=photo, borderwidth=0, bg='#2f3542') )
    missionButtons[len(missionButtons)-1].image = photo #On garde une référence de l'image
    missionButtons[len(missionButtons)-1].place(x=screeny[0]+2/8*buttonSize[0], y=screeny[1]-7/2*buttonSize[1])
    Translation(missionButtons[len(missionButtons)-1],animationTime, [-19/8*buttonSize[0], 0], [screeny[0],screeny[1]-7/2*buttonSize[1]], True)

def profileVar(var,newValue = None,write = False, shouldVerifyMission = True):
    global chosenProfile,lines,header,missionButtons,missionImage
    readCsv()
    if newValue is not None:

        lines[chosenProfile+2][header.index(var)] = newValue

        if write:
            writeCsv()
            if shouldVerifyMission:
                verifyMissions()
    else:
        return lines[chosenProfile+2][header.index(var)]

missionsToShow = []
def verifyMissions():
    global profile, missionsToShow, missionsNumbers, lines

    readCsv()
    GAgameNumber = lines[chosenProfile+2][header.index('GAgameNumber')]
    PHvictories = lines[chosenProfile+2][header.index('PHvictories')]
    PHdefeats = lines[chosenProfile+2][header.index('PHdefeats')]
    PEvictories = lines[chosenProfile+2][header.index('PEvictories')]
    PEdefeats = lines[chosenProfile+2][header.index('PEdefeats')]
    GAspeedRecord = lines[chosenProfile+2][header.index('GAspeedRecord')]
    allStats = [GAgameNumber,PHvictories,PHdefeats,PEvictories,PEdefeats,GAspeedRecord]
    for i in range(len(allStats)):
        if allStats[i] != 'None':
            allStats[i]=float(allStats[i])
        else:
            allStats[i]=0
    GAgameNumber = allStats[0]
    PHvictories = allStats[1]
    PHdefeats = allStats[2]
    PEvictories = allStats[3]
    PEdefeats = allStats[4]
    GAspeedRecord = allStats[5]

    missionsNumbers = lines[chosenProfile+2][header.index('completedMissions')]

    changed = False
    for i in range(len(missions)):
        missionNumber = missionsNumbers[i]
        if missionNumber != 'completed':
            missionNumber = int(missionNumber)
            missionsNumbers[i] = missionNumber
            if missionNumber == 0:
                missionNumber = 1

            if eval(missions[i][2]):
                changed = True

                try: #Si le titre est "Première partie", la fonction eval() renvoit une erreur. On gère donc l'exception:
                    missionsToShow.append( [ eval(missions[i][0])+'\n'+eval(missions[i][1]),missions[i][3] ] )
                except:
                    missionsToShow.append( [ missions[i][0]+'\n'+missions[i][1],missions[i][3] ] )

                missionsNumbers[i] = eval(missions[i][5])

    if changed:
        profileVar('completedMissions',missionsNumbers,True,False)
        showMission(missionsToShow[0][0],missionsToShow[0][1])
        missionsToShow.pop(0)

errorSet = None
def backToHub(direction = 'gameChoice'):
    global plaqueTournante, title, profileName, errorSet
    errorSet = False

    try:
        w.delete(profileName)
        profileName = None
    except:
        pass

    for i in range(len(labels)):
        labels[i].destroy()
    labels.clear()

    for i in range(len(buttons)):
        buttons[i].destroy()
    buttons.clear()

    for i in range(len(entries)):
        entries[i].destroy()
    entries.clear()

    if title is None:
        title = w.create_text( (screeny[0]-(titleSize-7*prop[2])*len(titleContent))/2, titleSize*1.5, text=titleContent, anchor = NW, font=("Courier",int(titleSize) ), fill='white')

    if direction == 'profiles':
        drawProfile( readGeneralStats() )
        fenetre.mainloop()
    elif direction == 'gameChoice':
        gameChoice()
    else:
        launchGame( 'Plaque Tournante' )

def readGeneralStats():
    readCsv()

    maximum = lines[1]

    del lines[:2]

    if len(lines) >=1:

        profiles = []
        for i in range(len(lines)):
            profiles.append([lines[i][ header.index('Profil') ]])

        maxValues = []
        gameIndex = 0
        for game in statsByGame.keys():
            for var in statsByGame[game]:
                index = header.index(var)

                if isinstance(maximum[index], (list,)): #Si c'est une liste

                    maxValues.append( len(maximum[index]) )
                    coefficient = length/maxValues[len(maxValues)-1]

                    for i in range(len(profiles)):
                        if lines[i][index]!='None':
                            profiles[i].append( len(lines[i][index])*coefficient )
                        else:
                            profiles[i].append( 0 )

                else:

                    check = maximum[index].split('/')

                    if (check[0] == "moy"):
                        for i in range(len(lines)):
                            if (lines[i][index] != 'None'):
                                try:
                                    #On vérifie si c'est un float car python gère mal la longueur des string avec des points, e.g: "5.52"
                                    moy = float(lines[i][index])
                                except:
                                    sum=0
                                    for j in range(len(lines[i][index])):
                                        sum += float(lines[i][index][j])
                                    moy = sum/len(lines[i][index])

                                lines[i][index] = moy

                            else:
                                lines[i][index] = 'None'

                        maximum[index] = check[1]


                    values = []
                    for i in range(len(lines)):
                        if (lines[i][index] != 'None'):
                            values.append(float(lines[i][index]))

                    if (maximum[index] == "max"):

                        try:
                            maxValues.append(max(values))
                            coefficient = length/maxValues[len(maxValues)-1]
                        except: #Toutes les statistiques pour cette variable sont à 'None', il n'y a donc pas de valeur maximale
                            pass

                        for i in range(len(profiles)):
                            if lines[i][index]!= "None":
                                profiles[i].append( float(lines[i][index])*coefficient )

                            else:
                                profiles[i].append( 0 )


                    else: #if (maximum[index] == "min"):

                        try:
                            maxValues.append(min(values))
                            coefficient = length/maxValues[len(maxValues)-1]
                        except: #Toutes les statistiques pour cette variable sont à 'None', il n'y a donc pas de valeur minimale
                            pass


                        for i in range(len(profiles)):
                            if lines[i][index]!= "None":
                                profiles[i].append( float(float(lines[i][index])*coefficient/length) )

                            else:
                                profiles[i].append( 0 )

            for i in range(len(profiles)):

                listToSum = profiles[i][1+gameIndex:]

                sum = 0
                for j in range(len(listToSum)):
                    sum += float(listToSum[j])
                moy = sum/len(statsByGame[game])
                del profiles[i][1+gameIndex:]
                profiles[i].append(moy)

            gameIndex +=1

        return profiles

    else:

        return []

COLOR = 'white'
matplotlib.rcParams['text.color'] = COLOR
matplotlib.rcParams['axes.labelcolor'] = COLOR
matplotlib.rcParams['xtick.color'] = COLOR
matplotlib.rcParams['ytick.color'] = COLOR

titleContent = 'NeuroFit'
titleSize = 25*prop[2]
title = w.create_text( (screeny[0]-(titleSize-7*prop[2])*len(titleContent))/2, titleSize*1.5, text=titleContent, anchor = NW, font=("Courier",int(titleSize) ), fill='white')

canvasList = []

def drawChart(name, values,coords):
    global canvasList, clientDPI, dpiGraphSize, graphSize
    labels = []
    for game in statsByGame.keys():
        if game == 'PhotoQuiz':
            game = 'Photo'
        labels.append(game)
    N = len(labels)
    x_as = [n / float(N) * 2 * pi for n in range(N)]
    # Le graphique va être circulaire
    # Donc on ajoute la première valeur de chaque liste à la fin de celle-ci
    values += values[:1]
    x_as += x_as[:1]

    # On définit la couleur des axes
    plt.rc('axes', linewidth=0.5, edgecolor="#888888")
    # Création d'un graphique aux coordonnées polaires
    ax = plt.subplot(1,1,1, polar=True)
    ax.set_facecolor(graphColor)
    # On défini un sens de rotation horaire:
    ax.set_theta_offset(pi / 2)
    ax.set_theta_direction(-1)

    # On définit la position y des labels
    ax.set_rlabel_position(0)


    # On définit la couleur et le style de la grille
    ax.xaxis.grid(True, color="#888888", linestyle='solid', linewidth=0.5)
    ax.yaxis.grid(True, color="#888888", linestyle='solid', linewidth=0.5)

    # On définit les paliers en x
	# e.g: x_as = [Pi/3, 2*Pi/3, 3*Pi/3]
	#Les paliers d'angle theta seront [Pi/3, 2*Pi/3]
    plt.xticks(x_as[:-1], [])

    # Ont définit les paliers en y
    plt.yticks([20, 40, 60, 80, 100], ["20", "40", "60", "80", "100"])

    # Données du graphique
    ax.plot(x_as, values, color=insideGraphColor, alpha=0.8, linewidth=1, linestyle='solid', zorder=3)

    # On remplit le graphique
    ax.fill(x_as, values, color=insideGraphColor, alpha=0.8)

    # On définit les limites des axes
    plt.ylim(0, 100)


    # On affiche les paliers en y pour être
	# certain qu'ils s'intègrent proprement
    for i in range(N):
        angle_rad = i / float(N) * 2 * pi
        if angle_rad == 0:
            ha, distance_ax = "center", 20
        elif 0 < angle_rad < pi:
            ha, distance_ax = "left", 2
        elif angle_rad == pi:
            ha, distance_ax = "center", 2
        else:
            ha, distance_ax = "right", 2

        ax.text(angle_rad, 100 + distance_ax, labels[i], size=7, horizontalalignment=ha, verticalalignment="center")

    # On montre le graphique polaire
    fig = plt.figure(num=1, dpi=clientDPI)
    fig.set_facecolor("none")

    fig.set_figheight(dpiGraphSize[0])
    fig.set_figwidth(dpiGraphSize[1])

	#On transforme la figure en canvas de Tkinter
    canvas = FigureCanvasTkAgg(fig, master=fenetre)
    canvas.get_tk_widget().configure(background=backgroundColor,highlightbackground=backgroundColor)
    plot_widget = canvas.get_tk_widget()
    plot_widget.place(x=coords[0],y=coords[1])
	#On ajoute le canvas à une liste pour le supprimer plus tard
    canvasList.append(canvas)
	#On ferme la figure pour passer au prochain graphique
    plt.close(fig)

profilParLigne = 3
graphSize=[240*prop[0],225*prop[1]]
buttonSize=[graphSize[0],30*prop[1]] #Taille de chaque bouton
clientDPI = 96
dpiGraphSize=[graphSize[0]/clientDPI,graphSize[1]/clientDPI]

profilWidth = buttonSize[0] #Largeur totale du profil
profilHeight = buttonSize[1]+graphSize[1] #Longueur totale du profil

profilSeparator = 10

buttons = []
entryWidth = int(50*prop[0])
labelTexts = ["Pseudonyme", "Mot de passe", "Confirmez le mot de passe"]
labelHeight = int(4*prop[1])
separatorLabelText = 30*prop[0]

longestLength = 0
for index in range(len(labelTexts)):
    if len(labelTexts[index]) > longestLength:
        longestLength = len(labelTexts[index])

labelWidth = int( (longestLength*5)*prop[0] +separatorLabelText )

entries = []
labels = []
lastIndex = None
yOrigin = None

registering = False
def createProfile():
    global registering, yOrigin, lastIndex, labels, buttons, canvas, entryWidth, entries

    for i in range(len(buttons)):
        buttons[i].destroy()
    buttons.clear()

    for i in range(len(canvasList)):
        canvasList[i].get_tk_widget().destroy()
    canvasList.clear()

    entries = []
    labels = []

    yOrigin = (screeny[1] - len(labelTexts)*labelHeight - 400*prop[1])/2

    xCoords = [(screeny[0]-entryWidth-labelWidth +separatorLabelText)/2,
               (screeny[0]-entryWidth-labelWidth -separatorLabelText)/2 -labelWidth] # [x entries coords , x labels coords]

    buttons.append(Button(w, text="Retour", command = lambda direction='profiles': backToHub(direction), anchor = CENTER, font=("Courier",int(12*prop[2]))))
    buttons[len(buttons)-1].configure(fg='white', background='#111', activebackground = '#4CAF50', relief = RIDGE, justify='center')
    buttons[len(buttons)-1].place(x=screeny[0]-5/8*buttonSize[0], y=screeny[1]-3/2*buttonSize[1], width=buttonSize[0]/2, height=buttonSize[1])

    for i in range(len(labelTexts)):

        if labelTexts[i] == "Mot de passe" or labelTexts[i] == "Confirmez le mot de passe":
            entries.append(Entry(fenetre, width=entryWidth, show="*"))
        else:
            entries.append(Entry(fenetre, width=entryWidth))

        entries[len(entries)-1].place(x = xCoords[0] , y=yOrigin + labelHeight*i*15)

        labels.append( Label(fenetre, text=labelTexts[i], height=labelHeight, bg=backgroundColor, fg="white") )
        labels[len(labels)-1].place(x = xCoords[1], y=yOrigin + labelHeight*(i*15-5) )
        lastIndex = i

    entries[0].focus()
    lastIndex+=1

    registering = True
    buttons.append(Button(w, text="Créer un nouveau profil", command = lambda: saveProfile(), anchor = CENTER, font=("Courier",int(12*prop[2]))))
    buttons[len(buttons)-1].configure(fg='white', background='#111', activebackground = '#4CAF50', relief = RIDGE, justify='center')
    buttons[len(buttons)-1].place(x=(screeny[0]-buttonSize[0])/2, y=yOrigin + labelHeight*lastIndex*15, width=buttonSize[0], height=buttonSize[1])

    lastIndex +=1

longestLengthProfile = 0
for index in range(len(labelTexts)):
    if len(labelTexts[index]) > longestLengthProfile:
        longestLengthProfile = len(labelTexts[index])

labelWidthProfile = int( (longestLengthProfile*5)*prop[0] +separatorLabelText )
chosenLanguage = 'français'
def login():
    global profileName, chosenLanguage, logging, errorSet, lines, chosenProfile, lastIndex

    fichier=io.open(resource_path("../input/stats.csv"), 'r', encoding='utf8')
    lines=fichier.readlines()
    fichier.close()

    header = lines[0]
    header = header.replace('\n','')
    header = header.replace('\r','')
    header = header.split(';')

    del lines[:2]

    for i in range(len(lines)):
        lines[i] = lines[i].replace('\n','')
        lines[i] = lines[i].replace('\r','')
        lines[i] = lines[i].split(';')
        for j in range(len(lines[i])):
            lines[i][j] = lines[i][j].split(",")
            if (len(lines[i][j]) == 1):
                lines[i][j] = lines[i][j][0]

    password = entries[0].get()
    if password.lower() != Cesar(lines[chosenProfile][header.index('Mot de passe')], getKey(path,'landscape','key'), 1):
        if errorSet:
            labels[len(labels)-1].config(text=errorsDict["WrongPassword"])
        else:
            errorSet = True
            labels.append( Label(fenetre, text=errorsDict["WrongPassword"], height=labelHeight, bg=backgroundColor, fg='#ff6b6b') )
            labels[len(labels)-1].place(x = (screeny[0]-len(errorsDict["WrongPassword"])*6)/2, y=yOrigin + labelHeight*(lastIndex*15-5) )
        return

    logging = False

    w.delete(profileName)
    profileName = None

    for i in range(len(labels)):
        labels[i].destroy()
    labels.clear()

    for i in range(len(buttons)):
        buttons[i].destroy()
    buttons.clear()

    for i in range(len(entries)):
        entries[i].destroy()
    entries.clear()

    chosenLanguage = lines[chosenProfile][header.index('langage')]

    if (chosenLanguage == 'None'):
        chosenLanguage = 'français'

    missionsSetup() #On traduit les missions après avoir choisi le langage
    gameChoice()

logging = False
chosenProfile = None
profileName = None
def choseProfile(profileIndex):
    global profileName, logging, errorSet, chosenProfile, yOrigin, lastIndex, labels, buttons, canvas, entryWidth, entries

    chosenProfile = profileIndex

    for i in range(len(buttons)):
        buttons[i].destroy()
    buttons.clear()

    buttons.append(Button(w, text="Retour", command = lambda direction='profiles': backToHub(direction), anchor = CENTER, font=("Courier",int(12*prop[2]))))
    buttons[len(buttons)-1].configure(fg='white', background='#111', activebackground = '#4CAF50', relief = RIDGE, justify='center')
    buttons[len(buttons)-1].place(x=screeny[0]-5/8*buttonSize[0], y=screeny[1]-3/2*buttonSize[1], width=buttonSize[0]/2, height=buttonSize[1])

    for i in range(len(canvasList)):
        canvasList[i].get_tk_widget().destroy()
    canvasList.clear()

    entries = []
    labels = []
    nameToShow=profileVar('Profil')
    profileName = w.create_text( (screeny[0]-(titleSize-7*prop[2])*len(nameToShow))/2, (screeny[1]-525*prop[1])/2, text=nameToShow, anchor = NW, font=("Courier",int(titleSize) ), fill='white')

    yOrigin = (screeny[1] - labelHeight - 400*prop[1])/2

    xCoords = [(screeny[0]-entryWidth-labelWidthProfile +separatorLabelText)/2,
               (screeny[0]-entryWidth-labelWidthProfile -separatorLabelText)/2 -labelWidthProfile] # [x entries coords , x labels coords]

    entries.append(Entry(fenetre, width=entryWidth, show="*"))
    entries[len(entries)-1].place(x = xCoords[0] , y=yOrigin + labelHeight*0*15)

    labels.append( Label(fenetre, text=labelTexts[1], height=labelHeight, bg=backgroundColor, fg="white") )
    labels[len(labels)-1].place(x = xCoords[1], y=yOrigin + labelHeight*(0*15-5) )

    entries[0].focus()
    lastIndex = 1

    errorSet = False

    logging = True
    buttons.append(Button(w, text="Se connecter", command = lambda: login(), anchor = CENTER, font=("Courier",int(12*prop[2]))))
    buttons[len(buttons)-1].configure(fg='white', background='#111', activebackground = '#4CAF50', relief = RIDGE, justify='center')
    buttons[len(buttons)-1].place(x=(screeny[0]-buttonSize[0])/2, y=yOrigin + labelHeight*lastIndex*15, width=buttonSize[0], height=buttonSize[1])

    lastIndex +=1

alreadyImported = []
lastGame = None
plaqueTournante = False

def launchGame(game):
    global plaqueTournante, lastGame, buttons, title, alreadyImported

    for i in range(len(buttons)):
        buttons[i].destroy()
    buttons.clear()
    w.delete(title)
    title = None

    if game == 'Plaque Tournante':
        plaqueTournante = True
        gameList = ['PhotoQuiz','Pendu','GeometryAccuracy']
        if lastGame is not None:
            gameList.remove(lastGame)
        game = random.choice(gameList)
    else:
        plaqueTournante = False

    alreadyPlayedGameList = profileVar('gamePlayed')
    if alreadyPlayedGameList == 'None':
        alreadyPlayedGameList = []
    else:
        if isinstance(alreadyPlayedGameList, (list,)):
            pass
        else:
            alreadyPlayedGameList = alreadyPlayedGameList.split(',')
    if game not in alreadyPlayedGameList:
        alreadyPlayedGameList.append(game)
    profileVar('gamePlayed',alreadyPlayedGameList,True)

    game=game.replace(' ','')
    lastGame = game
    if (game in alreadyImported):
        del sys.modules[game]
    else:
        alreadyImported.append(game)
        sys.path.insert(0, resource_path('../'+game+'/'))
    new_module = __import__(game) #On import le module 'game'

gameButtonText = [  'Geometry Accuracy',
                    'PhotoQuiz',
                    'Pendu',
                    'Plaque Tournante'
]
gameButtonSize = [  [370,500],
                    [250,250],
                    [250,250],
                    [300,500]
]
for i in range(len(gameButtonSize)):
    for j in range(len(gameButtonSize[i])):
        gameButtonSize[i][j]= int( gameButtonSize[i][j] * prop[j] )
gameButtonColor = [ '#55efc4',
                    '#81ecec',
                    '#74b9ff',
                    '#a29bfe'
]

buttonBlocksSeparator = 110
xOrigin = gameButtonSize[0][0]+gameButtonSize[1][0]+buttonBlocksSeparator+gameButtonSize[3][0]
xOrigin = (screeny[0]-xOrigin)/2
gameButtonSeparator = [[xOrigin,110],
                      [gameButtonSize[0][0],0],
                      [0,gameButtonSize[1][1]],
                      [gameButtonSize[2][0]+buttonBlocksSeparator,-gameButtonSize[2][1]]
]

try:
    fichier=io.open(resource_path("translate.csv"), 'r', encoding='utf8')
except:
    fichier=io.open(resource_path("translate.csv"), 'w', encoding='utf8')
    fichier.write('english;français\n')
    fichier.close()
    fichier=io.open(resource_path("translate.csv"), 'r', encoding='utf8')

translateList=fichier.readlines()
fichier.close()

for i in range(len(translateList)):
    translateList[i] = translateList[i].replace('\n','')
    translateList[i] = translateList[i].split(';')
languages = translateList[0]

allLanguages = OrderedDict()
allLanguages["english"] = 0
allLanguages["français"] = 1

def translate(toTranslate):
    global translateList, chosenLanguage
    found = False
    for i in range(len(translateList)):
        for j in range(len(translateList[i])):
            if translateList[i][j]==toTranslate:
                found = True
                indexes = [i,j]
                break
    if found == True:

        if indexes[1]!=allLanguages[chosenLanguage]:
            translated = translateList[indexes[0]][allLanguages[chosenLanguage]].replace('\r','')
            if translated != "None":
                return translated
            else:
                return toTranslate
        else:
            return toTranslate
    else:
        translateList.append([toTranslate,"None"])
        fichier=io.open(resource_path("translate.csv"), 'a', encoding='utf8')
        fichier.write(toTranslate+ ';None\n')
        fichier.close()
        return toTranslate

def choseLanguage(language):
    global chosenLanguage
    if chosenLanguage != language:
        chosenLanguage = language
        missionsSetup()
        profileVar('langage',chosenLanguage,True)
        buttons[len(buttons)-1].configure(text=translate('Back'))

def langage():
    for i in range(len(buttons)):
        buttons[i].destroy()
    buttons.clear()

    index = 0
    for language in allLanguages.keys():

        buttons.append(Button(w, text = language, command = lambda language=language: choseLanguage(language), anchor = CENTER,font=("Courier",int(12*prop[2]))))
        buttons[len(buttons)-1].configure(fg='white', background='#111', activebackground = '#4CAF50', relief = RIDGE, justify='center')
        buttons[len(buttons)-1].place(x=screeny[0]/2-buttonSize[0]*len(allLanguages)/2 +buttonSize[0]*index, y=screeny[1]/2-buttonSize[1]/2, width=buttonSize[0], height=buttonSize[1])
        index+=1

    buttons.append(Button(w, text=translate('Back'), command = lambda direction='gameChoice': backToHub(direction), anchor = CENTER, font=("Courier",int(12*prop[2]))))
    buttons[len(buttons)-1].configure(fg='white', background='#111', activebackground = '#4CAF50', relief = RIDGE, justify='center')
    buttons[len(buttons)-1].place(x=screeny[0]-6/5*buttonSize[0], y=screeny[1]-(5/2+1/8)*buttonSize[1], width=buttonSize[0]/2, height=buttonSize[1])

def importMissions():
    for i in range(len(buttons)):
        buttons[i].destroy()
    buttons.clear()

    if ('Missions' in alreadyImported):
        del sys.modules['Missions']
        import Missions
    else:
        alreadyImported.append('Missions')
        sys.path.insert(0, resource_path('../Missions/'))
        import Missions

def gameChoice():
    global buttons
    coords = list( gameButtonSeparator[0] ) #On ne prend pas la référence de la variable gameButtonSeparator[0] qui est un pointeur

    for i in range(len(gameButtonText)):
        buttons.append(Button(w, text=translate(gameButtonText[i]), command = lambda game=gameButtonText[i]: launchGame(game), anchor = CENTER, font=("Courier",int(20*prop[2]))))
        buttons[len(buttons)-1].configure(fg='white', background=gameButtonColor[i], activebackground = '#4CAF50', relief = FLAT, justify='center', wraplength=gameButtonSize[i][0]+15*prop[0])
        buttons[len(buttons)-1].place(x=coords[0], y=coords[1], width=gameButtonSize[i][0], height=gameButtonSize[i][1])

        if i < len(gameButtonText)-1:
            coords[0] += gameButtonSeparator[i+1][0]
            coords[1] += gameButtonSeparator[i+1][1]

    buttons.append(Button(w, text=translate('Language'), command = langage, anchor = CENTER, font=("Courier",int(12*prop[2]))))
    buttons[len(buttons)-1].configure(fg='white', background='#111', activebackground = '#4CAF50', relief = RIDGE, justify='center')
    buttons[len(buttons)-1].place(x=screeny[0]-6/5*buttonSize[0], y=buttonSize[1], width=buttonSize[0]/2, height=buttonSize[1])

    buttons.append(Button(w, text=translate('Missions'), command = importMissions, anchor = CENTER, font=("Courier",int(12*prop[2]))))
    buttons[len(buttons)-1].configure(fg='white', background='#111', activebackground = '#4CAF50', relief = RIDGE, justify='center')
    buttons[len(buttons)-1].place(x=screeny[0]-3/5*buttonSize[0], y=buttonSize[1], width=buttonSize[0]/2, height=buttonSize[1])

    buttons.append(Button(w, text=translate('Back'), command = lambda direction='profiles': backToHub(direction), anchor = CENTER, font=("Courier",int(12*prop[2]))))
    buttons[len(buttons)-1].configure(fg='white', background='#111', activebackground = '#4CAF50', relief = RIDGE, justify='center')
    buttons[len(buttons)-1].place(x=screeny[0]-6/5*buttonSize[0], y=screeny[1]-(5/2+1/8)*buttonSize[1], width=buttonSize[0]/2, height=buttonSize[1])

    supprButton = Button(w, text=translate('Delete account'), anchor = CENTER, font=("Courier",int(12*prop[2])))
    buttons.append(supprButton)
    buttons[len(buttons)-1].configure(fg='white', background='#111', activebackground = '#4CAF50', relief = RIDGE, justify='center', command = lambda supprButton=buttons[len(buttons)-1]: deleteProfile(supprButton))
    buttons[len(buttons)-1].place(x=screeny[0]-6/5*buttonSize[0], y=screeny[1]-3/2*buttonSize[1], width=buttonSize[0], height=buttonSize[1])

errorsDict = OrderedDict()
errorsDict["PseudoAlreadyUsed"] = "Ce pseudonyme est déjà pris"
errorsDict["PseudoTooShort"] = "Votre pseudonyme est trop court"
errorsDict["PasswordsNotMatching"] = "Les deux mots de passe ne correspondent pas"
errorsDict["PasswordTooShort"] = "Votre mot de passe est trop court"
errorsDict["WrongPassword"] = "Vous avez renseigné un mauvais mot de passe"
excludedProfileCharacters = [';',',']
sum = ""
for i in range(len(excludedProfileCharacters)):
    sum=sum+'\''+excludedProfileCharacters[i]+'\''
    if i < len(excludedProfileCharacters)-1:
        sum = sum + ", "
errorsDict["PseudoExcludedCharacters"] = "Votre pseudo ne peut contenir les caractères "+sum
errorsDict["PasswordExcludedCharacters"] = "Votre mdp ne peut contenir les caractères "+sum

def reEnable(supprButton):
    supprButton.configure(text=translate('Are you certain ?'), fg='white', background='#111', state='normal', command = lambda supprButton=supprButton: deleteProfile(supprButton, 1) )

def deleteProfile(supprButton, step = 0):
    global chosenProfile

    if step == 0:
        supprButton.configure(text=translate('Are you certain ?'), fg='white', bg='#ff6b6b', state='disabled')
        fenetre.after(1000, lambda supprButton=supprButton: reEnable(supprButton) )
    else:

        fichier=io.open(resource_path("../input/stats.csv"), 'r', encoding='utf8')
        lines=fichier.readlines()
        fichier.close()

        for i in range(len(lines)):
            lines[i] = lines[i].replace('\n','')
            lines[i] = lines[i].replace('\r','')
            lines[i] = lines[i].split(';')

        lines.pop(chosenProfile+2)

        fichier=io.open(resource_path("../input/stats.csv"), 'w', encoding='utf8')
        for i in range(len(lines)):
            toWrite = ""
            for j in range(len(lines[i])):
                if j == len(lines[i])-1:
                    toWrite = toWrite + str(lines[i][j])
                else:
                    toWrite = toWrite + str(lines[i][j]) + ";"
            if i < len(lines)-1:
                toWrite = toWrite + "\n"
            fichier.write(toWrite)
        fichier.close()

        chosenProfile = None

        backToHub('profiles')

errorSet = False
def saveProfile():
    global excludedProfileCharacters, registering, chosenProfile, yOrigin, errorSet, entries, labels, lastIndex, buttons

    pseudo = entries[labelTexts.index("Pseudonyme")].get()
    password = entries[labelTexts.index("Mot de passe")].get()
    confirmedPassword = entries[labelTexts.index("Confirmez le mot de passe")].get()
    for i in range(len(pseudo)):
        if pseudo[i] in excludedProfileCharacters:
            if errorSet:
                labels[len(labels)-1].config(text=errorsDict["PseudoExcludedCharacters"])
            else:
                errorSet = True
                labels.append( Label(fenetre, text=errorsDict["PseudoExcludedCharacters"], height=labelHeight, bg=backgroundColor, fg='#ff6b6b') )
                labels[len(labels)-1].place(x = (screeny[0]-len(errorsDict["PseudoExcludedCharacters"])*6)/2, y=yOrigin + labelHeight*(lastIndex*15-5) )
            return
    for i in range(len(password)):
        if password[i] in excludedProfileCharacters:
            if errorSet:
                labels[len(labels)-1].config(text=errorsDict["PasswordExcludedCharacters"])
            else:
                errorSet = True
                labels.append( Label(fenetre, text=errorsDict["PasswordExcludedCharacters"], height=labelHeight, bg=backgroundColor, fg='#ff6b6b') )
                labels[len(labels)-1].place(x = (screeny[0]-len(errorsDict["PasswordExcludedCharacters"])*6)/2, y=yOrigin + labelHeight*(lastIndex*15-5) )
            return
    if len(pseudo) <= 2:
        if errorSet:
            labels[len(labels)-1].config(text=errorsDict["PseudoTooShort"])
        else:
            errorSet = True
            labels.append( Label(fenetre, text=errorsDict["PseudoTooShort"], height=labelHeight, bg=backgroundColor, fg='#ff6b6b') )
            labels[len(labels)-1].place(x = (screeny[0]-len(errorsDict["PseudoTooShort"])*6)/2, y=yOrigin + labelHeight*(lastIndex*15-5) )
        return
    if len(password) <= 2:
        if errorSet:
            labels[len(labels)-1].config(text=errorsDict["PasswordTooShort"])
        else:
            errorSet = True
            labels.append( Label(fenetre, text=errorsDict["PasswordTooShort"], height=labelHeight, bg=backgroundColor, fg='#ff6b6b') )
            labels[len(labels)-1].place(x = (screeny[0]-len(errorsDict["PasswordTooShort"])*6)/2, y=yOrigin + labelHeight*(lastIndex*15-5) )
        return
    if password != confirmedPassword:
        if errorSet:
            labels[len(labels)-1].config(text=errorsDict["PasswordsNotMatching"])
        else:
            errorSet = True
            labels.append( Label(fenetre, text=errorsDict["PasswordsNotMatching"], height=labelHeight, bg=backgroundColor, fg='#ff6b6b') )
            labels[len(labels)-1].place(x = (screeny[0]-len(errorsDict["PasswordsNotMatching"])*6)/2, y=yOrigin + labelHeight*(lastIndex*15-5) )
        return

    fichier=open(resource_path("../input/stats.csv"),"r")
    lines=fichier.readlines()
    fichier.close()


    header = lines[0]
    header = header.replace('\n','')
    header = header.split(';')

    del lines[:2]

    for i in range(len(lines)):
        lines[i] = lines[i].replace('\n','')
        lines[i] = lines[i].split(';')
        for j in range(len(lines[i])):
            lines[i][j] = lines[i][j].split(",")
            if (len(lines[i][j]) == 1):
                lines[i][j] = lines[i][j][0]

    for i in range(len(lines)):

        if lines[i][header.index('Profil')] == pseudo:
            if errorSet:
                labels[len(labels)-1].configure(text=errorsDict["PseudoAlreadyUsed"])
            else:
                errorSet = True
                labels.append( Label(fenetre, text=errorsDict["PseudoAlreadyUsed"], height=labelHeight, bg=backgroundColor, fg='#ff6b6b') )
                labels[len(labels)-1].place(x = (screeny[0]-len(errorsDict["PseudoAlreadyUsed"])*6)/2, y=yOrigin + labelHeight*(lastIndex*15-5) )
            return
    registering = False
    cryptedPassword = Cesar(password, getKey(path,'landscape','key'), 0)

    fichier=io.open(resource_path("../input/stats.csv"), 'a+', encoding='utf8')
    toAdd = ""
    for i in range(len(header)):
        if header[i] == "Profil":
            toAdd = "\n"+pseudo
        elif header[i] == "Mot de passe":
            toAdd = toAdd+cryptedPassword
        elif header[i] == "completedMissions":
            varToWrite = str(missionsValues[0])
            for j in range(1,len(missions)):
                varToWrite = varToWrite+','+str(missionsValues[j])
            toAdd = toAdd+varToWrite
        else:
            toAdd = toAdd+"None"
        if i < len(header)-1:
            toAdd = toAdd +";"
    fichier.write(toAdd)

    chosenProfile = len(lines)

    for i in range(len(entries)):
        entries[i].destroy()
    for i in range(len(labels)):
        labels[i].destroy()
    for i in range(len(buttons)):
        buttons[i].destroy()
    entries.clear()
    labels.clear()
    buttons.clear()

    gameChoice()

def drawProfile(profiles):
    global buttons,clientDPI

    if len(profiles) == 0:
        lastCoords = [0,1]

    if len(profiles) < 6:

        totalLines = ceil( (len(profiles)+1)/profilParLigne)

    else:

        totalLines = ceil( len(profiles)/profilParLigne)

    for ligne in range( totalLines ):
        for colonne in range(profilParLigne):
            if (ligne*profilParLigne+colonne <= len(profiles)-1):

                index = ligne*profilParLigne+colonne

                buttonCoords = [ screeny[0]/2-profilWidth*profilParLigne/2 + (profilWidth +profilSeparator)*(index-profilParLigne*ligne)
                ,                screeny[1]/2-profilHeight*totalLines    /2 + (profilHeight+profilSeparator*4)*ligne ]

                graphCoords = [ screeny[0]/2-profilWidth*profilParLigne /2 + (profilWidth+profilSeparator)*(index-profilParLigne*ligne)
                ,  10*prop[0] + screeny[1]/2-profilHeight*totalLines    /2 + (profilHeight+profilSeparator*4)*ligne + buttonSize[1] ]

                if len(profiles[index][1:])>0:
                    drawChart(profiles[index][0], profiles[index][1:], graphCoords)

                buttons.append(Button(w, text=profiles[index][0], command = lambda index=index: choseProfile(index), anchor = CENTER, font=("Courier",int(12*prop[2]))))
                buttons[len(buttons)-1].configure(fg='white', background='#111', activebackground = '#4CAF50', relief = RIDGE, justify='center')
                buttons[len(buttons)-1].place(x=buttonCoords[0], y=buttonCoords[1], width=buttonSize[0], height=buttonSize[1])

                lastCoords = [ligne,colonne+1]

    if len(profiles) < 6:

        if lastCoords[1] >= profilParLigne:
            lastCoords[0]+=1
            lastCoords[1]=0

        index = lastCoords[0]*profilParLigne+lastCoords[1]
        buttonCoords = [ screeny[0]/2-profilWidth*profilParLigne/2 + (profilWidth +profilSeparator)*(index-profilParLigne*lastCoords[0])
        ,                screeny[1]/2-profilHeight*totalLines   /2 + (profilHeight+profilSeparator*4)*lastCoords[0] ]

        buttons.append(Button(w, text='Créer une nouvelle session', command = lambda: createProfile(), anchor = CENTER, font=("Courier",int(12*prop[2]))))
        buttons[len(buttons)-1].configure(fg='white', background='#4CAF50', activebackground = 'green', relief = RIDGE, justify='center', wraplength=buttonSize[0]+15*prop[0])
        buttons[len(buttons)-1].place(x=buttonCoords[0], y=buttonCoords[1], width=buttonSize[0], height=profilHeight)

drawProfile( readGeneralStats() )

def pressEnter(event):
    if logging:
        login()
    elif registering:
        saveProfile()

fenetre.bind('<Return>', pressEnter)

fenetre.mainloop()
