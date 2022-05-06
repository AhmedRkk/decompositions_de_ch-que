import pytesseract as tess

import cv2

base_path = 'besoin/'

# la tronsformation  de l' image d'aderesse de  banque  en text
def adresse_bank(nom_image):
   # tess.pytesseract.tesseract_cmd = r'C:\Users\LENOVO\.conda\envs\tesseract\Library\bin\tesseract.exe'
    image = cv2.imread(base_path + nom_image)
    text = tess.image_to_string(image)
    liste = text.split()
    adresse =" ".join(liste)
    return adresse

# la tronsformation  de l'image de numero bancaire en text
def numero_cheque(nom_image):
   # tess.pytesseract.tesseract_cmd = r'C:\Users\LENOVO\.conda\envs\tesseract\Library\bin\tesseract.exe'
    image = cv2.imread(base_path + nom_image)
    text = tess.image_to_string(image)

    l = text.split()
    #print(l)
    test = False
    for i in range (len(l)):


        if len(l[i]) == 7:
            test = True
            indice = i
            for j in range(7):
                if l[i][j] not in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']:
                    test = False
                    break
    if test == True:
        return l[indice]
    else:
        return '0'

# la tronsformation  de l' image de rib bancaire en text
def rib(nom_image):
    #tess.pytesseract.tesseract_cmd = r'C:\Users\LENOVO\.conda\envs\tesseract\Library\bin\tesseract.exe'
    image = cv2.imread(base_path + nom_image)
    text = tess.image_to_string(image)
    l = text.split()
    ch = ''.join(l)
    chain = ''
    test = False
    nom_titulaire = ''

    for i in range(len(ch)):
        if ch[i] in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']:
            chain = chain + ch[i]
        elif len(chain) == 20:
            liste = [chain[0:2], chain[2:5], chain[5:18], chain[18:20]]
            test = True
            for j in range(l.index(liste[3]) + 1, len(l)):
                if not (l[j] in ['TND', 'le', 'LE', 'A','M']) and l[j] == l[j].upper():
                    nom_titulaire = nom_titulaire + l[j] + ' '
            liste.append(nom_titulaire)
            return liste
        else:
            chain = ''
    if test == False:
        return -1
