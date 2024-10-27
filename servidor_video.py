import socket
import cv2
import pickle
import struct

cam = cv2.VideoCapture(0)

servidor_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
cliente_ip = ('',9999)

while cam.isOpened():
    ret, frame = cam.read()
    if not ret:
        break


    datos = pickle.dumps(frame)
    msj_size = struct.pack("Q", len(datos))

    servidor_socket.sendto(msj_size + datos, cliente_ip)

    cv2.imshow('enviando video', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cam.release()
cv2.destroyAllWindows()