from abc import ABC, abstractmethod


class Cena(ABC):
    def __init__(self, gerenciador):
        self.gerenciador = gerenciador

    def ao_entrar(self):
        pass

    def tratar_evento(self, evento):
        pass

    def atualizar(self, dt):
        pass

    @abstractmethod
    def desenhar(self, tela):
        ...

    def trocar_para(self, nome):
        self.gerenciador.trocar_cena(nome)

    def sair(self):
        self.gerenciador.rodando = False
