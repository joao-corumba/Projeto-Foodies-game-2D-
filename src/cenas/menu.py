import pygame

import config
from src.cenas.cena import Cena
from src.texto import escrever


class MenuCena(Cena):
    def __init__(self, gerenciador):
        super().__init__(gerenciador)
        self.fonte_titulo = pygame.font.Font(None, 96)
        self.fonte = pygame.font.Font(None, 40)
        self.acoes = {pygame.K_RETURN: "jogo", pygame.K_SPACE: "jogo", pygame.K_c: "como_jogar"}

    def tratar_evento(self, evento):
        if evento.type != pygame.KEYDOWN:
            return
        if evento.key == pygame.K_ESCAPE:
            self.sair()
        elif evento.key in self.acoes:
            self.trocar_para(self.acoes[evento.key])

    def desenhar(self, tela):
        tela.fill(config.FUNDO_MENU)
        centro_x, centro_y = config.LARGURA // 2, config.ALTURA // 2
        escrever(tela, self.fonte_titulo, config.TITULO, (centro_x, centro_y - 60), centro=True)
        escrever(tela, self.fonte, "ENTER jogar  |  C como jogar  |  ESC sair", (centro_x, centro_y + 40), centro=True)
