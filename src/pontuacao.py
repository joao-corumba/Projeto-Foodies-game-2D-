import json
from pathlib import Path

ARQUIVO_RECORDE = Path(__file__).resolve().parent.parent / "highscore.json"


class Pontuacao:
    def __init__(self, arquivo=ARQUIVO_RECORDE):
        self.arquivo = Path(arquivo)
        self.recorde = self._carregar_recorde()
        self.reiniciar()

    @property
    def multiplicador(self):
        return 1 + min(self.combo // 5, 3)

    def ganhar_pontos(self, pontos, combo=False):
        if combo:
            self.combo += 1
            pontos *= self.multiplicador
        self.pontuacao += pontos

    def quebrar_combo(self):
        self.combo = 0

    def reiniciar(self):
        self.pontuacao = 0
        self.combo = 0

    def salvar_recorde(self):
        if self.pontuacao <= self.recorde:
            return False
        self.recorde = self.pontuacao
        try:
            self.arquivo.write_text(json.dumps({"recorde": self.recorde}))
        except OSError:
            pass
        return True

    def _carregar_recorde(self):
        try:
            return int(json.loads(self.arquivo.read_text())["recorde"])
        except (OSError, ValueError, KeyError, TypeError):
            return 0
