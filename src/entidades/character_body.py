import pygame

import config


class CharacterBody(pygame.sprite.Sprite):
    def __init__(self, posicao, tamanho, cor=(0, 0, 0, 0), vida=1, velocidade=0):
        super().__init__()
        self.vida = self.vida_maxima = vida
        self.velocidade = velocidade
        self.posicao = pygame.Vector2(posicao)
        self.image = pygame.Surface(tamanho, pygame.SRCALPHA)
        self.image.fill(cor)
        self.rect = self.image.get_rect(center=self.posicao)

    @property
    def vivo(self):
        return self.vida > 0

    def perder_vida(self, quantidade=1):
        self.vida = max(0, self.vida - quantidade)
        if not self.vivo:
            self.ao_morrer()

    def ao_morrer(self):
        self.kill()

    def sincronizar_rect(self):
        self.rect.center = round(self.posicao.x), round(self.posicao.y)

    def fora_da_tela(self, margem=120):
        return not self.rect.colliderect(pygame.Rect(-margem, -margem, config.LARGURA + 2 * margem,
                                                     config.ALTURA + 2 * margem))
