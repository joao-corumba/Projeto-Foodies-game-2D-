import pygame

import config


class Garfo(pygame.sprite.Sprite):
    def __init__(self, jogador):
        super().__init__()
        self.jogador = jogador
        self.tempo = config.GARFO_DURACAO
        self.acertados = set()
        self.image = pygame.Surface((60, 14))
        self.image.fill((200, 200, 210))
        pygame.draw.rect(self.image, (150, 150, 160), self.image.get_rect(), 2)
        self.rect = self.image.get_rect()
        self._posicionar()

    def _posicionar(self):
        j = self.jogador.rect
        if self.jogador.direcao > 0:
            self.rect.midleft = (j.right - 4, j.centery - 10)
        else:
            self.rect.midright = (j.left + 4, j.centery - 10)

    def update(self, dt):
        self.tempo -= dt
        self._posicionar()
        if self.tempo <= 0:
            self.kill()
