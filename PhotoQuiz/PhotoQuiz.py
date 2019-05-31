import sys
g = sys.modules['__main__']
# On importe les variables globales du fichier 'Hub.py' qui sont des attributs du module 'Hub'

from tkinter import *
from PIL import Image, ImageTk
import random, os
from collections import OrderedDict
from math import ceil
import codecs
import time

path = g.resource_path('../PhotoQuiz/imageFolder/')
dirs = []

themes = OrderedDict()
themes['cook'] = [g.translate('cook'),g.translate('Guess what meal is shown !')]
themes['space'] = [g.translate('space'),g.translate('Contemplate its treasures')]
themes['animals'] = [g.translate('animals'),g.translate('Beautiful (and funny) creatures')]
themes['technology'] = [g.translate('technology'),g.translate('Does the high-tech still have a secret you ?')]
themes['home furniture'] = [g.translate('home furniture'),g.translate('Why not take a new look at what\'s around you ?')]
themes['games'] = [g.translate('games'),g.translate('You think you\'re a crack at this ? Let\'s show us !')]

NbrCaracter=0
foundLetters=[]

for theme in themes.keys():
    #On vérifie que les dossiers existent
    dirs = os.listdir(path)

    if theme not in dirs:

        try:
            os.mkdir(path+theme)
            print('Le dossier '+theme+' a été créé.')
        except:
            print('Le dossier '+theme+' n\'a pas pas pu être créé.')

    imagesFromTheme = os.listdir(path+theme)

    for img in range(len(imagesFromTheme)):
        imgName = imagesFromTheme[img]
        for i in range(len(imgName)):
            if (imgName[i] == '.'):
                imgName=imgName[:i]
                break
        g.translate(imgName)

def saveVar(win=True):
    global beginTime
    elapsedTime = round(time.time() - beginTime, 3)
    timeList = g.profileVar('PHaverageTime')
    if timeList == 'None':
        timeList = []
    else:
        if isinstance(timeList, (list,)):
            pass
        else:
            timeList = timeList.split(',')
    timeList.append(elapsedTime)
    g.profileVar('PHaverageTime',timeList,True)

    themeList = g.profileVar('PHthemes')
    if themeList == 'None':
        themeList = []
    else:
        if isinstance(themeList, (list,)):
            pass
        else:
            themeList = themeList.split(',')
    if theme not in themeList:
        themeList.append(theme)
        g.profileVar('PHthemes',themeList,True)

    if win:
        nbr = g.profileVar('PHvictories')
        if nbr == 'None':
            nbr = 0
        nbr=int(nbr)
        nbr+=1
        g.profileVar('PHvictories',str(nbr),True)
    else:
        nbrDefeats = g.profileVar('PHdefeats')
        if nbrDefeats == 'None':
            nbrDefeats = 0
        nbrDefeats=int(nbrDefeats)
        nbrDefeats+=1
        g.profileVar('PHdefeats',str(nbrDefeats),True)

def letterChoice(lettre, index):
    global imgName, NbrCaracter, health, foundLetters, name, currentImgName, touches

    lettre=lettre.lower()

    changed = False
    for i in range( len(imgName) ):

        if normalizedImgName[i] == lettre:
            currentImgName = currentImgName[:i] + imgName[i] + currentImgName[i+1:]
            NbrCaracter += imgName.count(lettre)
            foundLetters.append(lettre)
            changed = True

    if changed:
        touches[index].configure(state='disabled', bg='#4CAF50')
        name.configure(text=currentImgName)
        if currentImgName == imgName:
            victory()
    else:
        touches[index].configure(state='disabled', bg='#ff6b6b')

def victory():
    restartButtonAppearPH()
    #print("victoire")
    saveVar() #On enregistre toutes les statistiques en tant que partie gagnée

def lose():
    restartButtonAppearPH()
    #print("défaite")
    saveVar(False) #On enregistre toutes les statistiques en tant que partie perdue

buttons = []
buttonSize=170*g.prop[2] #Taille de chaque bouton

divides = 3
separator = 5*g.prop[2] #Pixels entre chaque image

buttonSeparator = separator

def Keyboard():
    global touches, letterSize
    for ligne in range(3):
        for colonne in range(touchesParLigne):
            if (ligne*touchesParLigne+colonne <= len(liste)-1):

                touches.append(Button(g.w, text=liste[ligne*touchesParLigne+colonne], command = lambda lettre=liste[ligne*touchesParLigne+colonne], index=ligne*touchesParLigne+colonne: letterChoice(lettre,index), anchor = CENTER))
                touches[len(touches)-1].place(x=250*g.prop[0] +letterSize*colonne, y=450*g.prop[1]+letterSize*ligne, width=letterSize, height=letterSize)

def buttonToTheme(newTheme, buttonIndex):
    global theme, dirs, buttons

    theme=newTheme

    dirs = os.listdir(path+theme)
    #On vérifie que le dossier contienne plus de 2 images:
    if len(dirs) <=2:
        buttons[buttonIndex].configure(text='Il n\'y a pas suffisamment d\'images dans cette catégorie !', fg='white', bg='#ff6b6b', state='disabled')
    else:
        for i in range(len(buttons)):
            buttons[i].destroy()
        buttons.clear()
        defineImage()

def returnToHub(direction = 'gameChoice'):
    global buttons, imgRect, name
    for i in range(len(buttons)):
        buttons[i].destroy()
    buttons.clear()

    for i in range(len(imgRect)):
        imgRect[i].destroy()
    imgRect.clear()
    for i in range(len(blankRect)):
        blankRect[i].destroy()
    blankRect.clear()

    try:
        name.destroy()
        name = None
    except:
        pass

    g.backToHub(direction)

def ThemeChoice():
    global buttons, themeParLigne, themes, health

    health=9

    keys = []
    items = []
    for k, v in themes.items():
        keys.append(k)
        items.append(v)

    totalLines = ceil(len(themes)/themeParLigne)
    for ligne in range( totalLines ):
        for colonne in range(themeParLigne):
            if (ligne*themeParLigne+colonne <= len(themes)-1):

                index = ligne*themeParLigne+colonne
                buttons.append(Button(g.w, text = items[index][0] +'\n'+'\n'+ items[index][1], command = lambda theme_=keys[index], index_=index: buttonToTheme(theme_,index_), anchor = CENTER,font=("Courier",int(12*g.prop[2]))))
                buttons[len(buttons)-1].configure(fg='white', background='#111', activebackground = '#4CAF50', relief = RIDGE, justify='center', wraplength=160*g.prop[2])

                buttons[len(buttons)-1].place(x=g.screeny[0]/2-buttonSize*themeParLigne/2 +(buttonSize+buttonSeparator)*(index-themeParLigne*ligne), y=g.screeny[1]/2-(totalLines/2)*buttonSize + (buttonSize+buttonSeparator)*ligne, width=buttonSize, height=buttonSize)
    buttons.append(Button(g.w, text="Retour", command = lambda direction='gameChoice': returnToHub(direction), anchor = CENTER, font=("Courier",int(12*g.prop[2]))))
    buttons[len(buttons)-1].configure(fg='white', background='#111', activebackground = '#4CAF50', relief = RIDGE, justify='center')
    buttons[len(buttons)-1].place(x=g.screeny[0]-5/8*240*g.prop[0], y=g.screeny[1]-3/2*30*g.prop[1], width=240*g.prop[0]/2, height=30*g.prop[1])

imgHeight = int(300*g.prop[1])

def getImage():

    global imgWidth, theme, dirs

    try:
        #Relative Path
        imgName = random.choice([
            x for x in dirs
            if os.path.isfile(os.path.join(path+theme, x))
        ])

        img = Image.open(path+theme+'/'+imgName)

        width, height = img.size

        newSize = [int(width*imgHeight/height),imgHeight]

        for i in range(len(imgName)):
            if (imgName[i] == '.'):
                #formatImage=imgName[i+1:]
                imgNameUnCut=imgName
                imgName=imgName[:i]
                break

        if [width,height] != newSize:
            try:
                img = img.resize(newSize, Image.ANTIALIAS)
                img.save(path + theme +'/'+imgNameUnCut,"PNG", quality=100)

            except IOError:
                print("Impossible de redimensionner l'image "+imgName+" !")
                exit()

        #Effet miroir
        if random.randint(0,1)==0:
            img = img.transpose(Image.FLIP_LEFT_RIGHT)

        return[img, g.translate(imgName), newSize ]

    except IOError:
        pass

#All crop rectangles
#0,0,1,1
#0,1,1,2
#0,2,1,3

#1,0,2,1
#1,1,2,2
#1,2,2,3

#2,0,3,1
#2,1,3,2
#2,2,3,3

imgRect = []
blankRect = []
rectWidth=None
rectHeight=None
imgName = None
nameSize = 40
normalizedImgName = None

#Liste des caractères exclus, et donc automatiquement rêvélés à l'utilisateur
excludedCharacters = [':','-','.','œ','(',')',' ','’',"'",'_','0','1','2','3','4','5','6','7','8','9']

import unicodedata
name = None
center = None
picture=None
def defineImage():
    global picture, allImages, center, name,nameSize,beginTime,divides,separator,imgRect,blankRect,rectWidth,rectHeight,imgName,normalizedImgName,currentImgName,excludedCharacters
    newImage = getImage()

    imgName = newImage[1]
    #On enlève les accents:
    #On normalise la string sous forme NKFD,
    #c'est à dire décomposée de façon compatible
    normalizedImgName = unicodedata.normalize('NFKD', imgName)
    #On ajoute chaque lettre au mot
    normalizedImgName = u"".join([c for c in normalizedImgName if not unicodedata.combining(c)])
    #On met en minuscule le texte
    normalizedImgName = normalizedImgName.lower()

    currentImgName = ''
    for i in range(len(imgName)):
        if imgName[i] in excludedCharacters:
            currentImgName += imgName[i]
        else:
            currentImgName += '_' #Chaque lettre correspond à un '_' pour ne pas la dévoiler

    rectWidth = int(newImage[2][0]/divides)
    rectHeight = int(newImage[2][1]/divides)

    imgRect.clear()
    blankRect.clear()

    center = [g.screeny[0]/2, newImage[2][1]/2+2*separator+50*g.prop[1] ]
    x=center[0]-rectWidth-separator
    initY = center[1]-150*g.prop[1]
    y = initY
    Keyboard()
    picture=newImage[0]
    for i in range(divides):
        for j in range(divides):
            crop_rectangle = (rectWidth*i, rectHeight*j, rectWidth*(i+1), rectHeight*(j+1))

            cropped_img = newImage[0].crop(crop_rectangle)
            cropped_img = ImageTk.PhotoImage(cropped_img,master=g.fenetre)

            blankRect.append(Button(g.w, anchor = CENTER))
            blankRect[len(blankRect)-1]['command'] = lambda x_=x, y_=y, image_=cropped_img, button=blankRect[len(blankRect)-1]: drawImage(x_,y_,image_,button)
            blankRect[len(blankRect)-1].configure(background='#111', activebackground = '#4CAF50', relief = RIDGE)
            blankRect[len(blankRect)-1].place(x=x-rectWidth/2, y=y-rectHeight/2, width=rectWidth, height=rectHeight)


            y+=rectHeight+separator
        y = initY
        x+=rectWidth+separator
    name = Label(g.w, text=currentImgName, anchor = CENTER, font=("Courier",int(nameSize*g.prop[2])), bg=g.backgroundColor, fg='white')
    name.place(relx=.5, y=center[1]+rectHeight*1.5+separator, anchor='center')
    beginTime = time.time()

certain = False
def reEnable(supprButton):
    supprButton.configure(background='#111', state='normal')

def drawImage(x,y,photo,button):
    global health,imgRect,certain,allImages
    if health == 1 and certain == False:
        button.configure(text=g.translate('Are you certain ?'), fg='white', bg='#ff6b6b', state='disabled')
        certain = True
        g.fenetre.after(1000, lambda button=button: reEnable(button) )
    else:
        health=health-1
        imgRect.append( Label(image=photo, borderwidth=0) )
        imgRect[len(imgRect)-1].image = photo #On garde une référence de l'image
        imgRect[len(imgRect)-1].place(x=x-rectWidth/2, y=y-rectHeight/2)
        blankRect.remove(button)
        button.destroy()
        if health==0:
            restartButtonAppearPH()
            lose()

def restartAll():
    global buttons, health, name
    health = None

    for i in range(len(buttons)):
        buttons[i].destroy()
    buttons.clear()

    for i in range(len(imgRect)):
        imgRect[i].destroy()
    imgRect.clear()
    for i in range(len(blankRect)):
        blankRect[i].destroy()
    blankRect.clear()

    name.destroy()
    name = None

    if g.plaqueTournante:
        returnToHub('randomGame')
    else:
        ThemeChoice()


def restartButtonAppearPH():
    global picture, touches, buttons, name, blankRect, imgName, imgRect

    for i in range(len(touches)):
        touches[i].destroy()
    touches.clear()

    x=center[0]-rectWidth-separator
    initY = center[1]-150*g.prop[1]
    y = initY

    for i in range(len(imgRect)):
        imgRect[i].destroy()
    imgRect.clear()
    for i in range(len(blankRect)):
        blankRect[i].destroy()
    blankRect.clear()

    for i in range(divides):
        for j in range(divides):
            crop_rectangle = (rectWidth*i, rectHeight*j, rectWidth*(i+1), rectHeight*(j+1))

            cropped_img = picture.crop(crop_rectangle)
            cropped_img = ImageTk.PhotoImage(cropped_img,master=g.fenetre)

            imgRect.append( Label(image=cropped_img, borderwidth=0) )
            imgRect[len(imgRect)-1].image = cropped_img #On garde une référence de l'image
            imgRect[len(imgRect)-1].place(x=x-rectWidth/2, y=y-rectHeight/2)

            y+=rectHeight+separator
        y = initY
        x+=rectWidth+separator

    name.configure(text=imgName)

    buttons.append( Button(g.w, text=g.translate('Hub'), command = lambda direction='gameChoice': returnToHub(direction), anchor = CENTER, fg='white', background='#111', activebackground = '#4CAF50', relief = RIDGE, font=( "Courier",int(20*g.prop[2]) )) )
    buttons[len(buttons)-1].place(x=center[0]-210*g.prop[0], y=center[1]+rectHeight*1.5+separator+50*g.prop[1], width=200*g.prop[0], height=150*g.prop[1])

    buttons.append( Button(g.w, text=g.translate('Recommencer'), command = restartAll, anchor = CENTER, fg='white', background='#111', activebackground = '#4CAF50', relief = RIDGE, font=( "Courier",int(20*g.prop[2]) )) )
    buttons[len(buttons)-1].place(x=center[0]+10*g.prop[0], y=center[1]+rectHeight*1.5+separator+50*g.prop[1], width=200*g.prop[0], height=150*g.prop[1])


#--------------------------------------------------------------------

#Liste des lettres
liste = [ "A", "Z", "E", "R", "T", "Y", "U", "I", "O", "P", "Q", "S", "D", "F", "G", "H", "J", "K", "L", "M", "W", "X", "C", "V", "B", "N", "-"]
letterSize=75*g.prop[2] #Taille de chaque lettre dans chaque bouton composant le clavier
touchesParLigne = 10 #Nombre de touches par ligne
touches = [] #Liste des touches

themeParLigne = 3


if g.plaqueTournante:
    health=9

    keys = []
    for possibleTheme in themes.keys():
        if len( os.listdir(path+possibleTheme) ) > 2:
            keys.append(possibleTheme)
    theme=random.choice(keys)
    dirs = os.listdir(path+theme)

    defineImage()
else:
    ThemeChoice()