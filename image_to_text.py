from process_image import *

import pytesseract as tess
import cv2


#tess.pytesseract.tesseract_cmd = r'C:\Users\LENOVO\.conda\envs\tesseract\Library\bin\tesseract.exe'



def decomposition_le_cheque_en_image(nom_de_cheque) :
    image = cv2.imread('static/img/' + nom_de_cheque)
    text = tess.image_to_string(image)

    #print(text)
    largeur=image.shape[0]
    langueur=image.shape[1]
    #numero de cheque
    w = int ( langueur * 0.35)
    h =int ( largeur * 0.2)
    image2 = image[:, :]


    #rendre l'image noire et blanc
    gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY )
    cv2.imwrite('temp/index_gray.png',gray)

    cv2.rectangle(image, (0, 0), (w, h), (36, 0, 255), 2)
    num_cheque = image[0:h, 0:w]
    cv2.imwrite("besoin/numcheque.png", num_cheque)

    # montant de cheque
    cv2.rectangle(image, (langueur - w, 0), (langueur, h), (36, 0, 255), 2)
    montant = image[0:h, langueur - w:langueur]
    cv2.imwrite("besoin/montant.png", montant)

    #detection les champs globals
    dilate =detection_de_parametre(gray)

    cnts =cv2.findContours(dilate,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    cnts =cnts[0] if len(cnts) == 2 else cnts[1]
    cnts = sorted(cnts , key= lambda x: cv2.boundingRect(x)[0])
    i=0
    l=[]
    compteur =0
    compteur_rib =0



    for c in cnts :
        x,y,w,h = cv2.boundingRect(c)
        i=i+1
        if h > 20 and w > 10:
            roi =image[y:y+h,x:x+w]

            cv2.imwrite("temp/index_roi" + str(i) + ".png", roi)
            image1 = cv2.imread("temp/index_roi{}.png".format(i))
            text = tess.image_to_string(image1)
            l = text.split()
            #cv2.rectangle(image2, (x, y), (x + w, y+ h), (0, 250, 2), 2)

            if (('Titulaire' in l) or ( largeur * 0.45< y< largeur * 0.5 and (compteur_rib  < 1) )) :
                #detection du rib bancaire
                w = int(langueur * 0.45)
                k = int(y )
                h =  int(largeur * 0.25)
                z=int (langueur * 0.25)




                cv2.rectangle(image, (z, k), (z + w , k + h), (36, 0, 255), 2)
                compteur_rib =1
                if z >0 and y>0:
                    titulaire =image[k:k+h,z:z+w]
                    cv2.imwrite("besoin/titulaire.png",titulaire)

            elif ('Payable' in l) or (largeur * 0.50< y < largeur * 0.55 and compteur < 1 ) :
                #detection  de region de banque
                w = int(langueur * 0.25)
                k = int(y + h)
                h = int(largeur * 0.35)
                #z = int(x - w * 0.20)
                compteur =1
                cv2.rectangle(image, (0, k), (0 + w, k + h ), (36, 0, 255), 2)
                payable = image[k:k + h, 0:w]
                cv2.imwrite("besoin/payable.png", payable )
        cv2.imwrite("temp/image2.png", image2)

    cv2.imwrite("temp/image_bbox.png", image)

#image = cv2.imread('besoin/titulaire.png')
#text = tess.image_to_string(image)
