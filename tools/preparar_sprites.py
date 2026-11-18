import os
from collections import deque
from pathlib import Path

os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
import pygame

RAIZ = Path(__file__).resolve().parent.parent
ORIGEM = RAIZ / "assets"
DESTINO = RAIZ / "assets" / "sprites" / "jogador"
ARQUIVOS = {
    "normal_1": "Boneco NORMAL A1.png",
    "normal_2": "Boneco NORMAL A2.png",
    "pula_1": "Boneco PULA 01.png",
    "pula_2": "Boneco PULA 02.png",
    "pula_3": "Boneco PULA 03.png",
    "pula_4": "Boneco PULA 04 1.png",
    "gordo_a": "Boneco GORDO A.png",
    "gordo_b": "Boneco GORDO B.png",
    "gordo_c": "Boneco GORDO C.png",
}
TOLERANCIA = 40


def quase_branco(cor):
    return all(c >= 255 - TOLERANCIA for c in cor[:3])


def remover_fundo(img):
    img = img.convert_alpha()
    w, h = img.get_size()
    fila = deque((x, y) for x in range(w) for y in (0, h - 1))
    fila.extend((x, y) for y in range(h) for x in (0, w - 1))
    visto = set()
    while fila:
        x, y = fila.popleft()
        if (x, y) in visto or not (0 <= x < w and 0 <= y < h):
            continue
        visto.add((x, y))
        if quase_branco(img.get_at((x, y))):
            img.set_at((x, y), (0, 0, 0, 0))
            fila.extend(((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)))
    return img


def main():
    pygame.init()
    pygame.display.set_mode((1, 1))
    DESTINO.mkdir(parents=True, exist_ok=True)
    for nome, arquivo in ARQUIVOS.items():
        img = remover_fundo(pygame.image.load(ORIGEM / arquivo))
        pygame.image.save(img, DESTINO / f"{nome}.png")
        print("ok", nome)


if __name__ == "__main__":
    main()
