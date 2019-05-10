# -*- coding: cp1252 -*-
#!usr/bin/python3.2

#programme de décodage: steganographie

def getKey(chemin, envoi, retour):

    code=""
    code1=open(chemin+envoi+'.ppm','r')
    code2=open(chemin+retour+'.ppm','r')

    ligne1=str(code1.readline())
    ligne2=str(code2.readline())

    ligne1=str(code1.readline())
    ligne2=str(code2.readline())

    ligne1=str(code1.readline())
    ligne2=str(code2.readline())

    ligne1=str(code1.readline())
    ligne2=str(code2.readline())

    ligne1=str(code1.readline())
    ligne2=str(code2.readline())

    while ligne1!="":
        if ligne1 != ligne2 :
            x=abs(int(ligne2)-int(ligne1))
            if x==10:
                x=0
            code=code+str(x)
        ligne1=str(code1.readline())
        ligne2=str(code2.readline())
    code1.close()
    code2.close()

    listCode = []
    setTmp = False
    for i in range(1,len(code)+1):
        if i%3 == 0:
            listCode.append( int(code[i-1]) )
            continue
        if not setTmp:
            tmp = code[i-1]
            setTmp = True
            continue
        listCode.append( (int(tmp)+int(code[i-1]))%26 )
        setTmp = False

    return listCode



