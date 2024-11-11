import socket
import pygame

pygame.init()
pygame.joystick.init()
volante = pygame.joystick.Joystick(0)
volante.init()

datos_volante = {
    "angulo_giro": 0.5,  
    "acelerador": 0.0,
    "freno": 0.0,
    "embrague": 0.0
}

HOST = '192.168.106.99' 
PORT = 65432        

def read_wheel():
    pygame.event.pump()
    datos_volante["angulo_giro"] = (volante.get_axis(0) + 1) / 2
    datos_volante["acelerador"] = (1 - volante.get_axis(2)) / 2
    datos_volante["freno"] = (1 - volante.get_axis(3)) / 2
    datos_volante["embrague"] = (1 - volante.get_axis(1)) / 2
    return datos_volante

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    try:
        while True:
            fun_datos_volante= read_wheel()
            data = f"{fun_datos_volante}".encode()  
            s.sendall(data)
    finally:
        pygame.quit()
