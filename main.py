import pygame, sys, random
from pygame.locals import *

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

class CarroIA:
    def __init__(self, x, y, velocidade, imagem, escala_inicial):
        self.x = x
        self.y = y
        self.velocidade = velocidade
        self.imagem_original = imagem
        self.imagem = pygame.transform.scale(imagem, (int(imagem.get_width() * escala_inicial), int(imagem.get_height() * escala_inicial)))
        self.escala = escala_inicial

    def movimentar(self):
        # Aumenta a escala e a posição vertical conforme o carro se aproxima
        self.escala += 0.01
        self.y += self.velocidade
        self.x -= self.velocidade  # Ajusta a posição horizontal conforme o carro "vem da distância"
        self.imagem = pygame.transform.scale(self.imagem_original, (int(self.imagem_original.get_width() * self.escala), int(self.imagem_original.get_height() * self.escala)))

        # Reseta a posição quando o carro sai da tela
        if self.y > ALTURA_TELA:
            self.reset()

    def reset(self):
        self.escala = 0.1
        self.x = random.randint(0, LARGURA_TELA - int(self.imagem_original.get_width() * self.escala))
        self.y = -random.randint(100, 300)
        self.velocidade = random.randint(3, 6)

    def desenhar(self, tela):
        tela.blit(self.imagem, (self.x, self.y))

def main():
    pygame.init()

    # Janela do Pygame
    tela = pygame.display.set_mode((LARGURA_TELA, ALTURA_TELA))
    pygame.display.set_caption("simple road")
    
    # Carrega as imagens
    estrada_clara = pygame.image.load('./assets/images/light_road.png').convert()
    estrada_escura = pygame.image.load('./assets/images/dark_road.png').convert()
    imagem_carro = pygame.image.load('./assets/images/carro.png').convert_alpha()
    imagem_carro_ia = pygame.image.load('./assets/images/rivals cars.png').convert_alpha()

    # Dimensões e posição inicial do carro
    largura_carro, altura_carro = imagem_carro.get_size()
    posicao_carro_x = (LARGURA_TELA - largura_carro) // 2
    posicao_carro_y = ALTURA_TELA - altura_carro - 30  # Posição do carro na tela

    # Criação dos pilotos IA com uma escala inicial pequena para simular a distância
    carros_ia = [
        CarroIA(random.randint(0, LARGURA_TELA - largura_carro), -random.randint(100, 300), 5, imagem_carro_ia, 0.1),
        CarroIA(random.randint(0, LARGURA_TELA - largura_carro), -random.randint(100, 300), 4, imagem_carro_ia, 0.1),
        CarroIA(random.randint(0, LARGURA_TELA - largura_carro), -random.randint(100, 300), 3, imagem_carro_ia, 0.1)
    ]

    # Superfícies para as tiras de estrada
    faixa_clara = pygame.Surface((LARGURA_TELA, 1)).convert()
    faixa_escura = pygame.Surface((LARGURA_TELA, 1)).convert()
    faixa_clara.fill(estrada_clara.get_at((0, 0)))
    faixa_escura.fill(estrada_escura.get_at((0, 0)))

    # Variáveis de controle
    posicao_textura = 0
    ddz = 0.001
    dz = 0
    z = 0
    posicao_estrada = 0
    aceleracao_estrada = 80
    aceleracao_posicao_textura = 4
    limite_posicao_textura = 300
    metade_limite_posicao_textura = int(limite_posicao_textura / 2)

    # Variáveis para a curva
    posicao_curva = 0
    velocidade_curva = 0
    aceleracao_curva = 0.01
    s_curva_intensidade = 2

    # Mapa da curva
    mapa_curva = []
    for i in range(METADE_ALTURA_TELA):
        velocidade_curva += aceleracao_curva
        posicao_curva += velocidade_curva * s_curva_intensidade
        aceleracao_curva -= 0.0001
        mapa_curva.append(posicao_curva)
    
    # Variáveis de controle da curva
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

        # Controle de movimentação
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

        # Movimento do carro
        if teclas[K_LEFT]:
            posicao_carro_x -= 5
        if teclas[K_RIGHT]:
            posicao_carro_x += 5

        # Limites do carro na tela
        posicao_carro_x = max(0, min(posicao_carro_x, LARGURA_TELA - largura_carro))

        # Desenho da estrada
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

        # Atualiza e desenha os pilotos IA
        for carro_ia in carros_ia:
            carro_ia.movimentar()
            carro_ia.desenhar(tela)

        # Desenha o carro do jogador na tela
        tela.blit(imagem_carro, (posicao_carro_x, posicao_carro_y))

        pygame.display.flip()

if __name__ == "__main__":
    main()
