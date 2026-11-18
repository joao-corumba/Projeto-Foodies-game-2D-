import pygame

import config
from src.cenas.como_jogar import ComoJogarCena
from src.cenas.game_over import GameOverCena
from src.cenas.jogo import JogoCena
from src.cenas.menu import MenuCena
from src.gerenciador_cenas import GerenciadorCenas


def main():
    pygame.init()
    pygame.display.set_caption(config.TITULO)
    tela = pygame.display.set_mode(config.RESOLUCAO)

    gerenciador = GerenciadorCenas(tela, cena_inicial="menu")
    gerenciador.registrar("menu", MenuCena)
    gerenciador.registrar("jogo", JogoCena)
    gerenciador.registrar("game_over", GameOverCena)
    gerenciador.registrar("como_jogar", ComoJogarCena)
    gerenciador.executar()

    pygame.quit()


if __name__ == "__main__":
    main()
