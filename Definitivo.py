import pygame
from random import randint


# Inicialización de Pygame
pygame.init()

# Contador de golpes con el bate
golpes_con_bate = 0

# Dimensionado de la ventana de juego
ancho_ventana = 640
alto_ventana = 480
tamaño_ventana = (ancho_ventana, alto_ventana)

# Inicializo los valores con los que se van a mover la pelota
speed = [randint(2, 3), randint(-3, -2)]

# Configuración de la ventana del juego
ventana = pygame.display.set_mode(tamaño_ventana)
pygame.display.set_caption("ARKANOID ALEJANDRO y MIGUEL")
fuente = pygame.font.Font(None, 70)
fuente_pequeña = pygame.font.Font(None, 36)

## BOLA ##
# Crea el objeto pelota y obtengo su rectángulo
ball = pygame.image.load('Pelota.png')
ball = pygame.transform.scale(ball, (20, 20))  # Ajustar tamaño de la pelota si es necesario
ballrect = ball.get_rect()
ballrect.topleft = (200, 200)

## BATE ##
# Crea el objeto bate y obtengo su rectángulo
bate = pygame.image.load("plataforma.png")
bate = pygame.transform.scale(bate, (100, 20))  # Ajustar tamaño del bate si es necesario
baterect = bate.get_rect()
baterect.midbottom = (ancho_ventana // 2, alto_ventana - 30)

## LADRILLOS ##
class Ladrillo:
    def __init__(self, image_path, width, height):
        self.image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(self.image, (width, height))
        self.rect = self.image.get_rect()

class LadrilloIrrompible(Ladrillo):
    def __init__(self, image_path, width, height):
        super().__init__(image_path, width, height)

# Crea los objetos ladrillo y obtengo su rectángulo
ladrillo = Ladrillo("slakoth.png", 60, 30)
ladrillo_especial_1 = Ladrillo("ladrillo_especial_3.png", 60, 30)
ladrillo_especial_2 = Ladrillo("ladrillo_especial_2.png", 60, 30)
ladrillo_especial_3 = Ladrillo("ladrillo_especial_1.png", 60, 30)
ladrillo_irrompible = LadrilloIrrompible("ladrillo_irrompible.png", 60, 30)

# Matriz de ladrillos
filas = 5
columnas = 9
ladrillos = []

for fila in range(filas):
    fila_ladrillos = []
    for columna in range(columnas):
        if fila == 3:  # Fila especial
            ladrillo_instancia = ladrillo_especial_1
            ladrect = ladrillo_instancia.rect.copy()
            ladrect.topleft = (columna * (ladrect.width + 5) + 30, fila * (ladrect.height + 5) + 10)
            fila_ladrillos.append({'rect': ladrect, 'golpes': 0, 'surface': ladrillo_instancia.image})
        elif fila == 4 and columna in [3, 5]:  # Posiciones de los ladrillos irrompibles
            ladrillo_instancia = ladrillo_irrompible
            ladrect = ladrillo_instancia.rect.copy()
            ladrect.topleft = (columna * (ladrect.width + 5) + 30, fila * (ladrect.height + 5) + 10)
            fila_ladrillos.append({'rect': ladrect, 'golpes': -2, 'surface': ladrillo_instancia.image})  # -2 para identificar irrompibles
        else:
            ladrillo_instancia = ladrillo
            ladrect = ladrillo_instancia.rect.copy()
            ladrect.topleft = (columna * (ladrect.width + 5) + 30, fila * (ladrect.height + 5) + 10)
            fila_ladrillos.append({'rect': ladrect, 'golpes': -1, 'surface': ladrillo_instancia.image})
    ladrillos.append(fila_ladrillos)

# Contador de ladrillos rotos
ladrillos_rotos = 0

# Bucle principal del juego
jugando = True
while jugando:
    # Comprobamos los eventos
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            jugando = False

    # Compruebo si se ha pulsado alguna tecla
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and baterect.left > 0:
        baterect.move_ip(-6, 0)
    if keys[pygame.K_RIGHT] and baterect.right < ancho_ventana:
        baterect.move_ip(6, 0)

    # Compruebo si hay colisión entre el bate y la pelota
    if baterect.colliderect(ballrect):
        speed[1] = -speed[1]
        golpes_con_bate += 1
        if golpes_con_bate % 5 == 0:
            # Aumentar la velocidad de la bola 
            speed[0] *= 1.4
            speed[1] *= 1.4

    # Muevo la pelota
    ballrect = ballrect.move(speed)

    # Compruebo si la pelota llega a los límites de la ventana y rebota
    if ballrect.left < 0 or ballrect.right > ancho_ventana:
        speed[0] = -speed[0]
    if ballrect.top < 0:
        speed[1] = -speed[1]

    # Si la pelota sale por el fondo, finaliza la partida con una pantalla de game over
    if ballrect.bottom > alto_ventana:
        texto = fuente.render("Game Over", True, (0, 0, 255))
        texto_rect = texto.get_rect(center=(ancho_ventana // 2, alto_ventana // 2))
        ventana.blit(texto, texto_rect)
        pygame.display.flip()
        pygame.time.delay(2000)  # Pausa para mostrar el mensaje de Game Over
        jugando = False

    # Compruebo colisiones con ladrillos
    for fila in ladrillos:
        for ladrillo in fila:
            ladrillo_rect = ladrillo['rect']
            if ballrect.colliderect(ladrillo_rect):
                speed[1] = -speed[1]
                if ladrillo['golpes'] == -1:
                    fila.remove(ladrillo)  # Elimina el ladrillo normal cuando hay colisión
                    ladrillos_rotos += 25  # Incrementa el contador de ladrillos rotos
                elif ladrillo['golpes'] >= 0:
                    ladrillo['golpes'] += 1
                    if ladrillo['golpes'] == 1:
                        ladrillo['surface'] = ladrillo_especial_2.image
                    elif ladrillo['golpes'] == 2:
                        ladrillo['surface'] = ladrillo_especial_3.image
                    elif ladrillo['golpes'] >= 3:
                        fila.remove(ladrillo)  # Elimina el ladrillo especial después de 3 golpes
                        ladrillos_rotos += 50  # Incrementa el contador de ladrillos rotos

    if jugando:
        # Dibujar el fondo
        ventana.fill((50, 200, 50))

        # Dibujar los ladrillos
        for fila in ladrillos:
            for ladrillo in fila:
                ventana.blit(ladrillo['surface'], ladrillo['rect'].topleft)

        # Dibujar la pelota
        ventana.blit(ball, ballrect)

        # Dibujar el bate
        ventana.blit(bate, baterect)

        # Dibujar el contador de ladrillos rotos
        contador_texto = fuente_pequeña.render(f"Score: {ladrillos_rotos}", True, (0, 0, 0))
        ventana.blit(contador_texto, (10, 450))

        pygame.display.flip()

    # Controlamos la frecuencia de refresco (FPS)
    pygame.time.Clock().tick(60)

pygame.quit()
