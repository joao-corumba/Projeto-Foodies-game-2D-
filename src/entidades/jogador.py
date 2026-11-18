import pygame

import config
from src.entidades.character_body import CharacterBody
from src.entidades.garfo import Garfo

ESTAGIOS = ["Normal", "Gordo A", "Gordo B", "Gordo C"]
LIMITES_PULO = (-500, 0, 400)
_cache_sprites = None


def carregar_sprites():
    global _cache_sprites
    if _cache_sprites is None:
        pasta = config.SPRITES / "jogador"

        def img(nome):
            return pygame.image.load(pasta / f"{nome}.png").convert_alpha()

        _cache_sprites = {
            "andar": [img("normal_1"), img("normal_2")],
            "pulo": [img(f"pula_{i}") for i in range(1, 5)],
            "gordo": [img(f"gordo_{c}") for c in "abc"],
        }
    return _cache_sprites


class Jogador(CharacterBody):
    HITBOX = (70, 90)

    def __init__(self):
        super().__init__((config.LARGURA // 2, config.CHAO_Y - self.HITBOX[1] / 2), self.HITBOX,
                         vida=config.JOGADOR_VIDA, velocidade=config.JOGADOR_VELOCIDADE)
        self.sprites = carregar_sprites()
        self.pulo = config.JOGADOR_FORCA_PULO
        self.vel_y = 0.0
        self.no_chao = True
        self.andando = False
        self.direcao = 1
        self.invencivel = 0.0
        self.cooldown_ataque = 0.0
        self._tempo_anim = 0.0
        self.image = self.sprites["andar"][0]

    @property
    def estagio(self):
        return min(self.vida_maxima - self.vida, len(ESTAGIOS) - 1)

    @property
    def nome_estagio(self):
        return ESTAGIOS[self.estagio]

    def _fator_peso(self):
        return 1 - config.JOGADOR_PERDA_POR_ESTAGIO * self.estagio

    def input(self, teclas):
        dx = (teclas[pygame.K_RIGHT] or teclas[pygame.K_d]) - (teclas[pygame.K_LEFT] or teclas[pygame.K_a])
        if dx:
            self.direcao = dx
        self.andando = dx != 0
        return dx

    def pular(self):
        if self.no_chao:
            self.vel_y = -self.pulo * self._fator_peso()
            self.no_chao = False

    def atacar(self):
        if self.cooldown_ataque > 0:
            return None
        self.cooldown_ataque = config.GARFO_COOLDOWN
        return Garfo(self)

    def levar_dano(self, quantidade):
        if self.invencivel > 0:
            return False
        self.perder_vida(quantidade)
        self.invencivel = config.JOGADOR_INVENCIBILIDADE
        return True

    def curar(self, quantidade=1):
        self.vida = min(self.vida_maxima, self.vida + quantidade)

    def ao_morrer(self):
        pass

    def _escolher_sprite(self, dt):
        self._tempo_anim += dt
        if self.estagio:
            quadro = self.sprites["gordo"][self.estagio - 1]
        elif not self.no_chao:
            quadro = self.sprites["pulo"][sum(self.vel_y >= limite for limite in LIMITES_PULO)]
        else:
            quadro = self.sprites["andar"][int(self._tempo_anim * 6) % 2 if self.andando else 0]
        self.image = pygame.transform.flip(quadro, True, False) if self.direcao < 0 else quadro

    def update(self, dt):
        dx = self.input(pygame.key.get_pressed())
        meia = self.rect.width / 2
        self.posicao.x = max(meia, min(config.LARGURA - meia,
                                       self.posicao.x + dx * self.velocidade * self._fator_peso() * dt))

        self.vel_y += config.GRAVIDADE * dt
        self.posicao.y += self.vel_y * dt
        chao = config.CHAO_Y - self.rect.height / 2
        if self.posicao.y >= chao:
            self.posicao.y, self.vel_y, self.no_chao = chao, 0, True

        self.invencivel = max(0, self.invencivel - dt)
        self.cooldown_ataque = max(0, self.cooldown_ataque - dt)
        self.sincronizar_rect()
        self._escolher_sprite(dt)

    def desenhar(self, tela):
        if self.invencivel > 0 and int(self.invencivel * 15) % 2:
            return
        tela.blit(self.image, self.image.get_rect(midbottom=(self.rect.centerx, self.rect.bottom + 10)))
