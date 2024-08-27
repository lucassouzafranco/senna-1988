import pygame
import random

class Carro:
    def __init__(self, x=0, y=0, velocidade=0, aceleracao=0, freio=0, direcao=0, sensibilidade=1):
        self.x = x
        self.y = y
        self.velocidade = velocidade
        self.aceleracao = aceleracao
        self.freio = freio
        self.direcao = direcao
        self.sensibilidade = sensibilidade
        self.imagem = pygame.Surface((50, 30))  # Superfície para o carro
        self.imagem.fill((255, 0, 0))  # Cor do carro para visualização

    def acelerar(self):
        self.velocidade += self.aceleracao

    def frear(self):
        self.velocidade -= self.freio
        if self.velocidade < 0:
            self.velocidade = 0

    def mover(self):
        self.x += self.velocidade * pygame.math.cos(self.direcao)
        self.y += self.velocidade * pygame.math.sin(self.direcao)

    def detectar_colisao(self):
        # Método para detectar colisões
        pass

    def desenhar(self, tela):
        tela.blit(self.imagem, (self.x, self.y)) # Desenha a imagem do carro na tela na posição (x, y)
        
class CarroJogador(Carro):
    def __init__(self, x=0, y=0, velocidade=0, aceleracao=0, freio=0, direcao=0, sensibilidade=1):
        super().__init__(x, y, velocidade, aceleracao, freio, direcao, sensibilidade)
        # Aqui você pode adicionar atributos específicos para o carro do jogador

    def mover(self):
        # Método para mover o carro do jogador com base na entrada do teclado.
        teclas = pygame.key.get_pressed()
        if teclas[pygame.K_UP]:
            self.acelerar()
        if teclas[pygame.K_DOWN]:
            self.frear()
        if teclas[pygame.K_LEFT]:
            self.direcao -= 0.1 
        if teclas[pygame.K_RIGHT]:
            self.direcao += 0.1
        super().mover()

class CarroIA(Carro):
    def __init__(self, x=0, y=0, velocidade=0, aceleracao=0, freio=0, direcao=0, sensibilidade=1, nivel_dificuldade=1):
        super().__init__(x, y, velocidade, aceleracao, freio, direcao, sensibilidade)
        self.nivel_dificuldade = nivel_dificuldade

    def movimentar(self):
        # Depois adicionar o algoritmo para movimentação dos pilotos IA
        self.acelerar()
        if random.random() < 0.1 * self.nivel_dificuldade:
            self.direcao += random.uniform(-0.1, 0.1)  # Mudança aleatória na direção
        super().mover()
