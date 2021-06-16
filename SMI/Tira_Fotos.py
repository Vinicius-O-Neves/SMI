from cv2 import cv2

def Tira_Fotos():
    Foto=1
    while(True):
        camera = cv2.VideoCapture(0)
        retval, img = camera.read()
        cv2.imwrite('Foto'+str(Foto)+'.jpg',img)
        camera.release()
        Foto=Foto+1
