import pygame
import sys
import random
from pygame.locals import *

# Cores
PRETO = pygame.Color('black')
BRANCO = pygame.Color('white')
VERMELHO = pygame.Color('red')
VERDE = pygame.Color('green')
AZUL = pygame.Color('blue')
AMARELO = pygame.Color('yellow')

# Configurações de tela
LARGURA_TELA = 640
ALTURA_TELA = 480
METADE_ALTURA_TELA = int(ALTURA_TELA / 2)
LARGURA_ESTRADA = 200  # Largura da estrada

class CarroIA:
    def __init__(self, x, y, velocidade, imagem, escala_inicial):
        self.x = x
        self.y = y
        self.velocidade = velocidade
        self.imagem_original = imagem
        self.imagem = pygame.transform.scale(imagem, (int(imagem.get_width() * escala_inicial), int(imagem.get_height() * escala_inicial)))
        self.escala = escala_inicial
        self.direcao = random.choice([-1, 1])  # Direção inicial para mover-se lateralmente
        self.movimento_lateral = random.randint(1, 3)  # Velocidade do movimento lateral
        self.frequencia_mudanca = random.randint(30, 100)  # Frequência para mudar a direção lateral
        self.contador_mudanca = 0

    def movimentar(self):
        # Movimento vertical
        self.y += self.velocidade
        
        # Movimento lateral
        self.contador_mudanca += 1
        if self.contador_mudanca >= self.frequencia_mudanca:
            self.direcao *= -1  # Muda a direção do movimento lateral
            self.contador_mudanca = 0

        self.x += self.direcao * self.movimento_lateral
        
        # Restrições para que o carro não saia da tela
        self.x = max(240, min(self.x, 380))
        
        # Se o carro sai da tela, reinicie sua posição
        if self.y > ALTURA_TELA:
            self.reset()
        
        # Ajuste da escala
        if self.escala < 1.0:
            self.escala += 0.01
        
        self.imagem = pygame.transform.scale(self.imagem_original, (int(self.imagem_original.get_width() * self.escala), int(self.imagem_original.get_height() * self.escala)))

    def reset(self):
        self.escala = 0.2
        self.y = METADE_ALTURA_TELA - random.randint(20, 50)
        self.velocidade = random.randint(3, 6)
        self.x = random.randint(240, 380)
        self.direcao = random.choice([-1, 1])
        self.movimento_lateral = random.randint(1, 3)
        self.frequencia_mudanca = random.randint(30, 100)
        self.contador_mudanca = 0

    def desenhar(self, tela):
        tela.blit(self.imagem, (self.x, self.y))

def desenhar_estrada(tela):
    # Borda esquerda e direita da estrada
    pygame.draw.rect(tela, VERMELHO, (240, 0, 10, ALTURA_TELA), 3)  # Borda esquerda
    pygame.draw.rect(tela, VERMELHO, (LARGURA_TELA - 250, 0, 10, ALTURA_TELA), 3)  # Borda direita

def main():
    pygame.init()

    # Janela do Pygame
    tela = pygame.display.set_mode((LARGURA_TELA, ALTURA_TELA))
    pygame.display.set_caption("simple road")
    
    # Carrega as imagens
    estrada_clara = pygame.image.load('./assets/images/light_road.png').convert()
    estrada_escura = pygame.image.load('./assets/images/dark_road.png').convert()
    imagem_carro = pygame.image.load('./assets/images/f1_car_centered.png').convert_alpha()
    imagem_carro_ia = pygame.image.load('./assets/images/enemies_cars.png').convert_alpha()
    
    pygame.mixer.music.load('./assets/sounds/tema_da_vitoria_ayrton_senna.wav')
    pygame.mixer.music.play(-1)  # Play the soundtrack in a loop

    largura_carro, altura_carro = imagem_carro.get_size()
    posicao_carro_x = (LARGURA_TELA - largura_carro) // 2
    posicao_carro_y = ALTURA_TELA - altura_carro - 30

    carros_ia = [
        CarroIA(random.randint(240, 380), METADE_ALTURA_TELA - random.randint(20, 40), 1, imagem_carro_ia, 0.1),
        CarroIA(random.randint(240, 380), METADE_ALTURA_TELA - random.randint(20, 40), 1, imagem_carro_ia, 0.1),
        CarroIA(random.randint(240, 380), METADE_ALTURA_TELA - random.randint(20, 40), 1, imagem_carro_ia, 0.1)
    ]

    faixa_clara = pygame.Surface((LARGURA_TELA, 1)).convert()
    faixa_escura = pygame.Surface((LARGURA_TELA, 1)).convert()
    faixa_clara.fill(estrada_clara.get_at((0, 0)))
    faixa_escura.fill(estrada_escura.get_at((0, 0)))

    posicao_textura = 0
    ddz = 0.001
    dz = 0
    z = 0
    posicao_estrada = 0
    aceleracao_estrada = 80
    aceleracao_posicao_textura = 4
    limite_posicao_textura = 300
    metade_limite_posicao_textura = int(limite_posicao_textura / 2)

    global valor_curva
    posicao_curva = 0
    velocidade_curva = 0
    aceleracao_curva = 0.01
    s_curva_intensidade = 2

    mapa_curva = []
    for i in range(METADE_ALTURA_TELA):
        velocidade_curva += aceleracao_curva
        posicao_curva += velocidade_curva * s_curva_intensidade
        aceleracao_curva -= 0.0001
        mapa_curva.append(posicao_curva)
    
    tamanho_mapa_curva = len(mapa_curva)
    indice_mapa_curva = -1
    incremento_curva = 2
    direcao_curva = 1
    valor_curva = 0

    while True:
        pygame.time.Clock().tick(30)
        
        for evento in pygame.event.get():
            if evento.type == QUIT:
                pygame.quit()
                sys.exit()

        teclas = pygame.key.get_pressed()
        if teclas[K_UP]:
            posicao_estrada += aceleracao_estrada
            if posicao_estrada >= limite_posicao_textura:
                posicao_estrada = 0
            indice_mapa_curva += incremento_curva
            if indice_mapa_curva >= tamanho_mapa_curva:
                indice_mapa_curva = tamanho_mapa_curva
                incremento_curva *= -1
            elif indice_mapa_curva < -1:
                incremento_curva *= -1
                direcao_curva *= -1

        if teclas[K_LEFT]:
            posicao_carro_x -= 5
        if teclas[K_RIGHT]:
            posicao_carro_x += 5

        posicao_carro_x = max(0, min(posicao_carro_x, LARGURA_TELA - largura_carro))

        posicao_textura = posicao_estrada
        dz = 0
        z = 0
        tela.fill(AZUL)
        for i in range(METADE_ALTURA_TELA, 0, -1):
            if indice_mapa_curva >= i:
                valor_curva = mapa_curva[indice_mapa_curva - i] * direcao_curva
            else:
                valor_curva = 0
            if posicao_textura < metade_limite_posicao_textura:
                tela.blit(faixa_clara, (0, i + METADE_ALTURA_TELA))
                tela.blit(estrada_clara, (valor_curva, i + METADE_ALTURA_TELA), (0, i, LARGURA_TELA, 1))
            else:
                tela.blit(faixa_escura, (0, i + METADE_ALTURA_TELA))
                tela.blit(estrada_escura, (valor_curva, i + METADE_ALTURA_TELA), (0, i, LARGURA_TELA, 1))
            dz += ddz
            z += dz
            posicao_textura += aceleracao_posicao_textura + z
            if posicao_textura >= limite_posicao_textura:
                posicao_textura = 0


        for carro_ia in carros_ia:
            carro_ia.movimentar()
            carro_ia.desenhar(tela)

        tela.blit(imagem_carro, (posicao_carro_x, posicao_carro_y))
        pygame.display.update()

if __name__ == '__main__':
    main()

