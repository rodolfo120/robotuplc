from controller import Robot
import socket
import json

robot = Robot()
timestep = int(robot.getBasicTimeStep())

left_motor = robot.getDevice('left wheel motor')
right_motor = robot.getDevice('right wheel motor')
left_motor.setPosition(float('inf'))
right_motor.setPosition(float('inf'))
left_motor.setVelocity(0.0)
right_motor.setVelocity(0.0)

tcp_ip = "127.0.0.1"
tcp_puerto = 5005
buffer_size = 1024

sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
sock.bind((tcp_ip,tcp_puerto))
sock.listen(1)

print("esperando conexion")

conn, addr = sock.accept()
print("conexion establecida con {addr}")

def map_value(value, in_min, in_max, out_min, out_max):
    return out_min + (float(value - in_min) / float(in_max - in_min) * (out_max - out_min))

try:
    while robot.step(timestep) != -1:
        data = conn.recv(buffer_size).decode('utf-8')
        if not data:
            break
        
        datos = json.loads(data)
        if 'axis' in datos:
            giro = datos['axis']
            velocidad_izquierda = map_value(giro, -1, 1, -3, 3)
            velocidad_derecha = map_value(-giro, -1, 1, -3, 3)
            left_motor.setVelocity(velocidad_izquierda)
            right_motor.setVelocity(velocidad_derecha)

except KeyboardInterrupt:
    print("Servidor detenido.")
finally:
    conn.close()
    sock.close()