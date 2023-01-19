from utils import borded_rect, vertical_crop
from utils.colors import *
import pygame

class Dial(pygame.sprite.Sprite):
    def __init__(self, icon, rect, scr_size):
        super().__init__()

        self.scr_width, self.scr_height = scr_size
        self.image = pygame.Surface(rect[2:], pygame.SRCALPHA)
        self.icon = pygame.transform.smoothscale(pygame.image.load(icon), (min(rect[2:]),)*2)
        self.dial = pygame.Surface((self.image.get_width()-self.icon.get_width(), self.image.get_height()), pygame.SRCALPHA)
        self.font = pygame.font.SysFont("Tahoma", int(self.dial.get_height()*0.6))
        self.rect = rect

        self.image.blit(self.icon, (0, 0))
        self.counter = 0
    
    @property
    def counter(self):
        return self.__counter
    
    @counter.setter
    def counter(self, value):
        self.__counter = value
        txtcolor = (0, 0, 0)
        rv = vertical_crop(self.font.render(str(value), True, txtcolor), txtcolor)
        rv_pos = rv.get_rect(center=self.dial.get_rect().center)
        borded_rect(self.dial, DIAL_COLOR, (0, 0, self.dial.get_width(), self.dial.get_height()), self.scr_width//200, DIAL_BORDER_COLOR, self.scr_width//160)
        self.dial.blit(rv, rv_pos)
        self.image.blit(self.dial, (self.icon.get_width(), 0))