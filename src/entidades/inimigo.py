import math
import random

import pygame

import config
from src.entidades.character_body import CharacterBody


class Inimigo(CharacterBody):
    pontos = config.PONTOS_INIMIGO
    dano = 1

    def __init__(self, jogador, vida=2, velocidade=150, tamanho=(56, 56), cor=(170, 60, 60), posicao=None):
        if posicao is None:
            posicao = (random.choice((-40, config.LARGURA + 40)), config.CHAO_Y - tamanho[1] / 2)
        super().__init__(posicao, tamanho, cor, vida, velocidade)
        self.jogador = jogador
        self.empurrao = 0.0
        w, h = tamanho
        for x in (w // 3, 2 * w // 3):
            pygame.draw.circle(self.image, config.BRANCO, (x, h // 3), 6)

    def levar_golpe(self, dano=1, direcao=1):
        self.empurrao = 500 * direcao
        self.perder_vida(dano)

    def update(self, dt):
        if self.empurrao:
            self.posicao.x += self.empurrao * dt
            self.empurrao = self.empurrao * 0.85 if abs(self.empurrao) > 20 else 0
        else:
            distancia = self.jogador.posicao.x - self.posicao.x
            if abs(distancia) > 4:
                self.posicao.x += math.copysign(self.velocidade * dt, distancia)
        self.sincronizar_rect()


class Chefe(Inimigo):
    pontos = config.PONTOS_CHEFE

    def __init__(self, jogador, gerador, grupo_comidas, nivel=1):
        super().__init__(jogador, vida=10 + 5 * nivel, velocidade=160 + 20 * nivel, tamanho=(140, 110),
                         cor=(120, 40, 120), posicao=(config.LARGURA // 2, 110))
        self.atirador = gerador
        self.grupo_comidas = grupo_comidas
        self.intervalo_tiro = max(0.5, 1.6 - 0.2 * nivel)
        self.recarga = self.intervalo_tiro
        self.sentido = 1

    def atirar_comida(self):
        self.grupo_comidas.add(self.atirador.gerar_comida_junk(self.rect.midbottom, self.jogador.posicao, 380))

    def levar_golpe(self, dano=1, direcao=1):
        self.perder_vida(dano)

    def update(self, dt):
        self.posicao.x += self.sentido * self.velocidade * dt
        if not 100 < self.posicao.x < config.LARGURA - 100:
            self.sentido *= -1
        self.recarga -= dt
        if self.recarga <= 0:
            self.atirar_comida()
            self.recarga = self.intervalo_tiro
        self.sincronizar_rect()
