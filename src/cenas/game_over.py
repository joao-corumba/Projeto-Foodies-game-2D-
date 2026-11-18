import pygame

import config
from src.cenas.cena import Cena
from src.texto import escrever


class GameOverCena(Cena):
    def __init__(self, gerenciador):
        super().__init__(gerenciador)
        self.fonte_grande = pygame.font.Font(None, 100)
        self.fonte = pygame.font.Font(None, 42)

    def tratar_evento(self, evento):
        if evento.type == pygame.KEYDOWN:
            if evento.key in (pygame.K_RETURN, pygame.K_SPACE):
                self.trocar_para("jogo")
            elif evento.key == pygame.K_ESCAPE:
                self.trocar_para("menu")

    def desenhar(self, tela):
        tela.fill((50, 20, 30))
        d = self.gerenciador.dados
        x = config.LARGURA // 2
        escrever(tela, self.fonte_grande, "FIM DE JOGO", (x, 200), (255, 120, 120), centro=True)
        linhas = [(f"Pontuação: {d.get('pontuacao', 0)}", config.BRANCO),
                  (f"Recorde: {d.get('recorde', 0)}", config.BRANCO)]
        if d.get("novo_recorde"):
            linhas.append(("NOVO RECORDE!", (255, 220, 80)))
        linhas.append(("ENTER jogar de novo  |  ESC menu", (200, 200, 200)))
        for i, (texto, cor) in enumerate(linhas):
            escrever(tela, self.fonte, texto, (x, 290 + i * 60), cor, centro=True)
