#importamos las dependecias necesarias
import socketio
import base64
import cv2
import numpy as np

#iniciamos la libreia socketio como cliente
sio = socketio.Client()

#definimos la url y el puerto del servidor
sio.connect('http://localhost:3000')

#definimos una imagen inicial para mostrar en caso de no reciviir nada la iniciar el programa para que cv2.imshow no genre error
imgn = np.ones((480,640,3), np.uint8)

#funcion para decodificar las imagenes recibidas
def decode_img(args):
    #se crea una variable global don ira contenida la imagem para mostrar
    global imgn

    #quitamos los espacio dentro del string en base64 recibido
    i =''.join(args)

    #quitamos los datos de la cabecera
    img = i[23:]

    #decodificamos el string con los datos en base64
    image=base64.b64decode(img)

    #creamos un vector para imagen
    nparr = np.frombuffer(image, np.uint8)

    #convertimos el vector en imagen ya con la imagen podrias manipuklarla y anadirle mas cosas 
    imgn = cv2.imdecode(nparr, cv2.IMREAD_COLOR)


    
#bucle para recibir las imagenes
while True:
    #escuchamos al servidor en busca de imagnes emitidas
    sio.on('stream', decode_img)

    #podermos agregar un retraso en segundos al para recibir las imagenes cada x timpo
    #sio.sleep(x)

    #mostramos las imagenes recibidas
    cv2.imshow('preview', imgn)
  
    #detenemos todo presionando la tecla Esc  
    k = cv2.waitKey(10)
    if k == 27:
        cv2.destroyAllWindows()
        sio.disconnect()
        break
