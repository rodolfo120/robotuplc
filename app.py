import pygame
import socket
import json

tcp_ip = "127.0.0.1"
tcp_puerto = 5005
buffer_size = 1024

pygame.init()
pygame.joystick.init()

if pygame.joystick.get_count() > 0:
    joystick = pygame.joystick.Joystick(0)
    joystick.init()
    print("detectado")
else:
    print("no detectado")
    exit()

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((tcp_ip,tcp_puerto))

try:
    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.JOYAXISMOTION:
                giro = joystick.get_axis(0)
                datos = {
                    "axis": giro
                }
                sock.sendall(json.dumps(datos).encode("utf-8"))

except KeyboardInterrupt:
    print("Conexion cerrada")

finally:
    sock.close()
    pygame.quit()