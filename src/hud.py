import pygame

import config
from src.texto import escrever


class HUD:
    def __init__(self):
        self.fonte = pygame.font.Font(None, 36)
        self.fonte_msg = pygame.font.Font(None, 32)
        self.mensagem = None
        self.cor_msg = config.BRANCO
        self.tempo_msg = 0.0

    def mostrar(self, texto, cor=config.BRANCO, duracao=2.5):
        self.mensagem, self.cor_msg, self.tempo_msg = texto, cor, duracao

    def atualizar(self, dt):
        self.tempo_msg = max(0, self.tempo_msg - dt)

    def _escrever(self, tela, texto, pos, cor=config.BRANCO):
        escrever(tela, self.fonte, texto, pos, cor, sombra=True)

    def desenhar(self, tela, jogador, pontuacao, chefe=None):
        for i in range(jogador.vida_maxima):
            cor = (220, 40, 60) if i < jogador.vida else (90, 90, 90)
            pygame.draw.circle(tela, cor, (30 + i * 36, 30), 13)
        cor_forma = config.VERDE if jogador.estagio == 0 else (255, 150, 60)
        self._escrever(tela, jogador.nome_estagio, (30 + jogador.vida_maxima * 36, 18), cor_forma)
        self._escrever(tela, f"Pontos: {pontuacao.pontuacao}", (20, 55))
        self._escrever(tela, f"Recorde: {pontuacao.recorde}", (20, 85))
        if pontuacao.multiplicador > 1:
            self._escrever(tela, f"Combo x{pontuacao.multiplicador}", (20, 115), (255, 200, 60))

        if chefe:
            barra = pygame.Rect(0, 16, 400, 18)
            barra.centerx = config.LARGURA // 2
            pygame.draw.rect(tela, (60, 60, 60), barra)
            pygame.draw.rect(tela, (170, 40, 170), (barra.x, barra.y, barra.w * chefe.vida // chefe.vida_maxima, barra.h))
            pygame.draw.rect(tela, config.PRETO, barra, 2)

        if self.tempo_msg > 0:
            escrever(tela, self.fonte_msg, self.mensagem, (config.LARGURA // 2, config.ALTURA - 40),
                     self.cor_msg, centro=True, sombra=True)
