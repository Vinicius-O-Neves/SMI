from cv2 import cv2
import numpy as np 
import imutils
import os
import os.path
from tkinter import *
from pyfirmata import Arduino, util
from pyfirmata import Arduino
from configparser import ConfigParser
import time
import sys
from Tira_Fotos import *
from PIL import Image
from PIL import ImageTk

Pasta_sem_Epi = "Funcionário_Sem_EPI"

frontal_face_cascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
face_alt_tree_cascade = cv2.CascadeClassifier("haarcascade_frontalface_alt_tree.xml")
face_alt2_cascade = cv2.CascadeClassifier("haarcascade_frontalface_alt2.xml")
profile_face_cascade = cv2.CascadeClassifier("haarcascade_profileface.xml")


#Define a webcam 
cap = cv2.VideoCapture(0)

global Sem_EPI
global CorOculos
CorOculos = False
global Batatinha
Batatinha = False
global ComOculos
ComOculos = False
global Placa
global ardu 
global frame
global parser
parser = ConfigParser()


def nothing(x):
    pass

def get_Color():
    import cor
    
def def_aduino():
    global ardu
    ardu = Tk()
    ardu.title("Teste")
    ardu.geometry("500x300")
    ardu.configure(background="#dde")
    ardu.resizable(False, False)
    ardu.iconbitmap("icon.ico")

def exitt():
    exit()
    
def Desligar_Maquina(event):
    global Batatinha
    Batatinha = True
    cap.release()
    cv2.destroyAllWindows()
    exit()
    
def ligar_camera():
    _, frame = cap.read()
    _, imagem = cap.read()
    imagem = imutils.resize(imagem, width=600, height=600)
    frame = imutils.resize(frame, width=600, height=600)

def Ligar_Maquina():
    while True:  
        if Batatinha == False:
            _, frame = cap.read()
            _, imagem = cap.read()
            imagem = imutils.resize(imagem, width=600, height=600)
            frame = imutils.resize(frame, width=600, height=600)
            hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
            hsv_imagem= cv2.cvtColor(imagem, cv2.COLOR_BGR2HSV)
            alturaImagem, larguraImagem = imagem.shape[:2]
            Gray = cv2.cvtColor(imagem, cv2.COLOR_BGR2GRAY)
            face1 = frontal_face_cascade.detectMultiScale(Gray, 1.1, 5, minSize=(60,60))
            face2 = face_alt2_cascade.detectMultiScale(Gray, 1.1, 5, minSize=(60,60))
            face3 = face_alt_tree_cascade.detectMultiScale(Gray, 1.1, 5, minSize=(60,60))
            face4 = profile_face_cascade.detectMultiScale(Gray, 1.1, 5, minSize=(60,60))
            cor = (0,0,255)              
            cv2.line(imagem, (75,0), (600,550), cor,2)
            parser.read('config.ini')
            a = int(parser.get('low_blue', 'l_h' ))
            b = int(parser.get('low_blue', 'l_s' ))
            c = int(parser.get('low_blue', 'l_v' ))
            d = int(parser.get('high_blue', 'h_h'))
            e = int(parser.get('high_blue', 'h_s'))
            f = int(parser.get('high_blue', 'h_v'))
            low_blue = np.array([a, b, c],np.uint8)
            high_blue = np.array([d, e, f],np.uint8)
            blue_mask = cv2.inRange(hsv_frame, low_blue, high_blue)
            ret, threshold = cv2.threshold(blue_mask, 95, 255, cv2.THRESH_BINARY)
            kernal = np.ones((5, 5), "uint8") 
            Color = cv2.dilate(blue_mask, kernal) 
            res_color = cv2.bitwise_and(frame, frame,  
            mask = blue_mask) 
            bordas=cv2.Canny(Color, 100,150)
            contours, hierarchy = cv2.findContours(Color, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            objetos, hierarchy2= cv2.findContours(Color.copy(),cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            for pic, contour in enumerate(contours):
                area = cv2.contourArea(contour)
                AskFace = [face1, face3, face4]
                for AskFaces in AskFace:
                    for(origemX, origemY, largura, altura) in AskFaces:
                        cv2.rectangle(imagem,(origemX,origemY),
                        (origemX + largura, origemY + altura),cor,2)
                        Largura = largura
                        Altura = altura
                        #print("Largura", largura, "Altura", altura)
                        Find = format(len(AskFaces))
                        Faces_Found = '1', '2'
                        Faces = Find
                        Many_Face = '3'
                        if Faces == "":
                            Found_Faces = False
                        elif not (Faces):
                            Found_Faces = False
                        elif Faces == AskFaces:
                            Found_Faces = False
                        elif Faces in Faces_Found:
                            Found_Faces = True
                        elif Faces == Many_Face:
                            Found_Faces = False
                        elif Faces is None:
                            Found_Faces = False
                        else:
                            Found_Faces = False             
                    if 300 < area > 500: 
                        (x, y, w, h)  = cv2.boundingRect(contour)
                        cv2.rectangle(frame, (x,y), (x + w, y +h), (0, 0, 255), 2 )
                        #cv2.putText(frame, str(area), (x, y), 1, 1, (0, 255, 0))
                        cv2.putText(frame, "Press q to quit", (x, y), 1, 2, (0, 0, 255))
                        Find_Glasses = format(len(contours))
                        Found_Glasses = format(len(Find_Glasses))
                        cv2.drawContours(frame, objetos, -1, (255, 0, 0), 2)
                        Total_de_Oculos = format(len(objetos)) 
                        Oculos = int(Total_de_Oculos) 
                        Oculos_Found = '1', '2'
                        raio = 4
                        centroRosto = (origemX + int(largura/2),origemY + int(altura/2))
                        cv2.circle(imagem, centroRosto, raio, cor)
                        NormZero21 = int(larguraImagem/2)
                        fatorDeCorreção = 10
                        erro = (((centroRosto[0] - (larguraImagem/2)) 
                        /NormZero21) * fatorDeCorreção)
                        #print(Faces)
                        #print(Oculos)
                        erro = int(erro)
                        if Oculos in range(1,4):
                            CorOculos = True
                        elif not Oculos:
                            CorOculos = False
                        if Found_Glasses != Faces:
                            ComOculos = False
                            CorOculos =  False
                    else: 
                        CorOculos = False
                        
        cv2.imshow("Frame", frame)
        #cv2.imshow("Imagem", imagem)
        if not Found_Faces:
            ComOculos = False
        elif Found_Faces is True:
            ComOculos = True
        elif Found_Faces is False:
            ComOculos = False
        else:
            ComOculos = False
    
        if CorOculos and ComOculos is True:
            print("Com EPI")
            if os.path.isdir(Pasta_sem_Epi):
                pass
            else:
                os.mkdir(Pasta_sem_Epi)
        else:
            time.sleep(0.23)
            if CorOculos and ComOculos is True:
                print("Com EPI")
            else:
                print("Sem EPI")
        
        if cv2.waitKey(1) & 0xFF==ord('q'):
            exit()
            break
 
    janela.mainloop()
    cap.release()
    cv2.destroyAllWindows()



janela = Tk()
janela.title("SMI-VisualSecurity")
janela.geometry("700x500")
janela.configure(background="#dde")
janela.resizable(False, False)
janela.iconbitmap("icon.ico")

#Definição das Imagens 
photo1 = PhotoImage(file="Logos/start.png")
photo2 = PhotoImage(file="Logos/stop.png")
photo3 = PhotoImage(file="Logos/Segurança.png")

load = Image.open("Logos/Segurança.png")
render = ImageTk.PhotoImage(load)
img1 = Label(janela, image= render)
img1.pack()

Bt1=Button(janela,text="Start", image=photo1, activebackground="green",relief=RAISED,
borderwidth=0, width=250, height=50, command=lambda:[Ligar_Maquina(),ligar_camera()])
Bt1.place(x=90,y=160)

Bt2=Button(janela,text="Stop", image=photo2, activebackground="red",relief=RAISED,
borderwidth=0, width=250, height=50, command=lambda:exitt())
Bt2.place(x=395,y=160)

MenuP = Menu(janela)

FileMenu = Menu(MenuP, tearoff=0)
FileMenu.add_separator()
FileMenu.add_command(label="Exit",command=janela.destroy)
MenuP.add_cascade(label="File", menu=FileMenu)

ArduinoMenu = Menu(MenuP, tearoff=0)
ArduinoMenu.add_command(label="Color Edit", command=get_Color)
ArduinoMenu.add_command(label="Arduino", command=def_aduino)
MenuP.add_cascade(label="Arduino", menu=ArduinoMenu)

janela.config(menu=MenuP)

janela.mainloop()

