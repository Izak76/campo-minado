import os
os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = ""

import pygame as pg

def borded_rect(surface, color, rect, border_width=0, border_color=(0, 0, 0), border_radius=-1):
    rect = pg.Rect(*rect)

    if isinstance(border_radius, int):
        border_radius = (border_radius,)
    
    elif len(border_radius) == 4:
        border_radius = (-1,)+tuple(border_radius)

    else:
        raise AttributeError("Atributo \"border_radius\" deve ser um inteiro ou uma tupla de 4 inteiros")
    
    if border_width > 0:
        pg.draw.rect(surface, color, rect, 0, *border_radius)
        pg.draw.rect(surface, border_color, rect, border_width, *border_radius)
    
    elif border_width == 0:
        pg.draw.rect(surface, color, rect, 0, *border_radius)
    
    else:
        return pg.Rect(rect.left, rect.top, 0, 0)

    return rect

def vertical_crop(surface:pg.Surface, color=(0, 0, 0)) -> pg.Surface:
    width = surface.get_width()
    height = surface.get_height()
    n = width*4
    c = (bytes(color)+b'\0')*width
    raw = pg.image.tostring(surface, "RGBA")

    for a, b in zip(range(0, len(raw), n), range(n, len(raw), n)):
        if raw[a:b] != c:
            raw = raw[a:]
            break
        else:
            height -= 1

    for a, b in zip(range(len(raw)-n, -1, -n), range(len(raw), -1, -n)):
        if raw[a:b] != c:
            raw = raw[:b]
            break
        else:
            height -= 1

    return pg.image.fromstring(raw, (width, height), "RGBA")
