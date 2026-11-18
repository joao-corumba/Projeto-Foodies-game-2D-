import pygame

import config
from src.cenas.cena import Cena
from src.entidades.comida import sprite_comida
from src.gerador_comida import LISTA_JUNK, LISTA_SAUDAVEL
from src.texto import escrever

REGRAS = [
    "A/D ou setas: andar     ESPAÇO/W: pular     J/Z/F: garfo     ESC: pausar",
    "",
    "Comida que encosta em você é comida!",
    "Saudável dá pontos (pegue várias seguidas para combo).",
    "Junk engorda (Normal > Gordo A > B > C): fica mais lento e pula menos.",
    "Comer junk gordo C é fim de jogo — mas dá para rebater junk com o garfo!",
    "Junk que vem pelos lados: pule ou rebata.",
    "Inimigos te perseguem e chefes atiram junk: use o garfo.",
    "Rebata junk de volta no chefe para machucá-lo.",
]


class ComoJogarCena(Cena):
    def __init__(self, gerenciador):
        super().__init__(gerenciador)
        self.titulo = pygame.font.Font(None, 72)
        self.fonte = pygame.font.Font(None, 32)

    def tratar_evento(self, evento):
        if evento.type == pygame.KEYDOWN:
            self.trocar_para("menu")

    def desenhar(self, tela):
        tela.fill(config.FUNDO_MENU)
        escrever(tela, self.titulo, "Como jogar", (config.LARGURA // 2, 60), centro=True)
        for i, linha in enumerate(REGRAS):
            escrever(tela, self.fonte, linha, (80, 110 + i * 32))

        y = 120 + len(REGRAS) * 32
        for titulo, lista, x in (("Saudáveis", LISTA_SAUDAVEL, 80), ("Junk", LISTA_JUNK, 660)):
            escrever(tela, self.fonte, titulo, (x, y), (255, 220, 120))
            for i, (nome, sprite, _) in enumerate(lista):
                cx, cy = x + (i // 6) * 260, y + 40 + (i % 6) * 34
                tela.blit(sprite_comida(sprite, 32), (cx, cy - 4))
                escrever(tela, self.fonte, nome, (cx + 40, cy))
        escrever(tela, self.fonte, "Qualquer tecla para voltar", (config.LARGURA // 2, config.ALTURA - 30),
                 (200, 200, 200), centro=True)
