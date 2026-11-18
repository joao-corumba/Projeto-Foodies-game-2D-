import pygame

import config


class GerenciadorCenas:
    def __init__(self, tela, cena_inicial):
        self.tela = tela
        self.relogio = pygame.time.Clock()
        self.rodando = True
        self.dados = {}
        self._cenas = {}
        self._cena_atual = None
        self._proxima = cena_inicial
        self._fonte_debug = pygame.font.Font(None, 24)

    def registrar(self, nome, classe_cena):
        self._cenas[nome] = classe_cena(self)

    def trocar_cena(self, nome):
        if nome not in self._cenas:
            raise KeyError(f"Cena '{nome}' não registrada")
        self._proxima = nome

    def _aplicar_troca(self):
        if self._proxima:
            self._cena_atual = self._cenas[self._proxima]
            self._proxima = None
            self._cena_atual.ao_entrar()

    def executar(self):
        while self.rodando:
            dt = self.relogio.tick(config.FPS) / 1000
            self._aplicar_troca()
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    self.rodando = False
                else:
                    self._cena_atual.tratar_evento(evento)
            self._cena_atual.atualizar(dt)
            self._cena_atual.desenhar(self.tela)
            if config.DEBUG:
                fps = self._fonte_debug.render(f"FPS: {self.relogio.get_fps():.0f}", True, config.BRANCO)
                self.tela.blit(fps, (config.LARGURA - 90, 10))
            pygame.display.flip()
