import cv2
def detection_de_parametre(gray):
    blur =cv2.GaussianBlur(gray,(7,7),0)
    cv2.imwrite('temp1/index_blur.png',blur)

    thresh = cv2.threshold(blur,0,255,cv2.THRESH_BINARY_INV +cv2.THRESH_OTSU)[1]
    cv2.imwrite("temp/index_thresh.png", thresh)
    kernal =cv2.getStructuringElement(cv2.MORPH_RECT,(20,20))

    cv2.imwrite("temp/index_kernal.png", kernal)

    dilate = cv2.dilate(thresh,kernal,iterations= 1)
    cv2.imwrite("temp/index_dilate.png",dilate)
    return  dilate