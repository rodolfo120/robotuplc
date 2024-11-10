import socket
import pygame

# Inicializa pygame y el volante (ver paso anterior)
pygame.init()
pygame.joystick.init()
wheel = pygame.joystick.Joystick(0)
wheel.init()

# Configuración del cliente socket
HOST = '192.168.106.99'  # Dirección del servidor (localhost en este caso)
PORT = 65432        # Puerto de comunicación

# Función para leer los datos del volante
def read_wheel():
    pygame.event.pump()
    steering = wheel.get_axis(0)
    throttle = wheel.get_axis(1)
    brake = wheel.get_axis(2)
    return steering, throttle, brake

# Enviar datos mediante el socket
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    try:
        while True:
            steering, throttle, brake = read_wheel()
            data = f"{steering},{throttle},{brake}".encode()  # Convierte a bytes
            s.sendall(data)
    finally:
        pygame.quit()
