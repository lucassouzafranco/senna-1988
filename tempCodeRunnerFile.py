tempo_atual = pygame.time.get_ticks()
        tempo_decorrido = (tempo_atual - tempo_inicial) // 1000  # Tempo decorrido em segundos
        cronometro_texto = fonte.render(f"Tempo: {tempo_decorrido}s", True, BRANCO)
        tela.blit(cronometro_texto, (LARGURA_TELA - 150, 10))