import sys
g = sys.modules['__main__']
# On importe les variables globales du fichier 'Hub.py' qui sont des attributs du module 'Hub'

from collections import OrderedDict
import time
from tkinter import *
import tkinter as Tk
import math
import numpy as np
import itertools
import types
from PIL import Image, ImageTk
from random import randint, uniform, choice

path = g.resource_path('../GeometryAccuracy/')

image = Image.open(path+"Background.jpg")
width, height = image.size

photo = ImageTk.PhotoImage(image)

images = []

platformSize = 0.5
options = [70*g.prop[0]*platformSize,70*g.prop[1]*platformSize,50*g.prop[0]*platformSize] #width, height, yExtent

def CubeCircle(A, #A Rectangle
              B): #B Cercle

    coordsB=B.getCoords()

    pointsA=A.getCoords()
    pointsA = [ [pointsA[0][0],pointsA[1][0],pointsA[2][0],pointsA[3][0]],
                       [pointsA[0][1],pointsA[1][1],pointsA[2][1],pointsA[3][1]] ]
    pointsA = [[min(pointsA[0]),min(pointsA[1])],[max(pointsA[0]),max(pointsA[1])]]

    # on définit la ‘boundbox’ du rectangle
    rleft,rtop,rright,rbottom = pointsA[0][0], pointsA[0][1], pointsA[1][0], pointsA[1][1]

    # on définit la ‘boundbox’ du cercle
    cleft, ctop, cright, cbottom = coordsB[0]-B.radius, coordsB[1]-B.radius, coordsB[0]+B.radius, coordsB[1]+B.radius

    # On vérifie que les boundbox ne se coupent pas:
    if rright < cleft or rleft > cright or rbottom < ctop or rtop > cbottom:
        return False  # pas de collision possible

    # On vérifie qu’aucun point du rectangle ne soit à l’intérieur du cercle
    for x in (rleft, rright):
        for y in (rtop, rbottom):
            # On compare la distance entre le centre du cercle et chaque point du rectangle avec le rayon du cercle
            if math.hypot(x-coordsB[0], y-coordsB[1]) <= B.radius:
                return True  # Collision détectée

    # On vérifie si le centre du cercle est à l’intérieur du rectangle
    if rleft <= coordsB[0] <= rright and rtop <= coordsB[1] <= rbottom:
        return True  # Superposition

    return False  # Pas de collision détectée


def CircleCircle(A,B): #A: [radius,[coord.x,coord.y]] - B: [radius,[coord.x,coord.y]]
    r = A.radius + B.radius
    r *= r
    coordsA=A.getCoords()
    coordsB=B.getCoords()
    #Retourne vrai si R^2 < Distance^2
    #                 R   < Distance
    return r > (coordsA[0]-coordsB[0])**2 + (coordsA[1]-coordsB[1])**2

def CubeCube(A,B): #A: [[min.x, min.y],[max.x, max.y]] - B: [[min.x, min.y],[max.x, max.y]]

    pointsA=A.getCoords()
    pointsA = [ [pointsA[0][0],pointsA[1][0],pointsA[2][0],pointsA[3][0]], [pointsA[0][1],pointsA[1][1],pointsA[2][1],pointsA[3][1]] ]
    pointsA = [[min(pointsA[0]),min(pointsA[1])],[max(pointsA[0]),max(pointsA[1])]]

    pointsB=B.getCoords()
    pointsB = [ [pointsB[0][0],pointsB[1][0],pointsB[2][0],pointsB[3][0]], [pointsB[0][1],pointsB[1][1],pointsB[2][1],pointsB[3][1]] ]
    pointsB = [[min(pointsB[0]),min(pointsB[1])],[max(pointsB[0]),max(pointsB[1])]]

    # Pas d'intersection si les objets sont séparés le long d'un axe
    if (pointsA[1][0] < pointsB[0][0] or pointsA[0][0] > pointsB[1][0]):
        return False
    if (pointsA[1][1] < pointsB[0][1] or pointsA[0][1] > pointsB[1][1]):
        return False
    #Il existe des axes qui se coupent entre-eux
    return True

def returnToHub(direction = 'gameChoice'):
    global buttons, lost

    for i in range(len(buttons)):
        buttons[i].destroy()
    buttons.clear()

    for i in range(len(lost)):
        g.w.delete(lost[i])
    lost.clear()

    for i in range(len(images)):
        g.w.delete(images[i])
    images.clear()

    g.w.delete(DistanceAfficheur)
    g.w.delete(fast)

    g.backToHub(direction)

#Mode Normal
amplitudeX = 15
amplitudeY = 8
oneShakeDuration = 0.1 #secondes
totalDuration = oneShakeDuration* 8 /2 #secondes

#Mode Bourré
#amplitudeX = 200
#amplitudeY = 120
#oneShakeDuration = 1 #secondes
#totalDuration = oneShakeDuration* 6 /2 #secondes

shakeMoves = []
numberOfShakes = 0
shakeIndex = None
buttonColor = '#B53471'
buttons = []
def restartButtonAppear():
    global buttons

    buttons.append( Button(g.w, text=g.translate('Recommencer'), command = restartAll, anchor = CENTER, font=("Courier",int(20*g.prop[2]))) )
    buttons[len(buttons)-1].configure(fg='white', background=buttonColor, activebackground = '#4CAF50', relief = FLAT, justify='center', wraplength=(300+15)*g.prop[0])
    buttons[len(buttons)-1].place(x=510*g.prop[0], y=300*g.prop[1], width=200*g.prop[0], height=150*g.prop[1])

    buttons.append( Button(g.w, text=g.translate('Vitesse'), command = speedChoice, anchor = CENTER, font=("Courier",int(20*g.prop[2]))) )
    buttons[len(buttons)-1].configure(fg='white', background=buttonColor, activebackground = '#4CAF50', relief = FLAT, justify='center', wraplength=(300+15)*g.prop[0])
    buttons[len(buttons)-1].place(x=300*g.prop[0], y=300*g.prop[1], width=200*g.prop[0], height=150*g.prop[1])

    buttons.append( Button(g.w, text=g.translate('Hub'), command = lambda direction='gameChoice': returnToHub(direction), anchor = CENTER, font=("Courier",int(20*g.prop[2]))) )
    buttons[len(buttons)-1].configure(fg='white', background=buttonColor, activebackground = '#4CAF50', relief = FLAT, justify='center', wraplength=(300+15)*g.prop[0])
    buttons[len(buttons)-1].place(x=90*g.prop[0], y=300*g.prop[1], width=200*g.prop[0], height=150*g.prop[1])

lost = []

def restartAll():
    global chosenSpeed, lastFrameTime, destroyedPlatforms, phaseRealPositionX, speed, playerVelocity, lost, realPosition, lastPosition, buttons, player, items, createAfterX

    for i in range(len(buttons)):
        buttons[i].destroy()
    buttons.clear()

    for i in range(len(lost)):
        g.w.delete(lost[i])
    lost.clear()

    for i in range(len(images)):
        g.w.delete(images[i])
    images.clear()

    if g.plaqueTournante:
        returnToHub('randomGame')
    else:

        destroyedPlatforms = 0
        phaseRealPositionX = 0
        playerVelocity = [0,-400,0]
        speed = chosenSpeed

        realPosition = [0,playerHeight]
        lastPosition = int(0.2*g.screeny[0])

        initializeGraphicObjects()

        createAfterX = randint(int(xPlatformInterval[0]*4), int(xPlatformInterval[1]*3))
        lastFrameTime=time.time()
        Game()

def shakeScreen():
    global numberOfShakes, totalDuration, oneShakeDuration, shakeMoves, amplitudeX, amplitudeY, shakeIndex

    if numberOfShakes == 0:
        numberOfShakes = int(totalDuration / oneShakeDuration)
        shakeMoves.clear()

        for i in range(numberOfShakes):
            moveX = int(uniform(0,amplitudeX) - amplitudeX/2)
            moveY = int(uniform(0,amplitudeY) - amplitudeY/2)
            shakeMoves.append([moveX,moveY])
        for i in range(len(shakeMoves)):
            shakeMoves.append([-shakeMoves[i][0],-shakeMoves[i][1]])

        shakeIndex = 0

def GradientSetStep(color,goal,limit):

    (r1,g1,b1) = g.fenetre.winfo_rgb(color)
    (r2,g2,b2) = g.fenetre.winfo_rgb(goal)

    return [float(r2-r1) / limit,float(g2-g1) / limit,float(b2-b1) / limit]

#Couleur de la trajectoire
limit = 50 #Pas de 1/50 entre chaque changement de couleur
colors= ['white','#333']
trajectoireColor = colors [0]
iterations = 0
step = GradientSetStep(colors[0],colors[1],limit)
timeColor = 0

#Couleur des pupilles
iris = []
pupilles = []
pupilleLimit = 30 #Pas de 1/20 entre chaque changement de couleur
irisColor = 'white'
pupilleColors= ['fuchsia','black']
pupilleStep = GradientSetStep(pupilleColors[0],pupilleColors[1],pupilleLimit)
pupilleColor = pupilleColors[0]
pupilleRadius = 3
pupilleIterations = 0

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

def flatten(list_of_lists):
    #Aplatit la liste d'un niveau: ( [ [],[] ] , [ [],[] ] ) devient ( [],[],[],[] )
    return itertools.chain.from_iterable(list_of_lists)

class Cube:
    def __init__(self, ptA_, corners, color_, center_, visible_=True):
        self.visible=visible_
        self.type = 'Cube'

        self.color = color_

        self.center = center_

        self.ptA = ptA_

        self.points = [[corners[0][0],corners[0][1],0], [corners[1][0],corners[0][1],0], [corners[1][0],corners[1][1],0], [corners[0][0],corners[1][1],0]]

        for i in range(len(self.points)):
            self.points[i][0] = self.points[i][0]+self.ptA[0]- self.center[0]
            self.points[i][1] = self.points[i][1]+self.ptA[1]- self.center[1]
        if self.visible:
            self.draw()

    def draw(self):
        tmpPoints = []
        for i in range(len(self.points)):
            tmpPoints.append([  self.points[i][0]+self.center[0],
                                self.points[i][1]+self.center[1]])
        self.item = g.w.create_polygon(tmpPoints, fill=self.color, outline='')

    def refresh(self):
        if self.visible:
            tmpPoints = []
            for i in range(len(self.points)):
                tmpPoints.append([  int(self.points[i][0]+self.center[0]),
                                    int(self.points[i][1]+self.center[1])])
            g.w.coords(self.item,
            *flatten(tmpPoints))

    def translation(self, vector):
        self.center[0]+=vector[0]
        self.center[1]+=vector[1]

    def rotate(self, matrix, theta):
        for i in range(len(self.points)):
            self.points[i] = np.dot(matrix,self.points[i])

    def getCoords(self):
        tmpPoints = []
        for i in range(len(self.points)):
            tmpPoints.append([  int(self.points[i][0]+self.center[0]),
                                int(self.points[i][1]+self.center[1])])
        return tmpPoints

class Circle:
    def __init__(self, ptA_, radius_, start_, extent_, color_, center_):
        self.type = 'Circle'
        self.color = color_
        self.center = center_
        self.ptA = [ptA_[0] - self.center[0],ptA_[1] - self.center[1],0]

        self.radius = radius_
        self.start = start_
        self.extent = extent_

        self.draw()

    def draw(self):
        if self.extent == 360:
            self.item = g.w.create_oval([
            self.ptA[0]+self.center[0]-self.radius,
            self.ptA[1]+self.center[1]-self.radius,
            self.ptA[0]+self.center[0]+self.radius -1, #-1 car sinon le cercle dépase
            self.ptA[1]+self.center[1]+self.radius
            ], fill=self.color, outline='')

        else:
            self.item = g.w.create_arc([
            self.ptA[0]+self.center[0]-self.radius,
            self.ptA[1]+self.center[1]-self.radius,
            self.ptA[0]+self.center[0]+self.radius -1, #-1 car sinon le cercle dépase
            self.ptA[1]+self.center[1]+self.radius
            ], style='pieslice', fill=self.color, start=self.start, extent=self.extent, outline='')

    def refresh(self):
        g.w.coords(self.item,
        self.ptA[0]+self.center[0]-self.radius,
        self.ptA[1]+self.center[1]-self.radius,
        self.ptA[0]+self.center[0]+self.radius -1, #-1 car sinon le cercle dépase
        self.ptA[1]+self.center[1]+self.radius
        )
        if self.extent != 360:
            g.w.itemconfig(self.item,start=self.start)

    def translation(self, vector):
        self.center[0]+=vector[0]
        self.center[1]+=vector[1]

    def rotate(self, matrix, theta):
        self.ptA = np.dot(matrix,self.ptA)
        if self.extent != 360:
            self.start += math.degrees(theta)

    def getCoords(self):
        return [self.ptA[0]+self.center[0],self.ptA[1]+self.center[1]]

class Platform:
    def __init__(self, ptA_,color_,gravity_=False,toRotate_=False,player_=False):
        self.collidingState = False

        self.player = player_
        self.gravity = gravity_

        #Composantes linéaires
        self.velocity = [0,0,0]
        self.acceleration = [0,0,0]

        #Composantes angulaires
        if toRotate_:
            self.angularVelocity =[0,0,0.5]
        else:
            self.angularVelocity =[0,0,0]

        self.color = color_
        self.ptA= ptA_

        #On admet que la densité est de 1
        massAndCenters=[ #Aire, Centre
        #Premier rectangle l*L
        ( options[0]/2*(options[1]+options[2])
        ,(
        options[0]/4
        ,(options[1]+options[2])/2
        ))
        #Deuxième rectangle l*L
        ,(options[0]/2*(options[1]/2+options[2])
        ,(
        options[0]/4 + options[0]/2
        ,(options[1]/2+options[2])/2 +options[1]/2
        ))
        #Quart de cercle    (pi*R^2)/4
        ,((math.pi*(options[0]/2)**2)/4
        ,(
        (4*options[0]/2)/(3*math.pi)    +options[0]/2
        ,(4*options[0]/2)/(3*math.pi)
        ))
        ]

        self.center = [0,0]
        totalMass = 0
        for i in range(len(massAndCenters)):
            self.center[0] += massAndCenters[i][1][0] * massAndCenters[i][0]
            self.center[1] += massAndCenters[i][1][1] * massAndCenters[i][0]
            totalMass += massAndCenters[i][0]

            middle = [massAndCenters[i][1][0] + self.ptA[0], massAndCenters[i][1][1] + self.ptA[1]]
            #g.w.create_oval(middle[0]-5, middle[1]-5, middle[0]+5, middle[1]+5, fill='red')

        self.center[0] = self.center[0]/totalMass +self.ptA[0]
        self.center[1] = self.center[1]/totalMass +self.ptA[1]

        #self.mass = totalMass

        #g.w.create_oval(self.center[0]-5, self.center[1]-5, self.center[0]+5, self.center[1]+5, fill='green')

        self.elements = [
        Circle([self.ptA[0]+options[0]/2,self.ptA[1]+options[1]/2], options[0]/2, 0, 90, self.color[2], self.center)

        ,Cube(self.ptA,
        [[0,0]
        ,[options[0]/2, options[1]+options[2]]
        ], self.color[0], self.center)

        ,Cube(self.ptA,
        [[options[0]/2, options[1]/2]
        ,[options[0], options[1]+options[2]]
        ], self.color[1], self.center)

        ,Cube(self.ptA,
        [[0,0]
        ,[options[0], options[1]+options[2]]
        ], self.color[0], self.center, False)]

        if self.player:
            global iris, irisColor, pupilles, pupilleColor
            iris.extend([Circle([self.ptA[0]+options[0]/4,self.ptA[1]+(options[1]+options[2])/2], options[0]/4, 0, 360, irisColor, self.center)
                           ,Circle([self.ptA[0]+options[0]*3/4,self.ptA[1]+(options[1]+options[2])/2], options[0]/4, 0, 360, irisColor, self.center)])
            pupilles.extend([g.w.create_oval(0,0,0,0, fill=pupilleColor)
                            ,g.w.create_oval(0,0,0,0, fill=pupilleColor)])


    def translation(self, vector):
        self.center[0]+=vector[0]
        self.center[1]+=vector[1]

    def refresh(self):
        for i in range(len(self.elements)):
            self.elements[i].refresh()

    def mayCollide(self,object):
        if CubeCube(self.elements[len(self.elements)-1],object.elements[len(object.elements)-1]):
            return True

    def collide(self, object):
        #3*3 collisions possibles entre Cercle, AABB, CCDD, Cercle2, EEFF, GGHH
        #Cercle-Cercle2     #AABB-Cercle2   #CCDD-Cercle2
        #Cercle-EEFF        #AABB-EEFF      #CCDD-EEFF
        #Cercle-GGHH        #AABB-GGHH      #CCDD-GGHH
        for i in range(len(self.elements)-1):
            for j in range(len(object.elements)-1):

                if self.elements[i].type == 'Circle':
                    if object.elements[j].type == 'Circle':
                        if CircleCircle(self.elements[i],object.elements[j]):
                            return True
                    else:
                        if CubeCircle(object.elements[j],self.elements[i]):
                            return True
                else:
                    if object.elements[j].type == 'Circle':
                        if CubeCircle(self.elements[i],object.elements[j]):
                            return True
                    else:
                        if CubeCube(self.elements[i],object.elements[j]):
                            return True

    def delete(self, removeFromList=True):
        for i in range(len(self.elements)-1):
            g.w.delete(self.elements[i].item)
        if removeFromList:
            try:
                items.remove(self)
            except:
                pass

    def makeCollidable(self):
        self.collidingState = False


lastPosition = int(0.2*g.screeny[0])

playerHeight = 0.45*g.screeny[1]

realPosition = [0,playerHeight]
phaseRealPositionX = 0

#Minimum et maximum:
xPlatformInterval = [int(options[0]*7),int(options[0]*15)]

yPlatformInterval = [int(1*g.screeny[1] - realPosition[1]),int(1.4*g.screeny[1] - realPosition[1])]

items = []

axis = [0,0,1]

lastFrameTime=time.time()
fps = 1/80

playerVelocity = [0,-400,0]

pointsTrajectoire = 113
precision = 0.05 #Temps entre chaque point de la trajectoire
trajectoire = []

gravityConst = 9.81*30

def strokeText(x, y, text, textcolor, strokecolor, size):
    texts = []
    # On affiche un texte en gras, c'est l'ombre du texte normal
    texts.append( g.w.create_text(x, y, text=text, anchor = NW, font=("Courier",size,'bold'), fill=strokecolor) )
    # On affiche un texte normal
    texts.append( g.w.create_text(x, y, text=text, anchor = NW, font=("Courier",size), fill=textcolor) )

    return texts

timeBeforeDestroyingPlatform = 0.35 #Le temps entre chaque destruction de plateforme est de 200 milisecondes
destroyedPlatforms = 0
timeDelayDestroy = 0

def Game():
    global timeDelayDestroy, timeBeforeDestroyingPlatform, destroyedPlatforms, lost, pupilleStep, pupilleColors, pupilleColor, pupilleIterations, numberOfShakes, shakeIndex, iris, pupilles, pupilleRadius, timeColor, step, iterations, colors, trajectoireColor, speed, lastFrameTime, fps, playerVelocity, realPosition, phaseRealPositionX, createAfterX, trajectoire, pointsTrajectoire, precision, totalTime

    # dt est la différence de temps en secondes
    currentTime = time.time()
    dt = currentTime - lastFrameTime

    dt*=speed
    timeDelayDestroy+=dt

    lastFrameTime = currentTime

    if numberOfShakes != 0:
        if shakeIndex < numberOfShakes*2 -1:

            toMoveBy = [shakeMoves[math.ceil(shakeIndex)][0]*dt/oneShakeDuration,shakeMoves[math.ceil(shakeIndex)][1]*dt]
            for i in range(len(items)):
                items[i].translation(toMoveBy)

            for i in range(len(images)):
                g.w.move(images[i], toMoveBy[0], toMoveBy[1])

            shakeIndex += dt/oneShakeDuration #Produit en croix

            if shakeIndex >= numberOfShakes*2 -1:
                numberOfShakes = 0

                #toMoveBy = [0.2*g.screeny[0]-player.center[0],playerHeight- player.center[1]]

                #for i in range(len(items)):
                #    items[i].translation(toMoveBy)

                #for i in range(len(images)):
                #    g.w.move(images[i], toMoveBy[0], toMoveBy[1])

    #On obtient la position du curseur par rapport à la fenêtre
    mouseCoords = [g.fenetre.winfo_pointerx() - g.fenetre.winfo_rootx(), g.fenetre.winfo_pointery() - g.fenetre.winfo_rooty()]

    #Vitesse intiiale
    initialVelocity = math.sqrt((player.center[0]-mouseCoords[0])**2+(player.center[1]-mouseCoords[1])**2)

    initialAngle = math.atan2(mouseCoords[1]-player.center[1], mouseCoords[0]-player.center[0])

    newVelocity = [initialVelocity*math.cos(initialAngle),initialVelocity*math.sin(initialAngle)]

    if newVelocity[0] > 340:
        newVelocity[0] = 340
    elif newVelocity[0] < -100:
        newVelocity[0] = -100
    if newVelocity[1] < -460:
        newVelocity[1] = -460

    for c in range(len(trajectoire)):
        g.w.delete(trajectoire[c])
    trajectoire.clear()

    coords = list(player.center)
    modifiedVelocity = list(newVelocity)

    if pupilleIterations == pupilleLimit:
        pupilleColor = pupilleColors[1]

    else:
        pupilleIterations+=1
        (r1,g1,b1) = g.fenetre.winfo_rgb(pupilleColor)
        pupilleColor = "#%4.4x%4.4x%4.4x" % (int(r1+pupilleStep[0]),int(g1+pupilleStep[1]),int(b1+pupilleStep[2]))
        for i in range(len(pupilles)):
            g.w.itemconfig(pupilles[i], fill=pupilleColor)


    if iterations == limit:
        trajectoireColor = colors[1] #On s'assure que le but soit atteint
        timeColor+=dt #Somme du temps depuis que la couleur voulue ait été atteinte
        if timeColor > 1.2: #si la somme du temps est supérieure à 1,2 secondes:
            colors=colors[::-1] #Inverse la liste
            step=GradientSetStep(colors[0],colors[1],limit)
            iterations = 0
    else:
        iterations+=1
        (r1,g1,b1) = g.fenetre.winfo_rgb(trajectoireColor)
        trajectoireColor = "#%4.4x%4.4x%4.4x" % (int(r1+step[0]),int(g1+step[1]),int(b1+step[2]))
        timeColor = 0

    if (trajectoireColor != '#333'):
        for c in range(pointsTrajectoire):

            modifiedVelocity[1] += gravityConst*precision
            coords[1]  += modifiedVelocity[1] * precision

            coords[0] += modifiedVelocity[0] * precision
            trajectoire.append(g.w.create_oval(coords[0]-2,coords[1]-2,coords[0]+2,coords[1]+2, outline=trajectoireColor) )
        for c in range(len(trajectoire)):
            g.w.tag_lower(trajectoire[c])
        for c in range(len(images)):
            g.w.tag_lower(images[c])

    speed += 0.0001
    g.w.itemconfig(fast, text=str(int(speed*100))+'%')

    #Velocity
    playerVelocity[1] += gravityConst*dt

    #Position
    realPosition[0] += playerVelocity[0]*dt
    phaseRealPositionX += playerVelocity[0]*dt
    realPosition[1] += playerVelocity[1]*dt

    g.w.itemconfig(DistanceAfficheur, text=g.translate('Distance parcourue')+': '+str( int(realPosition[0]) ) )

    toDelete = []
    toMoveBy = [-playerVelocity[0]*dt,-playerVelocity[1]*dt]

    for i in range(len(images)):
        g.w.move(images[i], toMoveBy[0]/2, toMoveBy[1]/2)

        if g.w.coords(images[i])[1] >= 2*height:
            g.w.move(images[i], 0, -3*height)

        elif g.w.coords(images[i])[1] <= -height+g.screeny[1] -2*height:

            g.w.move(images[i], 0, 3*height)

        if g.w.coords(images[i])[0] >= 2*width:
            g.w.move(images[i], -3*width, 0)

        elif g.w.coords(images[i])[0] <= -width+g.screeny[0]-2*width:
            g.w.move(images[i], 3*width, 0)


    for i in range(len(items)):
        if (not items[i].player):
            items[i].translation([toMoveBy[0]+items[i].velocity[0]*dt,toMoveBy[1]+items[i].velocity[1]*dt])

        if items[i].angularVelocity != [0,0,0]:

            theta = items[i].angularVelocity[2] * dt

            rotationMatrix = M(axis, theta) #On calcule la matrice de rotation

            for j in range(len(items[i].elements)):
                    items[i].elements[j].rotate(rotationMatrix, theta)
            #Eyes
            if items[i].player:
                for j in range(len(iris)):
                    iris[j].rotate(rotationMatrix, theta)
                    iris[j].refresh()

        #Collision avec le bord gauche de l'écran:
        if items[i].elements[len(items[i].elements)-1].center[0] + options[0]/2 <= -g.screeny[1] and not items[i].player:
            toDelete.append(items[i])
        else:
            items[i].refresh()
    #Eyes
    for i in range(len(iris)):
        circleCenter = iris[i].getCoords()
        x = circleCenter[0] + (iris[i].radius-pupilleRadius) * math.cos( math.atan2(mouseCoords[1]-circleCenter[1], mouseCoords[0]-circleCenter[0]) );
        y = circleCenter[1] + (iris[i].radius-pupilleRadius) * math.sin( math.atan2(mouseCoords[1]-circleCenter[1], mouseCoords[0]-circleCenter[0]) );
        g.w.coords(pupilles[i],
        x-pupilleRadius,
        y-pupilleRadius,
        x+pupilleRadius,
        y+pupilleRadius
        )

    for i in range(len(toDelete)):
        toDelete[i].delete()

    #Collision du joueur avec une autre platforme
    for i in range(len(items)):
        if (not items[i].player):
            if player.mayCollide(items[i]): #Broad Phase
                if player.collide(items[i]): #Narrow Phase, phase plus précise

                    if timeDelayDestroy >= timeBeforeDestroyingPlatform:
                        destroyedPlatforms +=1
                        timeDelayDestroy = 0

                    playerVelocity = newVelocity
                    items[i].velocity = [-playerVelocity[0],-playerVelocity[1]]

                    shakeScreen()

                    if pupilleIterations == pupilleLimit:

                        pupilleColors=pupilleColors[::-1] #Inverse la liste
                        pupilleStep=GradientSetStep(pupilleColors[0],pupilleColors[1],pupilleLimit)
                        pupilleIterations = 0

                    break

    if (createAfterX - phaseRealPositionX <= 0):

        phaseRealPositionX = 0
        y = randint(yPlatformInterval[0], yPlatformInterval[1])+playerHeight-realPosition[1]

        newPlatform = Platform([g.screeny[0]+options[0], y],['#2ed573','#1e90ff','#3742fa'])

        theta = uniform(-math.pi, math.pi)

        rotationMatrix = M([0,0,1], theta) #On calcule la matrice de rotation

        for j in range(len(newPlatform.elements)):

            newPlatform.elements[j].rotate(rotationMatrix, theta)
            newPlatform.refresh()

        items.append(newPlatform)

        createAfterX = randint(xPlatformInterval[0], xPlatformInterval[1])
    if realPosition[1] > 1.5*g.screeny[1]:

        speedRecord = g.profileVar('GAspeedRecord')
        if speedRecord == 'None':
            speedRecord = 0
        if speed > float(speedRecord):
            g.profileVar('GAspeedRecord',str(speed),True)

        destroyedPlatformsList = g.profileVar('GAaverageDestroyedPlatforms')
        if destroyedPlatformsList == 'None':
            destroyedPlatformsList = []
        else:
            if isinstance(destroyedPlatformsList, (list,)):
                pass
            else:
                destroyedPlatformsList = destroyedPlatformsList.split(',')
        destroyedPlatformsList.append(destroyedPlatforms)
        g.profileVar('GAaverageDestroyedPlatforms',destroyedPlatformsList,True)

        gameNumber = g.profileVar('GAgameNumber')
        if gameNumber == 'None':
            gameNumber = 0
        gameNumber = int(gameNumber)
        gameNumber+=1
        g.profileVar('GAgameNumber',str(gameNumber),True)

        lost = strokeText(g.screeny[0]/2 + 110*g.prop[0], g.screeny[1]/2, g.translate('Game Over'), 'white', 'fuchsia', int(30*g.prop[2]))

        for i in range(len(items)):
            items[i].delete(False)
        items.clear()

        for i in range(len(trajectoire)):
            g.w.delete(trajectoire[i])
        trajectoire.clear()

        for i in range(len(iris)):
            g.w.delete(iris[i].item)
        iris.clear()

        for i in range(len(pupilles)):
            g.w.delete(pupilles[i])
        pupilles.clear()

        restartButtonAppear()

    else:

        timeToWait = int((fps-dt)*1000)
        if timeToWait <0:
            timeToWait = 0
        g.fenetre.after(timeToWait, Game)

chosenSpeed = None
speed = 1

player = None

def initializeGraphicObjects():
    global player, items, images, lastPosition

    for ligne in range(3):
        for colonne in range(3):
            images.append( g.w.create_image((-1+colonne)*width, (-1+ligne)*height, anchor = Tk.NW, image=photo) )

    player = Platform([0.2*g.screeny[0], playerHeight],['#3c40c6','#34e7e4','#ffdd59'], True, True, True)
    items.extend([player,Platform([0.2*g.screeny[0], randint(yPlatformInterval[0], yPlatformInterval[1])],['#2ed573','#1e90ff','#3742fa'])])

    platformsNumber = math.ceil( (g.screeny[0]-lastPosition)/xPlatformInterval[0] )
    #Le nombre de plateformes est arrondi à l'entier supérieur

    for i in range(platformsNumber):
        newPos = randint(lastPosition+xPlatformInterval[0], lastPosition+xPlatformInterval[1])

        newPlatform = Platform([newPos, randint(yPlatformInterval[0], yPlatformInterval[1])],['#2ed573','#1e90ff','#3742fa'])
        lastPosition = newPos
        theta = uniform(-math.pi, math.pi)

        rotationMatrix = M([0,0,1], theta) #On calcule la matrice de rotation

        for j in range(len(newPlatform.elements)):

            newPlatform.elements[j].rotate(rotationMatrix, theta)
            newPlatform.refresh()

        items.append(newPlatform)

createAfterX = None
fast = None
DistanceAfficheur = None
def chooseSpeed(newSpeed):
    global chosenSpeed, speed, buttons, lastFrameTime, DistanceAfficheur, fast, createAfterX, destroyedPlatforms, phaseRealPositionX, playerVelocity, speed, chosenSpeed, realPosition, lastPosition, createAfterX, lastFrameTime

    chosenSpeed = float(newSpeed)/100
    speed = chosenSpeed

    for i in range(len(buttons)):
        buttons[i].destroy()
    buttons.clear()

    fast = g.w.create_text(g.screeny[0]-120*g.prop[0], 20*g.prop[1], text=str(speed*100)+'%', anchor = NW, font=("Courier",int(30*g.prop[2])), fill='white')
    DistanceAfficheur = g.w.create_text(15*g.prop[0], 10*g.prop[1], text=g.translate('Distance parcourue')+': '+str( int(realPosition[0]) ), anchor = NW, font=("Courier",int(17*g.prop[2])), fill='white')

    destroyedPlatforms = 0
    phaseRealPositionX = 0
    playerVelocity = [0,-400,0]

    realPosition = [0,playerHeight]
    lastPosition = int(0.2*g.screeny[0])

    initializeGraphicObjects()

    createAfterX = randint(int(xPlatformInterval[0]*4), int(xPlatformInterval[1]*3))
    lastFrameTime=time.time()

    Game()

speedDict = OrderedDict()
speedDict["75"] = 'Novice'
speedDict["100"] = 'Débutant'
speedDict["150"] = 'Amateur'
speedDict["200"] = 'Maître'

def speedChoice():
    global buttons, DistanceAfficheur, fast, lost, images

    for i in range(len(buttons)):
        buttons[i].destroy()
    buttons.clear()
    g.w.delete(DistanceAfficheur)
    g.w.delete(fast)
    try:
        for i in range(len(buttons)):
            buttons[i].destroy()
        buttons.clear()
    except:
        pass
    try:
        for i in range(len(lost)):
            g.w.delete(lost[i])
        lost.clear()
    except:
        pass
    try:
        for i in range(len(images)):
            g.w.delete(images[i])
        images.clear()
    except:
        pass

    speedRecord = g.profileVar('GAspeedRecord')
    if speedRecord == 'None':
        speedRecord = 0
    else:
        speedRecord = float(speedRecord)
    i = 0

    for speedParameter in speedDict.keys():

        buttons.append(Button(g.w, text = speedParameter +'cc\n'+ speedDict[speedParameter], command = lambda speedParameter=speedParameter: chooseSpeed(speedParameter), anchor = CENTER,font=("Courier",int(12*g.prop[2]))))
        buttons[len(buttons)-1].place(x=g.screeny[0]/2-200*g.prop[0]*len(speedDict)/2 +200*g.prop[0]*i, y=g.screeny[1]/2-150*g.prop[1]/2, width=200*g.prop[0], height=150*g.prop[1])
        buttons[len(buttons)-1].configure(fg='white', background='#111', activebackground = '#4CAF50', relief = RIDGE, justify='center')

        if float(speedParameter)/100 > speedRecord and speedParameter != "75":
            buttons[len(buttons)-1].configure(state='disabled', bg='#ff6b6b')
        i+=1

if g.plaqueTournante:
    playableSpeeds = []

    speedRecord = g.profileVar('GAspeedRecord')
    if speedRecord == 'None':
        speedRecord = 0
    else:
        speedRecord = float(speedRecord)

    for speedParameter in speedDict.keys():
        if speedRecord >= float(speedParameter)/100 or speedParameter == "75":
            playableSpeeds.append(float(speedParameter)/100)

    if len(playableSpeeds)>1:
        playableSpeeds.pop(0)

    speed = choice(playableSpeeds)
    initializeGraphicObjects()
    createAfterX = randint(int(xPlatformInterval[0]*4), int(xPlatformInterval[1]*3))
    fast = g.w.create_text(g.screeny[0]-120*g.prop[0], 20*g.prop[1], text=str(speed*100)+'%', anchor = NW, font=("Courier",int(30*g.prop[2])), fill='white')
    DistanceAfficheur = g.w.create_text(15*g.prop[0], 10*g.prop[1], text=g.translate('Distance parcourue')+': '+str( int(realPosition[0]) ), anchor = NW, font=("Courier",int(17*g.prop[2])), fill='white')

    lastFrameTime=time.time()
    g.fenetre.after(0, Game)

else:
    speedChoice()