import random

import pygame

import config
from src.entidades.comida import ComidaJunk, ComidaJunkAgressiva, ComidaSaudavel

LISTA_SAUDAVEL = [
    ("Maçã", "maca", "Maçã tem fibras que ajudam a digestão!"),
    ("Pera", "pera", "Pera tem muita água e fibras!"),
    ("Uva", "uva", "Uva dá energia rápida e saudável!"),
    ("Banana", "banana", "Banana tem potássio, bom para os músculos!"),
    ("Salada", "salada", "Salada tem vitaminas e minerais!"),
    ("Água de coco", "agua_de_coco", "Água de coco hidrata o corpo!"),
    ("Amora", "amora", "Amora tem antioxidantes que protegem o corpo!"),
    ("Laranja", "laranja", "Laranja tem vitamina C, que fortalece a imunidade!"),
]
LISTA_JUNK = [
    ("Hambúrguer", "hamburguer", "Muita gordura cansa o corpo!"),
    ("Pizza", "pizza", "Pizza todo dia tem gordura e sal demais!"),
    ("Refri", "refri", "Refrigerante tem muito açúcar!"),
    ("Donut", "donut", "Doce demais estraga os dentes!"),
    ("Sorvete", "sorvete", "Sorvete é gostoso, mas tem muito açúcar!"),
    ("Frango frito", "frango_frito", "Fritura tem muito óleo!"),
    ("Cupcake", "cupcake", "Cobertura doce é puro açúcar!"),
    ("Cachorro-quente", "cachorro_quente", "Salsicha tem muito sódio!"),
    ("Pirulito", "pirulito", "Pirulito gruda açúcar nos dentes!"),
    ("Picolé", "picole", "Picolé industrializado tem corantes e açúcar!"),
    ("Chocolate", "chocolate", "Chocolate em excesso engorda!"),
    ("Bala", "bala", "Bala é só açúcar, sem nutrientes!"),
]


class GeradorComida:
    def __init__(self, range_horizontal=(40, config.LARGURA - 40)):
        self.lista_saudavel = LISTA_SAUDAVEL
        self.lista_junk = LISTA_JUNK
        self.range_horizontal = range_horizontal
        self.dificuldade = 1.0
        self._t_queda = 0.0
        self._t_lateral = 4.0

    def _topo_aleatorio(self):
        return random.randint(*self.range_horizontal), -30

    def _queda(self):
        return 0, random.uniform(160, 260) * self.dificuldade

    def gerar_comida_saudavel(self):
        return ComidaSaudavel(*random.choice(self.lista_saudavel), self._topo_aleatorio(), self._queda())

    def gerar_comida_junk(self, origem=None, alvo=None, velocidade=None):
        dados = random.choice(self.lista_junk)
        if origem is None:
            return ComidaJunk(*dados, self._topo_aleatorio(), self._queda())
        direcao = pygame.Vector2(alvo) - origem
        direcao = direcao.normalize() if direcao.length_squared() else pygame.Vector2(0, 1)
        return ComidaJunk(*dados, origem, direcao * velocidade)

    def gerar_junk_agressiva(self):
        lado = random.choice((1, -1))
        x = -30 if lado > 0 else config.LARGURA + 30
        vel = random.uniform(260, 360) * self.dificuldade * lado
        return ComidaJunkAgressiva(*random.choice(self.lista_junk), (x, config.CHAO_Y - 22), (vel, 0))

    def atualizar(self, dt, grupo, com_chefe=False):
        fator = 0.5 if com_chefe else 1.0
        self._t_queda -= dt * self.dificuldade * fator
        if self._t_queda <= 0:
            self._t_queda = random.uniform(0.6, 1.2)
            saudavel = random.random() < (0.7 if com_chefe else 0.55)
            grupo.add(self.gerar_comida_saudavel() if saudavel else self.gerar_comida_junk())

        self._t_lateral -= dt * fator
        if self._t_lateral <= 0:
            self._t_lateral = random.uniform(3.5, 7.0) / self.dificuldade
            grupo.add(self.gerar_junk_agressiva())
