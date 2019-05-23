from tkinter import *
import math
import time
import numpy as np

fenetre = Tk() #On initialise la fenêtre

screeny = int(2*fenetre.winfo_screenwidth()/3), int(2*fenetre.winfo_screenheight()/3) #Taille de la fenêtre

#On défini le canvas
w = Canvas(fenetre,
            width=screeny[0],
            height=screeny[1],
            background='white')
#On place le canvas
w.grid(row=0,column=0)

#On défini les rapports de proportionnalité pour passer d'une résolution de 1280*720 à celle de l'utilisateur
prop = [screeny[0]/1280, screeny[1]/720, (screeny[0]*screeny[1])/(1280*720)]

playerCoords = [0.2*screeny[0], 0.45*screeny[1]]

originRadius = 8

player = w.create_oval(playerCoords[0]-originRadius,playerCoords[1]-originRadius,playerCoords[0]+originRadius,playerCoords[1]+originRadius, outline='green')

gravityConst = 9.81*30

pointsTrajectoire = 113
precision = 0.05 #Temps entre chaque point de la trajectoire
trajectoire = []

lastFrameTime=time.time()
fps = 1/60

limit = 10 #Pas de 1/10 entre chaque changement de couleur

def GradientSetStep(color,goal):
    global limit
    (r1,g1,b1) = fenetre.winfo_rgb(color)
    (r2,g2,b2) = fenetre.winfo_rgb(goal)

    return [float(r2-r1) / limit,float(g2-g1) / limit,float(b2-b1) / limit]

colors= ['#333','#333']
trajectoireColor = '#333'
iterations = 0
step = GradientSetStep(colors[0],colors[1])
trajectoireRadius = 4

def Game():
    global step, iterations, colors, trajectoireColor, gravityConst, pointsTrajectoire, precision, trajectoire, line, lastFrameTime, fps

    currentTime = time.time()
    # dt est la différence de temps en secondes
    dt = currentTime - lastFrameTime
    lastFrameTime = currentTime

    #On obtient la position du curseur par rapport à la fenêtre
    mouseCoords = [fenetre.winfo_pointerx() - fenetre.winfo_rootx(), fenetre.winfo_pointery() - fenetre.winfo_rooty()]

    #Vitesse intiiale = Distance entre l'origine et le curseur
    initialVelocity = math.sqrt((playerCoords[0]-mouseCoords[0])**2+(playerCoords[1]-mouseCoords[1])**2)
    #Angle entre l'origine et le curseur. Retourne la valeur atan(y/x) en radians
    initialAngle = math.atan2(mouseCoords[1]-playerCoords[1], mouseCoords[0]-playerCoords[0])

    newVelocity = [initialVelocity*math.cos(initialAngle),initialVelocity*math.sin(initialAngle)]

    print(newVelocity)
    if newVelocity[0] > 340:
        newVelocity[0] = 340
    elif newVelocity[0] < -100:
        newVelocity[0] = -100
    if newVelocity[1] < -460:
        newVelocity[1] = -460

    for c in range(len(trajectoire)):
        w.delete(trajectoire[c])
    trajectoire.clear()

    tmp_pos = playerCoords

    timeDelay = precision
    coords = list(playerCoords)
    coords2 =  list(playerCoords)

    modifiedVelocity = list(newVelocity)

    if iterations ==10:
        trajectoireColor = colors[1] #On s'assure que le but soit atteint
        colors=colors[::-1] #Inverse la liste
        step=GradientSetStep(colors[0],colors[1])
        iterations = 0
    else:
        iterations+=1
        (r1,g1,b1) = fenetre.winfo_rgb(trajectoireColor)

    for c in range(pointsTrajectoire):

        #Utilisée avec le délai entre chaque frame
        modifiedVelocity[1] += gravityConst*precision
        coords[1]  += modifiedVelocity[1] * precision

        coords[0] += modifiedVelocity[0] * precision
        trajectoire.append(w.create_oval(coords[0]-trajectoireRadius,coords[1]-trajectoireRadius,coords[0]+trajectoireRadius,coords[1]+trajectoireRadius, outline=trajectoireColor) )

        #Trajectoire inverse, utilisée si on centre la vue sur le joueur et que le reste bouge à sa place
        coords2[1]  += -modifiedVelocity[1] * precision

        coords2[0] += -modifiedVelocity[0] * precision
        trajectoire.append(w.create_oval(coords2[0]-trajectoireRadius,coords2[1]-trajectoireRadius,coords2[0]+trajectoireRadius,coords2[1]+trajectoireRadius, outline='blue') )

        #Utilisée avec la somme des délais
        dx = newVelocity[0]*timeDelay
        dy = gravityConst*timeDelay*timeDelay / 2 + newVelocity[1]*timeDelay

        trajectoire.append(w.create_oval(playerCoords[0]+dx-trajectoireRadius,playerCoords[1]+dy-trajectoireRadius,playerCoords[0]+dx+trajectoireRadius,playerCoords[1]+dy+trajectoireRadius, outline='red') )
        timeDelay += precision

    timeToWait = int((fps-dt)*1000)
    if timeToWait <0:
        timeToWait = 0
    fenetre.after(timeToWait, Game)


fenetre.after(0, Game)

fenetre.mainloop()