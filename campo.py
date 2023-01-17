import os
os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = ""

from utils.colors import *
from sprites import *
import pygame


pygame.init()
pygame.display.set_caption("Campo minado")
pygame.display.set_icon(pygame.image.load("src/bomb.png"))
resolucoes = ((400, 300), (640, 480), (800, 600), (960, 720), (1024, 768))
rp = resolucoes[2] #Resulução padrão
width, height = rp

screen = pygame.display.set_mode(rp)

mf = Minefield(9, rp)
minas = mf.image
minas_pos = mf.rect.topleft

p = 0.8
sobra = width-minas_pos[0]-minas.get_width()
dial_x = minas_pos[0]+minas.get_width()+(1-p)*sobra/2
dial_wh = (sobra*p, sobra*0.3)
tempo = Dial("src/chronometer.png", pygame.Rect(dial_x, minas_pos[1]+height//60, *dial_wh), rp)
mcount = Dial("src/bomb.png", pygame.Rect(dial_x, minas_pos[1]+tempo.rect.height+height//12, *dial_wh), rp)

rb1 = pygame.Rect(0, 0, *(sobra*0.25,)*2)
rb1.x = minas_pos[0]+minas.get_width()+sobra*0.1
rb1.y = minas_pos[1]+minas.get_height()-rb1.h
rb2 = pygame.Rect(rb1.right+sobra*0.1, rb1.y, sobra*0.45, rb1.h)
b1 = Button(rb1, image="src/gear.png")
b2 = Button(rb2, label="Novo jogo")
sprites1 = pygame.sprite.Group(tempo, mcount, mf)
sprites2 = pygame.sprite.Group(mf, b1, b2)

while True:
    for evt in pygame.event.get():
        if evt.type == pygame.QUIT:
            pygame.quit()
            exit()

        elif evt.type == pygame.KEYUP:
            if evt.key == pygame.K_UP:
                tempo.counter += 1

            elif evt.key == pygame.K_DOWN:
                tempo.counter -= 1

    screen.fill(BACKGROUND_COLOR)

    sprites1.draw(screen)
    sprites2.update()
    sprites2.draw(screen)
    pygame.display.flip()
