import pygame, sys
from pygame.locals import *

# Definindo cores
BLACK = pygame.Color('black')
WHITE = pygame.Color('white')
RED = pygame.Color('red')
GREEN = pygame.Color('green')
BLUE = pygame.Color('blue')
YELLOW = pygame.Color('yellow')

# Configurações de tela
SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480
HALF_SCREEN_HEIGHT = int(SCREEN_HEIGHT / 2)

def main():
    pygame.init()

    # Abrindo a janela do Pygame
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("simple road")
    
    # Carregando imagens
    light_road = pygame.image.load('./assets/images/light_road.png').convert()
    dark_road = pygame.image.load('./assets/images/dark_road.png').convert()
    car_image = pygame.image.load('./assets/images/carro.png').convert_alpha()

    # Dimensões e posição inicial do carro
    car_width, car_height = car_image.get_size()
    car_x = (SCREEN_WIDTH - car_width) // 2
    car_y = SCREEN_HEIGHT - car_height - 30  # Posição do carro na tela

    # Criando superfícies para as tiras de estrada
    light_strip = pygame.Surface((SCREEN_WIDTH, 1)).convert()
    dark_strip = pygame.Surface((SCREEN_WIDTH, 1)).convert()
    light_strip.fill(light_road.get_at((0, 0)))
    dark_strip.fill(dark_road.get_at((0, 0)))

    # Variáveis de controle
    texture_position = 0
    ddz = 0.001
    dz = 0
    z = 0
    road_pos = 0
    road_acceleration = 80
    texture_position_acceleration = 4
    texture_position_threshold = 300
    half_texture_position_threshold = int(texture_position_threshold / 2)

    # Variáveis para a curva
    curve_position = 0
    curve_velocity = 0
    curve_acceleration = 0.01
    s_curve_sharpness = 2

    # Criando o mapa da curva
    curve_map = []
    for i in range(HALF_SCREEN_HEIGHT):
        curve_velocity += curve_acceleration
        curve_position += curve_velocity * s_curve_sharpness
        curve_acceleration -= 0.0001
        curve_map.append(curve_position)
    
    # Variáveis de controle da curva
    curve_map_length = len(curve_map)
    curve_map_index = -1
    curve_increment = 2
    curve_direction = 1
    curve_value = 0

    while True:
        pygame.time.Clock().tick(30)
        
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        # Controle de movimentação
        keys = pygame.key.get_pressed()
        if keys[K_UP]:
            road_pos += road_acceleration
            if road_pos >= texture_position_threshold:
                road_pos = 0
            curve_map_index += curve_increment
            if curve_map_index >= curve_map_length:
                curve_map_index = curve_map_length
                curve_increment *= -1
            elif curve_map_index < -1:
                curve_increment *= -1
                curve_direction *= -1

        # Movimento do carro
        if keys[K_LEFT]:
            car_x -= 5
        if keys[K_RIGHT]:
            car_x += 5

        # Limites do carro na tela
        car_x = max(0, min(car_x, SCREEN_WIDTH - car_width))

        # Desenhando a estrada
        texture_position = road_pos
        dz = 0
        z = 0
        screen.fill(BLUE)
        for i in range(HALF_SCREEN_HEIGHT, 0, -1):
            if curve_map_index >= i:
                curve_value = curve_map[curve_map_index - i] * curve_direction
            else:
                curve_value = 0
            if texture_position < half_texture_position_threshold:
                screen.blit(light_strip, (0, i + HALF_SCREEN_HEIGHT))
                screen.blit(light_road, (curve_value, i + HALF_SCREEN_HEIGHT), (0, i, SCREEN_WIDTH, 1))
            else:
                screen.blit(dark_strip, (0, i + HALF_SCREEN_HEIGHT))
                screen.blit(dark_road, (curve_value, i + HALF_SCREEN_HEIGHT), (0, i, SCREEN_WIDTH, 1))
            dz += ddz
            z += dz
            texture_position += texture_position_acceleration + z
            if texture_position >= texture_position_threshold:
                texture_position = 0

        # Desenhando o carro na tela
        screen.blit(car_image, (car_x, car_y))

        pygame.display.flip()

if __name__ == "__main__":
    main()
