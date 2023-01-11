from utils.colors import *
from utils import borded_rect
import pygame

class Minefield(pygame.sprite.Sprite):
    def __init__(self, n, screen_size):
        super().__init__()
        
        width, height = screen_size
        self.screen_size = screen_size
        self.n = n
        self.image = pygame.Surface(((height-width//20)//n*n,)*2)
        l = self.image.get_width()//n
        self.rect = self.image.get_rect(topleft=((height-self.image.get_height())/2,)*2)

        self.positions = [[None for _ in range(n)] for _ in range(n)]
        for y in range(n):
            for x in range(n):
                self.positions[y][x] = pygame.Rect(l*y, l*x, l, l)
    
    def update(self):
        img_pos = self.rect.topleft
        mouse_pos = pygame.mouse.get_pos()

        for y in range(self.n):
            for x in range(self.n):
                pos = self.positions[y][x]
                x_, y_, w_, h_ = pos
                cor = DEFAULT_SQUARE_COLOR
                mpx, mpy = mouse_pos
                mpx -= img_pos[0]
                mpy -= img_pos[1]

                if (x_ < mpx < x_+w_) and (y_ < mpy < y_+h_):
                    cor = SELECTED_SQUARE_COLOR

                borded_rect(self.image, cor, pos, self.screen_size[0]//400)
