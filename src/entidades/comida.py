from abc import ABC, abstractmethod

import pygame

import config
from src.entidades.character_body import CharacterBody

_cache_sprites = {}


def sprite_comida(nome_arquivo, tamanho=config.TAMANHO_COMIDA):
    chave = (nome_arquivo, tamanho)
    if chave not in _cache_sprites:
        img = pygame.image.load(config.SPRITES / "comidas" / f"{nome_arquivo}.png").convert_alpha()
        _cache_sprites[chave] = pygame.transform.scale(img, (tamanho, tamanho))
    return _cache_sprites[chave]


class Comida(CharacterBody, ABC):
    cor_mensagem = config.BRANCO
    rebatida = False

    def __init__(self, nome, visual, mensagem, posicao, vel, tamanho=config.TAMANHO_COMIDA):
        super().__init__(posicao, (tamanho, tamanho))
        self.nome = nome
        self.mensagem = mensagem
        self.vel = pygame.Vector2(vel)
        if isinstance(visual, str):
            self.image = sprite_comida(visual, tamanho).copy()
        else:
            pygame.draw.circle(self.image, visual, (tamanho // 2, tamanho // 2), tamanho // 2)

    @abstractmethod
    def ao_comer(self, jogador, pontuacao):
        ...

    def pode_ser_rebatida(self):
        return False

    def update(self, dt):
        self.posicao += self.vel * dt
        self.sincronizar_rect()
        if self.rect.top >= config.CHAO_Y or self.fora_da_tela():
            self.kill()


class ComidaSaudavel(Comida):
    cor_mensagem = config.VERDE

    def ao_comer(self, jogador, pontuacao):
        pontuacao.ganhar_pontos(config.PONTOS_SAUDAVEL, combo=True)
        return self.mensagem


class ComidaJunk(Comida):
    cor_mensagem = config.VERMELHO
    dano = config.DANO_JUNK

    def pode_ser_rebatida(self):
        return not self.rebatida

    def rebater(self, direcao):
        self.rebatida = True
        self.vel.update(450 * direcao, -700)
        self.image.set_alpha(160)

    def ao_comer(self, jogador, pontuacao):
        if self.rebatida or not jogador.levar_dano(self.dano):
            return None
        pontuacao.quebrar_combo()
        return self.mensagem

    def update(self, dt):
        if self.rebatida:
            self.vel.y += config.GRAVIDADE * 0.3 * dt
        super().update(dt)


class ComidaJunkAgressiva(ComidaJunk):
    pass
