# -*- coding: cp1252 -*-
#!usr/bin/python3.2

#programme d'écriture: stéganographie
#Ouverture des fichiers
original=input("Quel est le nom de l'image originale ?")
final=input("Quel est le nom de l'image à créer ?")
code=input("Quel est le code à envoyer ?")

file1=open(original+'.ppm','r')
file2=open(final+'.ppm','w')

#On lit puis on copie les premières lignes
ligne1=str(file1.readline())
print(ligne1)
file2.write(ligne1)

ligne1=str(file1.readline())
print(ligne1)
file2.write(ligne1)

ligne1=str(file1.readline())
print(ligne1)
file2.write(ligne1)

liste=ligne1.split()
print(liste)
px=int(liste[0])*int(liste[1])*3 #si c'est une photo couleur
print("il y a ",px," pixels dans la photo")


ligne1=str(file1.readline())
file2.write(ligne1)
vmax=int(ligne1)
print("La valeur max d'un pixel vaut: ",vmax)

#COPIE DES DONNEES IMAGE ET INSERTION CODE

position=int(px/len(code))-1
for j in range(len(code)):
    print("Etape n°",j+1)

    ligne1=str(file1.readline())
    ajout=int(code[j])
    if ajout==0:
        ajout=10
    if int(ligne1)+10<vmax:
        file2.write(str(int(ligne1)+ajout)+'\n')
        print("Je remplace ",ligne1," par ", ligne1,"+",ajout)
    else :
        file2.write(str(int(ligne1)-ajout)+'\n')
        print("Je remplace ",ligne1," par ", ligne1,"-",ajout)
    print("je passe à la suite...")
    print("Je copie ", position-1," pixels.")
    for i in range(0,position-1): # on fait (position-1) tours dans la boucle
        ligne1=str(file1.readline())
        file2.write(ligne1)
    print("Insertion")

#COPIE PIXELS RESTANTS
pix2=(position)*len(code)
print("Ce qui me fait ",pix2," pixels recopiés")
print("Il en manque donc : ",px-pix2)
for k in range(0,px-pix2):
    ligne1=str(file1.readline())
    file2.write(ligne1)

print("Ce qui me fait ",(position)*len(code)+(px-pix2)," pixels recopiés")
print("L'image :",final," est disponible dans le dossier")

#FERMETURE FICHIERS
file1.close()
file2.close()