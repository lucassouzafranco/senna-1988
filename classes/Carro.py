import pygame

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
        #Método para detectar colisões
        pass

    def desenhar(self, tela):
        tela.blit(self.imagem, (self.x, self.y)) # Desenha a imagem do carro na tela na posição (x, y)
        
