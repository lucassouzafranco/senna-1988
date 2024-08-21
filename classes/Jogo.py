import pygame
import sys

class Jogo:
    def __init__(self, largura=800, altura=600):
        pygame.init()
        
        # Configura a tela do jogo
        self.largura = largura
        self.altura = altura
        self.tela = pygame.display.set_mode((largura, altura))
        pygame.display.set_caption("Fórmula 1")

        # Inicializa os atributos do jogo
        self.carro_jogador = None
        self.pista = None
        self.pilotos_ia = []
        self.ranking = Ranking()
        self.som = Som()
        self.interface = Interface()
        self.dificuldade = 1
        self.nome_jogador = ""
        self.estado_jogo = "iniciado"  # "iniciado", "pausado" ou "encerrado"

    def iniciar_jogo(self):
        # Inicia o jogo.
        self.estado_jogo = "iniciado"
        self.carro_jogador = CarroJogador()
        self.pista = Pista()
        self.pilotos_ia = [PilotoIA() for _ in range(5)]  # Exemplo com 5 pilotos IA
        self.ranking = Ranking()
        self.som.tocar_trilha()
        self.loop_jogo()

    def pausar_jogo(self):
        self.estado_jogo = "pausado"

    def retomar_jogo(self):
        if self.estado_jogo == "pausado":
            self.estado_jogo = "iniciado"
            self.loop_jogo()

    def encerrar_jogo(self):
        pygame.quit()
        sys.exit()

    def atualizar_estado(self):
        """Atualiza o estado do jogo."""
        if self.estado_jogo == "iniciado":
            self.processar_eventos()
            self.atualizar_elementos()
            self.desenhar()
        elif self.estado_jogo == "pausado":
            self.exibir_mensagem("Jogo Pausado")

    def processar_eventos(self):
        # Processa eventos do Pygame.
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                self.encerrar_jogo()
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_p:
                    self.pausar_jogo()
                elif evento.key == pygame.K_r:
                    self.retomar_jogo()

    def atualizar_elementos(self):
        # Atualiza a lógica dos elementos do jogo.
        if self.carro_jogador:
            self.carro_jogador.mover()
        for piloto in self.pilotos_ia:
            piloto.mover()

    def desenhar(self):
        # Desenha todos os elementos na tela.
        self.tela.fill((0, 0, 0))  # Limpa a tela com a cor preta
        if self.pista:
            self.pista.desenhar(self.tela)
        if self.carro_jogador:
            self.carro_jogador.desenhar(self.tela)
        for piloto in self.pilotos_ia:
            piloto.desenhar(self.tela)
        self.interface.desenhar(self.tela)
        pygame.display.flip()  # Atualiza a tela

    def loop_jogo(self):
        # Loop principal do jogo.
        clock = pygame.time.Clock()
        while True:
            self.atualizar_estado()
            clock.tick(60)  # Define a taxa de atualização para 60 frames por segundo