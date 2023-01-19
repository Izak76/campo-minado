import os
os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = ""

from utils.colors import *
from sprites import *
import pygame


def show_name_button(button:Button):
    font = pygame.font.SysFont("Tahoma", int(height*0.04))
    r = font.render(button.name, True, (255,)*3)
    if r.get_width() > sobra*p:
        r = pygame.transform.smoothscale(r, (sobra*p, sobra*p*r.get_height()/r.get_width()))
    
    screen.blit(r, (dial_x-(1-p)*sobra/2+(sobra-r.get_width())//2, (rb1.y-r.get_height())*0.97))

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

be = (1-p)/2
bw = (sobra*(1-3*be))/3
rb1 = pygame.Rect(0, 0, *(bw,)*2)
rb1.x = minas_pos[0]+minas.get_width()+sobra*be
rb1.y = minas_pos[1]+minas.get_height()-rb1.h*(1+be)
rb2 = rb1.copy()
rb2.left = rb1.right+sobra*(be/2)
rb3 = rb2.copy()
rb3.left = rb2.right+sobra*(be/2)
b1 = Button(rb1, "Ajustes", image="src/gear.png")
b2 = Button(rb2, "Histórico", image="src/history.png")
b3 = Button(rb3, "Opções de jogo", image="src/options.png")
sprites1 = pygame.sprite.Group(tempo, mcount)
sprites2 = pygame.sprite.Group(mf, b1, b2, b3)

while True:
    for evt in pygame.event.get():
        if evt.type == pygame.QUIT:
            pygame.quit()
            exit()

    screen.fill(BACKGROUND_COLOR)

    sprites1.draw(screen)
    sprites2.update(mouse_over_func=show_name_button)
    sprites2.draw(screen)
    pygame.display.flip()