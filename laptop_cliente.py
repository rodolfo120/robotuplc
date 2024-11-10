import socket
import pygame
import pickle
import struct
import cv2

cliente_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
cliente_socket.settimeout(0.1)

servidor_ip = ('192.168.1.120', 9999)

pygame.init()
pygame.joystick.init()
volante = pygame.joystick.Joystick(0)
volante.init()

def obtener_datos_volante():
    pygame.event.pump()
    dato = {'volante': volante.get_axis(0), 'acelerador':volante.get_axis(1)}
    return dato

while True:
    dato_volante = obtener_datos_volante()
    dato_volante_packed = pickle.dumps(dato_volante)
    cliente_socket.sendto(dato_volante_packed, servidor_ip)

    try:
        dato, _ = cliente_socket.recvfrom(4096)
        packed_mensaje_size = dato[:struct.calcsize("Q")]
        mensaje_size = struct.unpack("Q", packed_mensaje_size)[0]
        
        dato_frame = dato[struct.calcsize("Q"):]
        while len(dato_frame) < mensaje_size:
            packet, _ = cliente_socket.recvfrom(4096)
            dato_frame += packet
        
        if len(dato_frame) == mensaje_size:
            frame = pickle.loads(dato_frame)
            cv2.imshow('Video Recibido', frame)
        else:
            print("Frame incompleto, descartado.")
    except socket.timeout:
        pass  

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cliente_socket.close()
cv2.destroyAllWindows()
pygame.quit()