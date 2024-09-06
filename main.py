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
METADE_ALTURA_TELA = ALTURA_TELA // 2
LARGURA_ESTRADA = 200  # Largura da estrada

class CarroIA:
    def __init__(self, x, y, velocidade, imagem, escala_inicial):
        self.x = x
        self.y = y
        self.velocidade = velocidade
        self.imagem_original = imagem
        self.escala = escala_inicial
        self.imagem = pygame.transform.scale(
            imagem, 
            (int(imagem.get_width() * self.escala), int(imagem.get_height() * self.escala))
        )
        self.direcao = random.choice([-1, 1])  # Direção inicial para mover-se lateralmente
        self.movimento_lateral = random.randint(1, 3)  # Velocidade do movimento lateral
        self.frequencia_mudanca = random.randint(30, 100)  # Frequência para mudar a direção lateral
        self.contador_mudanca = 0
        self.collided = False  # Inicializa o atributo collided

    def movimentar(self):
        # Movimento vertical
        self.y += self.velocidade
        
        # Movimento lateral
        self.contador_mudanca += 1
        if self.contador_mudanca >= self.frequencia_mudanca:
            self.direcao *= -1  # Muda a direção do movimento lateral
            self.contador_mudanca = 0

        self.x += self.direcao * self.movimento_lateral
        
        # Restrições para que o carro não saia da estrada
        self.x = max(240, min(self.x, 380))
        
        # Se o carro sai da tela, reinicie sua posição
        if self.y > ALTURA_TELA:
            self.reset()
        
        # Ajuste da escala
        if self.escala < 1.0:
            self.escala += 0.01
        
        self.imagem = pygame.transform.scale(
            self.imagem_original, 
            (int(self.imagem_original.get_width() * self.escala), int(self.imagem_original.get_height() * self.escala))
        )

    def reset(self):
        self.escala = 0.2
        self.y = METADE_ALTURA_TELA - random.randint(20, 50)
        self.velocidade = random.randint(3, 6)
        self.x = random.randint(240, 380)
        self.direcao = random.choice([-1, 1])
        self.movimento_lateral = random.randint(1, 3)
        self.frequencia_mudanca = random.randint(30, 100)
        self.contador_mudanca = 0
        self.collided = False  # Redefine o estado de colisão

    def desenhar(self, tela):
        tela.blit(self.imagem, (self.x, self.y))

def desenhar_estrada(tela):
    pass 

def main():
    pygame.init()

    # Janela do Pygame
    tela = pygame.display.set_mode((LARGURA_TELA, ALTURA_TELA))
    pygame.display.set_caption("Simple Road")
    
    # Carrega as imagens
    estrada_clara = pygame.image.load('./assets/images/light_road.png').convert()
    estrada_escura = pygame.image.load('./assets/images/dark_road.png').convert()
    imagem_carro = pygame.image.load('./assets/images/centered_player_car.png.').convert_alpha()
    imagem_carro_ia = pygame.image.load('./assets/images/enemies_car_1.png').convert_alpha()

    largura_carro, altura_carro = imagem_carro.get_size()
    posicao_carro_x = (LARGURA_TELA - largura_carro) // 2
    posicao_carro_y = ALTURA_TELA - altura_carro - 30

    carros_ia = [
        CarroIA(random.randint(240, 380), METADE_ALTURA_TELA - random.randint(20, 40), 1, imagem_carro_ia, 0.01),
        CarroIA(random.randint(240, 380), METADE_ALTURA_TELA - random.randint(20, 40), 1, imagem_carro_ia, 0.01),
        CarroIA(random.randint(240, 380), METADE_ALTURA_TELA - random.randint(20, 40), 1, imagem_carro_ia, 0.01)
    ]

    colisoes = 0
    tempo_inicial = pygame.time.get_ticks()  # Tempo inicial do jogo    

    faixa_clara = pygame.Surface((LARGURA_TELA, 1)).convert()
    faixa_escura = pygame.Surface((LARGURA_TELA, 1)).convert()
    faixa_clara.fill(estrada_clara.get_at((0, 0)))
    faixa_escura.fill(estrada_escura.get_at((0, 0)))

    posicao_textura = 0
    dz = 0
    z = 0
    posicao_estrada = 0
    aceleracao_estrada = 80
    aceleracao_posicao_textura = 4
    limite_posicao_textura = 300
    metade_limite_posicao_textura = limite_posicao_textura // 2

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
            if posicao_textura < metade_limite_posicao_textura:
                tela.blit(faixa_clara, (0, i + METADE_ALTURA_TELA))
                tela.blit(estrada_clara, (0, i + METADE_ALTURA_TELA), (0, i, LARGURA_TELA, 1))
            else:
                tela.blit(faixa_escura, (0, i + METADE_ALTURA_TELA))
                tela.blit(estrada_escura, (0, i + METADE_ALTURA_TELA), (0, i, LARGURA_TELA, 1))
            dz += 0.001
            z += dz
            posicao_textura += aceleracao_posicao_textura + z
            if posicao_textura >= limite_posicao_textura:
                posicao_textura = 0

        for carro_ia in carros_ia:
            carro_ia.movimentar()
            rect_carro_jogador = pygame.Rect(posicao_carro_x + 26, posicao_carro_y, largura_carro - 52, altura_carro)
            rect_carro_ia = pygame.Rect(carro_ia.x, carro_ia.y, carro_ia.imagem.get_width(), carro_ia.imagem.get_height())
            rect_carro_ia.inflate_ip(-20, -20)
            if rect_carro_jogador.colliderect(rect_carro_ia):
                if not carro_ia.collided:
                    colisoes += 1
                    carro_ia.collided = True
                    if colisoes >= 7:
                        # O jogador perdeu o jogo
                        fonte = pygame.font.SysFont(None, 50)
                        mensagem_derrota = font.render("Você perdeu!", True, VERMELHO, PRETO)
                        tela.blit(mensagem_derrota, (LARGURA_TELA // 2 - mensagem_derrota.get_width() // 2, ALTURA_TELA // 2 - mensagem_derrota.get_height() // 2))
                        pygame.display.update()
                        pygame.time.delay(2000)  # Aguarda 2 segundos
                        pygame.quit()
                        sys.exit()
            else:
                carro_ia.collided = False  # Reseta o estado de colisão se não houver colisão

            carro_ia.desenhar(tela)

        # Exibir contador de colisões
        fonte = pygame.font.SysFont(None, 30)
        contador_texto = fonte.render("Colisões: " + str(colisoes), True, BRANCO)
        tela.blit(contador_texto, (10, 10))

        # Exibir cronômetro
        tempo_atual = pygame.time.get_ticks() - tempo_inicial
        tempo_restante = 60000 - tempo_atual

        if tempo_restante <= 0:
            # O jogador ganhou o jogo
            fonte = pygame.font.SysFont(None, 50)
            mensagem_vitoria = fonte.render("Você ganhou!", True, VERDE)
            tela.blit(mensagem_vitoria, (LARGURA_TELA // 2 - mensagem_vitoria.get_width() // 2, ALTURA_TELA // 2 - mensagem_vitoria.get_height() // 2))
            pygame.display.update()
            pygame.time.delay(2000)  # Aguarda 2 segundos
            pygame.quit()
            sys.exit()
        else:
            # Exibir o tempo restante
            segundos_restantes = tempo_restante // 1000
            fonte = pygame.font.SysFont(None, 30)
            tempo_texto = fonte.render("Tempo até a linha de chegada: " + str(segundos_restantes) + "s", True, BRANCO)
            tela.blit(tempo_texto, (LARGURA_TELA - tempo_texto.get_width() - 10, 10))

        tela.blit(imagem_carro, (posicao_carro_x, posicao_carro_y))
        pygame.display.update()

if __name__ == '__main__':
    main()
