import socket
import cv2
import pickle
import struct

servidor_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
servidor_socket.bind(('192.168.106.99', 9999))

camara = cv2.VideoCapture(1)

cliente_ip = None  

while camara.isOpened():
    ret, frame = camara.read()
    if not ret:
        break

    dato_frame = pickle.dumps(frame)
    mensaje_size = struct.pack("Q", len(dato_frame))

    if cliente_ip:
        servidor_socket.sendto(mensaje_size, cliente_ip)

        for i in range(0, len(dato_frame), 4096):
            servidor_socket.sendto(dato_frame[i:i+4096], cliente_ip)

    try:
        dato, ip = servidor_socket.recvfrom(4096)
        if not cliente_ip:
            cliente_ip = ip 

        dato_volante = pickle.loads(dato)  
        print("Datos del volante recibidos:", dato_volante)
    except socket.timeout:
        pass  

    cv2.imshow('Video Enviado', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

camara.release()
cv2.destroyAllWindows()
