import socket
import cv2
import pickle
import struct

servidor_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
servidor_socket.bind(('', 9999))

camara = cv2.VideoCapture(0)

cliente_ip = None

while camara.isOpened():
    ret, frame = camara.read()
    if not ret:
        break

    datos_frame = pickle.dumps(frame)
    mensaje_size = struct.pack("Q", len(datos_frame))

    if cliente_ip:
        servidor_socket.sendto(mensaje_size + datos_frame, cliente_ip)

    for i in range(0, len(datos_frame), 4096):
            servidor_socket.sendto(datos_frame[i:i+4096], cliente_ip)

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