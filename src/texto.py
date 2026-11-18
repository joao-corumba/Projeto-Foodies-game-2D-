import config


def escrever(tela, fonte, texto, pos, cor=config.BRANCO, centro=False, sombra=False):
    img = fonte.render(texto, True, cor)
    rect = img.get_rect(center=pos) if centro else img.get_rect(topleft=pos)
    if sombra:
        tela.blit(fonte.render(texto, True, config.PRETO), rect.move(2, 2))
    tela.blit(img, rect)
