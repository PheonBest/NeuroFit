import sys
g = sys.modules['__main__']
# On importe les variables globales du fichier 'Hub.py' qui sont des attributs du module 'Hub'

from tkinter import *
from collections import OrderedDict
from math import ceil
from PIL import Image, ImageTk

gameButtonSize=200*g.prop[2]

gameDescription = OrderedDict()
gameDescription["GAspeedRecord"] = "Record de vitesse"
gameDescription["GAaverageDestroyedPlatforms"] = "Nombre de plateformes détruites"
gameDescription["GAgameNumber"] = "Nombre de parties jouées"

gameDescription["PHthemes"] = "Thèmes joués"
gameDescription["PHvictories"] = "Nombre de parties gagnées"
gameDescription["PHdefeats"] = "Nombre de parties perdues"
gameDescription["PHaverageTime"] = "Temps joué"

gameDescription["PEdifficulty"] = "Difficultés jouées"
gameDescription["PEvictories"] = "Nombre de parties gagnées"
gameDescription["PEdefeats"] = "Nombre de parties perdues"
gameDescription["PEaverageTime"] = "Temps joué"

for key, value in gameDescription.items():
    gameDescription[key] = g.translate(value)

gameName = []
gameStats = []
for game, variablesOfGame in g.statsByGame.items():
    gameName.append(game)
    gameStats.append(variablesOfGame)
gameName.append('Global')

buttons = []
level=0
MissionsPricipales=[]

texts=[]
questsButtons = []

def changeLevel(newLevel):
    global level
    buttons[level+1].configure(background='#111')
    buttons[newLevel+1].configure(background='#4CAF50')
    level = newLevel

def GlobalMissions(drawButtons=True):
    global texts
    ClearText()

    fileToOpen = g.translate('ListeMissionsFrench.txt')
    fichier=open("../Missions/"+fileToOpen)
    lines=fichier.readlines()
    fichier.close()
    for i in range(len(lines)):
        lines[i].replace('\n','')
        texts.append(g.w.create_text(640*g.prop[0],(250+i*30)*g.prop[1],fill="WHITE",font=("Times",int(24*g.prop[2])),text=lines[i]))
    if drawButtons:
        buttons.append(Button(g.w, text=g.translate('Back'), command = lambda direction='gameChoice': returnToHub(direction), anchor = CENTER, font=("Courier",int(12*g.prop[2]))))
        buttons[len(buttons)-1].configure(fg='white', background='#111', activebackground = '#4CAF50', relief = RIDGE, justify='center')
        buttons[len(buttons)-1].place(x=g.screeny[0]-6/5*240*g.prop[0], y=g.screeny[1]-(5/2+1/8)*30*g.prop[1], width=240*g.prop[0]/2, height=30*g.prop[1])

        GameMissionChoice()
    changeLevel(len(gameName)-1)
    drawAllMissions(len(gameName)-1)

def ClearText():
    global texts
    for i in range(len(texts)):
        g.w.delete(texts[i])
    texts.clear()
    for i in range(len(questsButtons)):
        questsButtons[i].destroy()
    questsButtons.clear()

orderedDifficulty = ['Novice','Amateur','Extrême'] #Liste des difficultés du jeu du Pendu
missionsParLigne = 2
buttonSize= [2*240*g.prop[0],2*30*g.prop[1]]
buttonSeparator = 5*g.prop[2]

def GameMission(newLevel):
    global texts

    changeLevel(newLevel)
    ClearText()

    texts.append(g.w.create_text(640*g.prop[0],220*g.prop[1],fill="WHITE",font=("Times bold",int(24*g.prop[2])),text=g.translate('Défis')+' - '+g.translate(gameName[level])))
    for i in range(len(gameStats[level])):
        stat = g.profileVar(gameStats[level][i])
        if stat == "None":
            stat = '0'

        if isinstance(stat, (list,)):
            if gameStats[level][i] == 'PEdifficulty':
                for j in range(len(stat)):
                    stat[j]=orderedDifficulty[int(stat[j])]
            try: #Si c'est une liste de nombre, on calcule la somme
                somme = 0
                for j in range(len(stat)):
                    somme=somme+float(stat[j])
                toShow = str(int(somme))

                if gameDescription[gameStats[level][i]] == g.translate('Temps joué'):
                    toShow += ' '+g.translate('secondes')
            except: #Si c'est une liste de strings, on fait de la concaténation
                somme = ""
                for j in range(len(stat)):
                    somme=somme+g.translate(stat[j])
                    if j < len(stat)-1:
                        somme = somme + ", "
                toShow = somme
        else:
            toShow = stat
            if gameStats[level][i] == 'GAspeedRecord':
                toShow = str(round(float(stat)*100,1))+'%'

        texts.append(g.w.create_text(640*g.prop[0],(250+i*30)*g.prop[1],fill="WHITE",font=("Times",int(24*g.prop[2])),text=gameDescription[gameStats[level][i]]+': '+toShow))
        drawAllMissions(level)

def drawAllMissions(currentLevel):
    global questsButtons
    missionsNumbers = g.profileVar('completedMissions')
    missionSpecificToGame = []
    missionsNumbersSpecificToGame = []
    for i in range(len(g.missions)):
        if gameName[currentLevel] == g.missions[i][4]:
            missionSpecificToGame.append([g.missions[i],i])
            missionsNumbersSpecificToGame.append(missionsNumbers[i])
    totalLines = ceil(len(missionSpecificToGame)/missionsParLigne)
    for ligne in range(totalLines):
        for colonne in range(missionsParLigne):
            if (ligne*missionsParLigne+colonne <= len(missionSpecificToGame)-1):

                index = ligne*missionsParLigne+colonne
                missionNumber = missionsNumbersSpecificToGame[index]

                if missionNumber == 'completed' or missionNumber!=str( g.missionsValues[missionSpecificToGame[index][1]] ):
                    imgBackgroundColor = '#4CAF50'
                    if missionNumber != 'completed':
                        missionNumber=int(missionNumber)-25

                    else:
                        missionNumber = 1
                else:
                    imgBackgroundColor = '#ff6b6b'
                    missionNumber= g.missionsValues[missionSpecificToGame[index][1]]
                if missionNumber == 0:
                    missionNumber = 1

                imgToShow=missionSpecificToGame[index][0][3]
                img = Image.open('questsIcons/'+imgToShow)
                width, height = img.size

                imgHeight = buttonSize[1]
                newSize = [int(width*imgHeight/height),int(imgHeight)]
                if [width,height] != newSize:
                    try:
                        img = img.resize(newSize, Image.ANTIALIAS)
                        img.save('questsIcons/'+imgToShow,"PNG", quality=100)

                    except IOError:
                        print("Impossible de redimensionner l'image "+imgToShow+" !")
                        exit()

                x=(g.screeny[0]-(buttonSize[0]+newSize[0])*missionsParLigne)/2 + (buttonSize[0]++newSize[0]+buttonSeparator)*(index-missionsParLigne*ligne)
                y=120*g.prop[1]+g.screeny[1]/2 + (buttonSize[1]+buttonSeparator)*ligne

                photo = ImageTk.PhotoImage(img)
                questsButtons.append( Label(image=photo, borderwidth=0, bg=imgBackgroundColor) )
                questsButtons[len(questsButtons)-1].image = photo #On garde une référence de l'image
                questsButtons[len(questsButtons)-1].place(x=x, y=y)

                questsButtons.append(Button(g.w, text=eval(missionSpecificToGame[index][0][0].replace('translate','g.translate')), anchor=CENTER, font=("Courier",int(12*g.prop[2])), wraplengt=buttonSize[0]))
                questsButtons[len(questsButtons)-1].configure(relief = RIDGE, justify='center', fg=imgBackgroundColor, bg='#2f3542')
                questsButtons[len(questsButtons)-1].place(x=x++newSize[0], y=y, width=buttonSize[0], height=buttonSize[1])

def GameMissionChoice():
    global buttons
    for i in range(len(gameName)-1):
        buttons.append(Button(g.w, text = g.translate(gameName[i]), command = lambda i=i: GameMission(i), anchor = CENTER,font=("Times bold",int(12*g.prop[2]))))
        buttons[len(buttons)-1].configure(fg='white', background='#111', activebackground = '#4CAF50', relief = RIDGE, justify='center')
        buttons[len(buttons)-1].place(x=g.screeny[0]/2-gameButtonSize*2 +gameButtonSize*i, y=g.screeny[1]/3.5-gameButtonSize/2, width=gameButtonSize*1, height=gameButtonSize/2.5)
    i=len(gameName)-1
    buttons.append(Button(g.w, text = g.translate(gameName[i]), command = lambda drawButtons=False: GlobalMissions(drawButtons), anchor = CENTER,font=("Times bold",int(12*g.prop[2]))))
    buttons[len(buttons)-1].configure(fg='white', background='#111', activebackground = '#4CAF50', relief = RIDGE, justify='center')
    buttons[len(buttons)-1].place(x=g.screeny[0]/2-gameButtonSize*2 +gameButtonSize*i, y=g.screeny[1]/3.5-gameButtonSize/2, width=gameButtonSize*1, height=gameButtonSize/2.5)

def returnToHub(direction = 'gameChoice'):
    ClearText()
    for i in range(len(buttons)):
        buttons[i].destroy()
    buttons.clear()

    g.backToHub(direction)

GlobalMissions()