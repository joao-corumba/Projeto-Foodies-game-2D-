import os

os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
import pygame
import pytest

pygame.init()
pygame.display.set_mode((1, 1))

from src.entidades.comida import ComidaJunk, ComidaSaudavel  # noqa: E402
from src.entidades.jogador import Jogador  # noqa: E402
from src.pontuacao import Pontuacao  # noqa: E402


@pytest.fixture
def pont(tmp_path):
    return Pontuacao(tmp_path / "r.json")


def test_saudavel_da_pontos_e_nao_rebate(pont):
    j = Jogador()
    c = ComidaSaudavel("Maçã", (255, 0, 0), "msg", (0, 0), (0, 0))
    assert not c.pode_ser_rebatida()
    c.ao_comer(j, pont)
    assert pont.pontuacao > 0 and j.vida == j.vida_maxima


def test_junk_tira_vida_com_invencibilidade(pont):
    j = Jogador()
    a = ComidaJunk("Donut", (0, 0, 0), "msg", (0, 0), (0, 0))
    b = ComidaJunk("Refri", (0, 0, 0), "msg", (0, 0), (0, 0))
    a.ao_comer(j, pont)
    b.ao_comer(j, pont)  # ainda invencível
    assert j.vida == j.vida_maxima - 1


def test_junk_rebatida_nao_machuca(pont):
    j = Jogador()
    c = ComidaJunk("Donut", (0, 0, 0), "msg", (0, 0), (0, 0))
    c.rebater(1)
    assert not c.pode_ser_rebatida()
    c.ao_comer(j, pont)
    assert j.vida == j.vida_maxima


def test_junk_engorda_ate_gordo_c(pont):
    j = Jogador()
    assert j.nome_estagio == "Normal"
    for esperado in ("Gordo A", "Gordo B", "Gordo C"):
        j.invencivel = 0
        ComidaJunk("Donut", (0, 0, 0), "msg", (0, 0), (0, 0)).ao_comer(j, pont)
        assert j.nome_estagio == esperado
    j.invencivel = 0
    ComidaJunk("Donut", (0, 0, 0), "msg", (0, 0), (0, 0)).ao_comer(j, pont)
    assert not j.vivo
