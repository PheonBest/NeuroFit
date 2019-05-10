import sys
g = sys.modules['__main__']
# On importe les variables globales du fichier 'Hub.py' qui sont des attributs du module 'Hub'

from tkinter import *
from collections import OrderedDict

buttonSize=200*g.prop[2]

#statsByGame = OrderedDict()
#statsByGame["Geometry Accuracy"] = ["GAdifficulty","GAspeedRecord","GAaverageDestroyedPlatforms","GAgameNumber"]
#statsByGame["Photo"] = ["PHdifficulty","PHvictories","PHaverageTime"]
#statsByGame["Pendu"] = ["PEdifficulty","PEvictories","PEdefeats","PEaverageTime"]

gameName = []
gameStats = []
for game in g.statsByGame.keys():
    gameName.append(game)
    gameStats.append(g.statsByGame.get( game ))


buttons = []
level=0
MissionsPricipales=[]

texts=[]

def ProfilChoice(drawButtons=True):
   global texts

   ClearText()
   fichier=open("../Missions/ListeMissions.txt")
   lines=fichier.readlines()
   fichier.close()
   for i in range(len(lines)):
        lines[i].replace('\n','')
   texts.append(g.w.create_text(640*g.prop[0],120*g.prop[1],fill="WHITE",font=("Times bold",int(12*g.prop[2])),text="Défis principaux"))

   for i in range(7):
        texts.append(g.w.create_text(640*g.prop[0],(300+i*30)*g.prop[1],fill="WHITE",font=("Times",int(24*g.prop[2])),text= lines[i]))
   if drawButtons:
        buttons.append(Button(g.w, text=g.translate('Back'), command = lambda direction='gameChoice': returnToHub(direction), anchor = CENTER, font=("Courier",int(12*g.prop[2]))))
        buttons[len(buttons)-1].configure(fg='white', background='#111', activebackground = '#4CAF50', relief = RIDGE, justify='center')
        buttons[len(buttons)-1].place(x=g.screeny[0]-6/5*240*g.prop[0], y=g.screeny[1]-(5/2+1/8)*30*g.prop[1], width=240*g.prop[0]/2, height=30*g.prop[1])

        GameMissionChoice()

def ClearText():
    global texts
    for i in range(len(texts)):
        g.w.delete(texts[i])
    texts.clear()

def GameMission(newLevel):
    global level,texts
    level = newLevel

    fichier=open("../Missions/ListeMissions.txt")
    lines=fichier.readlines()
    fichier.close()
    for i in range(len(lines)):
        lines[i].replace('\n','')
    texts.append(g.w.create_text(640*g.prop[0],300*g.prop[1],fill="WHITE",font=("Times",int(24*g.prop[2])),text= lines[0]))

    ClearText()
    texts.append(g.w.create_text(640*g.prop[0],120*g.prop[1],fill="WHITE",font=("Times bold",int(12*g.prop[2])),text="Défis "+gameName[level]))
    for i in range(len(gameStats[level])):
        stat = g.profileVar(gameStats[level][i])
        if stat == "None":
            texts.append(g.w.create_text(640*g.prop[0],(300+i*30)*g.prop[1],fill="WHITE",font=("Times",int(24*g.prop[2])),text=gameStats[level][i]))
        else:
            if isinstance(stat, (list,)):
                sum = ""
                for i in range(len(stat)):
                    sum=sum+'\''+stat[i]+'\''
                    if i < len(stat)-1:
                        sum = sum + ", "
                toShow = sum
            else:
                toShow = stat

            texts.append(g.w.create_text(640*g.prop[0],(300+i*30)*g.prop[1],fill="GREEN",font=("Times",int(24*g.prop[2])),text=gameStats[level][i]+': '+toShow))

def GameMissionChoice():
    global buttons
    for i in range(3):
        buttons.append(Button(g.w, text = gameName[i], command = lambda i=i: GameMission(i), anchor = CENTER,font=("Times bold",int(12*g.prop[2]))))
        buttons[len(buttons)-1].configure(fg='white', background='#111', activebackground = '#4CAF50', relief = RIDGE, justify='center')
        buttons[len(buttons)-1].place(x=g.screeny[0]/2-buttonSize*2 +buttonSize*i, y=g.screeny[1]/3.5-buttonSize/2, width=buttonSize*1, height=buttonSize/2.5)
    i=3
    buttons.append(Button(g.w, text = g.translate('Global'), command = lambda drawButtons=False: ProfilChoice(drawButtons), anchor = CENTER,font=("Times bold",int(12*g.prop[2]))))
    buttons[len(buttons)-1].configure(fg='white', background='#111', activebackground = '#4CAF50', relief = RIDGE, justify='center')
    buttons[len(buttons)-1].place(x=g.screeny[0]/2-buttonSize*2 +buttonSize*i, y=g.screeny[1]/3.5-buttonSize/2, width=buttonSize*1, height=buttonSize/2.5)

def returnToHub(direction = 'gameChoice'):
    ClearText()
    for i in range(len(buttons)):
        buttons[i].destroy()
    buttons.clear()

    g.backToHub(direction)

ProfilChoice()