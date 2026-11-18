from src.pontuacao import Pontuacao


def test_ganhar_pontos(tmp_path):
    p = Pontuacao(tmp_path / "r.json")
    p.ganhar_pontos(10)
    assert p.pontuacao == 10


def test_combo_multiplica_e_quebra(tmp_path):
    p = Pontuacao(tmp_path / "r.json")
    for _ in range(5):
        p.ganhar_pontos(10, combo=True)
    assert p.multiplicador == 2
    p.quebrar_combo()
    assert p.multiplicador == 1


def test_recorde_salvo_e_carregado(tmp_path):
    arq = tmp_path / "r.json"
    p = Pontuacao(arq)
    p.ganhar_pontos(50)
    assert p.salvar_recorde() is True
    assert Pontuacao(arq).recorde == 50
    p.reiniciar()
    p.ganhar_pontos(10)
    assert p.salvar_recorde() is False
