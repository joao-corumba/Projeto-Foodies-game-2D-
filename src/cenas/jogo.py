import pygame

import config
from src.cenas.cena import Cena
from src.entidades.inimigo import Chefe, Inimigo
from src.entidades.jogador import Jogador
from src.gerador_comida import GeradorComida
from src.hud import HUD
from src.pontuacao import Pontuacao
from src.texto import escrever

TECLAS_PULO = (pygame.K_SPACE, pygame.K_w, pygame.K_UP)
TECLAS_ATAQUE = (pygame.K_j, pygame.K_z, pygame.K_f)
TECLAS_PAUSA = (pygame.K_ESCAPE, pygame.K_p)


class JogoCena(Cena):
    def __init__(self, gerenciador):
        super().__init__(gerenciador)
        self.pontuacao = Pontuacao()
        self.hud = HUD()
        self.fonte_pausa = pygame.font.Font(None, 80)
        self.fonte = pygame.font.Font(None, 36)
        self.fundo = self._criar_fundo()
        self.veu = pygame.Surface(config.RESOLUCAO, pygame.SRCALPHA)
        self.veu.fill((0, 0, 0, 150))

    @staticmethod
    def _criar_fundo():
        try:
            img = pygame.image.load(config.SPRITES / "fundo" / "cyberpunk_road.png").convert()
            return pygame.transform.scale(img, config.RESOLUCAO)
        except (pygame.error, FileNotFoundError):
            fundo = pygame.Surface(config.RESOLUCAO)
            fundo.fill(config.FUNDO_JOGO)
            return fundo

    def ao_entrar(self):
        self.jogador = Jogador()
        self.gerador = GeradorComida()
        self.comidas = pygame.sprite.Group()
        self.inimigos = pygame.sprite.Group()
        self.chefes = pygame.sprite.GroupSingle()
        self.garfos = pygame.sprite.Group()
        self.pontuacao.reiniciar()
        self.tempo = 0.0
        self.t_inimigo = config.INTERVALO_INIMIGO
        self.proximo_chefe = config.PONTOS_PRIMEIRO_CHEFE
        self.nivel_chefe = 0
        self.pausado = False

    def tratar_evento(self, evento):
        if evento.type != pygame.KEYDOWN:
            return
        if evento.key in TECLAS_PAUSA:
            self.pausado = not self.pausado
        elif self.pausado:
            if evento.key == pygame.K_m:
                self.trocar_para("menu")
        elif evento.key in TECLAS_PULO:
            self.jogador.pular()
        elif evento.key in TECLAS_ATAQUE and (garfo := self.jogador.atacar()):
            self.garfos.add(garfo)

    def atualizar(self, dt):
        if self.pausado:
            return
        dt = min(dt, config.DT_MAXIMO)
        self.tempo += dt
        self.gerador.dificuldade = 1.0 + self.tempo / 90

        self.jogador.update(dt)
        for grupo in (self.garfos, self.comidas, self.inimigos, self.chefes):
            grupo.update(dt)
        self.gerador.atualizar(dt, self.comidas, com_chefe=bool(self.chefes))
        self.hud.atualizar(dt)

        self._spawnar_inimigos(dt)
        self._colisoes()
        if not self.jogador.vivo:
            self._fim_de_jogo()

    def _spawnar_inimigos(self, dt):
        if self.chefes:
            return
        if self.pontuacao.pontuacao >= self.proximo_chefe:
            self.nivel_chefe += 1
            self.chefes.add(Chefe(self.jogador, self.gerador, self.comidas, self.nivel_chefe))
            self.proximo_chefe += config.INTERVALO_CHEFE
            self.hud.mostrar("Um CHEFE apareceu!", (255, 90, 220))
            return
        self.t_inimigo -= dt
        if self.t_inimigo <= 0:
            self.t_inimigo = max(6, config.INTERVALO_INIMIGO - self.tempo / 20)
            self.inimigos.add(Inimigo(self.jogador, velocidade=150 + self.tempo))

    def _colisoes(self):
        j = self.jogador
        chefe = self.chefes.sprite

        for comida in pygame.sprite.spritecollide(j, self.comidas, False):
            if comida.rebatida:
                continue
            comida.kill()
            if msg := comida.ao_comer(j, self.pontuacao):
                self.hud.mostrar(msg, comida.cor_mensagem)

        for garfo in self.garfos:
            for comida in pygame.sprite.spritecollide(garfo, self.comidas, False):
                if comida.pode_ser_rebatida():
                    comida.rebater(j.direcao)
                    self.pontuacao.ganhar_pontos(config.PONTOS_REBATER)
            alvos = pygame.sprite.spritecollide(garfo, self.inimigos, False)
            if chefe and garfo.rect.colliderect(chefe.rect):
                alvos.append(chefe)
            for alvo in alvos:
                if alvo not in garfo.acertados:
                    garfo.acertados.add(alvo)
                    self._ferir(alvo, j.direcao)

        if chefe:
            for comida in pygame.sprite.spritecollide(chefe, self.comidas, False):
                if comida.rebatida:
                    comida.kill()
                    self._ferir(chefe)

        for inimigo in pygame.sprite.spritecollide(j, self.inimigos, False):
            if j.levar_dano(inimigo.dano):
                self.pontuacao.quebrar_combo()
                inimigo.levar_golpe(0, 1 if inimigo.posicao.x > j.posicao.x else -1)

    def _ferir(self, alvo, direcao=0):
        alvo.levar_golpe(1, direcao)
        if alvo.vivo:
            return
        self.pontuacao.ganhar_pontos(alvo.pontos)
        if isinstance(alvo, Chefe):
            self.jogador.curar(2)
            self.hud.mostrar("Chefe derrotado! Você emagreceu!", config.VERDE)

    def _fim_de_jogo(self):
        novo = self.pontuacao.salvar_recorde()
        self.gerenciador.dados.update(pontuacao=self.pontuacao.pontuacao,
                                      recorde=self.pontuacao.recorde, novo_recorde=novo)
        self.trocar_para("game_over")

    def desenhar(self, tela):
        tela.blit(self.fundo, (0, 0))
        for grupo in (self.comidas, self.inimigos, self.chefes):
            grupo.draw(tela)
        self.jogador.desenhar(tela)
        self.garfos.draw(tela)
        self.hud.desenhar(tela, self.jogador, self.pontuacao, self.chefes.sprite)

        if self.pausado:
            tela.blit(self.veu, (0, 0))
            centro = (config.LARGURA // 2, config.ALTURA // 2)
            escrever(tela, self.fonte_pausa, "PAUSADO", (centro[0], centro[1] - 40), centro=True)
            escrever(tela, self.fonte, "ESC continuar  |  M menu", (centro[0], centro[1] + 30), centro=True)
