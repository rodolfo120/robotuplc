import pygame

# Inicializar pygame
pygame.init()

# Inicializar el joystick
pygame.joystick.init()

# Verificar si hay algún volante conectado
if pygame.joystick.get_count() == 0:
    print("No se detectó ningún volante.")
else:
    # Asignar el primer volante conectado
    volante = pygame.joystick.Joystick(0)
    volante.init()
    print(f"Volante detectado: {volante.get_name()}")

    # Diccionario para almacenar los datos del volante
    datos_volante = {
        "angulo_giro": 0.5,   # Inicia en 0.5, posición central
        "acelerador": 0.0,
        "freno": 0.0,
        "embrague": 0.0
    }

    # Bucle principal para leer los datos
    ejecutando = True
    while ejecutando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                ejecutando = False

            # Actualizar los datos del volante
            if evento.type == pygame.JOYAXISMOTION:
                # Obtener y normalizar el ángulo de giro (eje 0)
                # El valor se normaliza para que -1 sea 0.0 y 1 sea 1.0
                datos_volante["angulo_giro"] = (volante.get_axis(0) + 1) / 2

                # Obtener y normalizar el valor del acelerador (eje 2)
                datos_volante["acelerador"] = (1 - volante.get_axis(2)) / 2

                # Obtener y normalizar el valor del freno (eje 3)
                datos_volante["freno"] = (1 - volante.get_axis(3)) / 2

                # Obtener y normalizar el valor del embrague (eje 1)
                datos_volante["embrague"] = (1 - volante.get_axis(1)) / 2

        # Imprimir el diccionario de datos del volante
        print(datos_volante)

# Cerrar pygame
pygame.quit()

