import socket

# Configuración del servidor
HOST = '192.168.105.153'  # Dirección del servidor (localhost en este caso)
PORT = 65432        # Puerto de comunicación

# Crea el socket
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    print('Esperando conexión...')
    conn, addr = s.accept()
    with conn:
        print(f'Conectado con {addr}')
        while True:
            data = conn.recv(1024)
            if not data:
                break
            print('Datos recibidos:', data.decode())
