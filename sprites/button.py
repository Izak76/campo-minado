from utils import borded_rect, vertical_crop
from utils.colors import *
import pygame

class Button(pygame.sprite.Sprite):
    def __init__(self, rect:pygame.Rect, command=None, *, label:str=None, image:str=None):
        super().__init__()

        self.image = pygame.Surface(rect[-2:], pygame.SRCALPHA)
        self.rect = rect

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
            command = lambda: print("Botão pressionado")

        self.command = command

        self.update()
    
    def update(self):
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            borded_rect(self.image, BUTTON_SEL_BG, self.image.get_rect(), 3, BUTTON_SEL_BORDER, 3)
            self.image.blit(self.content2, self.content2.get_rect(center=self.image.get_rect().center))

            for evt in pygame.event.get(pygame.MOUSEBUTTONUP):
                if evt.button == 1:
                    self.command()

        else:
            borded_rect(self.image, BUTTON_BG, self.image.get_rect(), 3, BUTTON_BORDER, 3)
            self.image.blit(self.content1, self.content1.get_rect(center=self.image.get_rect().center))
        