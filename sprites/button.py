from utils import borded_rect, vertical_crop
from utils.colors import *
import pygame

class Button(pygame.sprite.Sprite):
    def __init__(self, rect:pygame.Rect, name='', command=None, *, label:str=None, image:str=None):
        super().__init__()

        self.image = pygame.Surface(rect[-2:], pygame.SRCALPHA)
        self.rect = rect
        self.name = name

        if label != None:
            font = pygame.font.SysFont("Tahoma", int(self.image.get_height()))
            for n, cor in enumerate(((255,)*3, (0,)*3), 1):
                content = vertical_crop(font.render(label, True, cor), cor)
                cont_rect = content.get_rect().fit(self.image.get_rect())
                cont_rect.w *= 0.8
                cont_rect.h *= 0.8
                content = pygame.transform.smoothscale(content, cont_rect[-2:])
                setattr(self, f"content{n}", content)

        elif image != None:
            self.content1 = pygame.image.load(image)
            cont_rect = self.content1.get_rect().fit(self.image.get_rect())
            cont_rect.w *= 0.8
            cont_rect.h *= 0.8
            self.content1 = pygame.transform.smoothscale(self.content1, cont_rect[-2:])
            self.content2 = self.content1
            
        else:
            raise AttributeError('Buttton deve ter o atributo "label" ou "image" definido')
        
        if command is None:
            command = lambda: print(f"Botão \"{name}\" pressionado")

        self.command = command

        self.update()
    
    def update(self, *, mouse_over_func=lambda *args: print("Em cima")):
        b = (9*self.rect.w/154.7).__ceil__()
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            borded_rect(self.image, BUTTON_SEL_BG, self.image.get_rect(), b, BUTTON_SEL_BORDER, b)
            self.image.blit(self.content2, self.content2.get_rect(center=self.image.get_rect().center))

            mouse_over_func(self)

            for evt in pygame.event.get(pygame.MOUSEBUTTONUP):
                if evt.button == 1:
                    self.command()

        else:
            borded_rect(self.image, BUTTON_BG, self.image.get_rect(), b, BUTTON_BORDER, b)
            self.image.blit(self.content1, self.content1.get_rect(center=self.image.get_rect().center))
        