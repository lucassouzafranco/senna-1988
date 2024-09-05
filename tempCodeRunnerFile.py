def main():
    pygame.init()

    # Janela do Pygame
    tela = pygame.display.set_mode((LARGURA_TELA, ALTURA_TELA))
    pygame.display.set_caption("Simple Road")
    
    # Carrega as imagens
    estrada_clara = pygame.image.load('./assets/images/light_road.png').convert()
    estrada_escura = pygame.image.load('./assets/images/dark_road.png').convert()
    imagem_carro = pygame.image.load('./assets/images/f1_car_centered.png').convert_alpha()
    imagem_carro_ia = pygame.image.load('./assets/images/enemies_cars.png').convert_alpha()

    largura_carro, altura_carro = imagem_carro.get_size()
    posicao_carro_x = (LARGURA_TELA - largura_carro) // 2
    posicao_carro_y = ALTURA_TELA - altura_carro - 30

    carros_ia = [
        CarroIA(random.randint(240, 380), METADE_ALTURA_TELA - random.randint(20, 40), 0.7, imagem_carro_ia, 0.1),
        CarroIA(random.randint(240, 380), METADE_ALTURA_TELA - random.randint(20, 40), 0.7, imagem_carro_ia, 0.1),
        CarroIA(random.randint(240, 380), METADE_ALTURA_TELA - random.randint(20, 40), 0.7, imagem_carro_ia, 0.1)
    ]

    colisoes = 0

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
    metade_limite_posicao_textura = limite_posicao_textura // 2

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
            
            # Verifica colisão entre o carro do jogador e o carro IA
            rect_carro_jogador = pygame.Rect(posicao_carro_x + 26, posicao_carro_y, largura_carro - 52, altura_carro)
            rect_carro_ia = pygame.Rect(carro_ia.x, carro_ia.y, carro_ia.imagem.get_width(), carro_ia.imagem.get_height())
            
            # Ajuste do retângulo de colisão para ficar próximo da área real do carro
            rect_carro_ia.inflate_ip(-10, -10)
            
            if rect_carro_jogador.colliderect(rect_carro_ia):
                if not carro_ia.collided:
                    colisoes += 1
                    carro_ia.collided = True
            else:
                carro_ia.collided = False  # Moveu para fora do 'if' anterior
            
            carro_ia.desenhar(tela)

        # Atualizar e exibir o contador de colisões
        fonte = pygame.font.SysFont(None, 30)
        contador_texto = fonte.render("Colisões: " + str(colisoes), True, BRANCO)
        tela.blit(contador_texto, (10, 10))

        tela.blit(imagem_carro, (posicao_carro_x, posicao_carro_y))
        pygame.display.update()

if __name__ == '__main__':
    main()
