import socket
import cv2
import pickle
import struct
import numpy as np

cliente_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
cliente_socket.bind(('',9999))

payload_size = struct.calcsize("Q")
datos = b''

while True:
    while len(datos) < payload_size:
        paquete, _ = cliente_socket.recvfrom(4096)
        datos += paquete

    paquete_msj_size = datos[:payload_size]
    datos = datos[payload_size:]
    msj_size = struct.unpack("Q", paquete_msj_size)[0]

    while len(datos) < msj_size:
        paquete, _ = cliente_socket.recvfrom(4096)
        datos += paquete

    frame_datos = datos[:msj_size]
    datos = datos[msj_size:]

    frame = pickle.loads(frame_datos)
    cv2.imshow('video recibido',frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cliente_socket.close()
cv2.destroyAllWindows()
