import pygame

from IRenderable import IRenderable

from directions import UP, DOWN, LEFT, RIGHT, UP_LEFT, UP_RIGHT, DOWN_LEFT, DOWN_RIGHT
from colors import BLACK


class Tile(IRenderable):
    COUNT = 0

    def __init__(self, image, tilesheet_cfg):
        self.__image = image

        image = pygame.transform.scale(image, (20, 20))
        pixelset = []
        for j in range(image.get_height()):
            pixelset.append([])
            for i in range(image.get_width()):
                pixel = image.get_at((i, j))
                pixelset[j].append(pixel)
        
        self.__pixelset = pixelset
        self.__idx = Tile.COUNT % tilesheet_cfg.tiles_count

        Tile.COUNT += 1
    
    def edge_pixels(self, direction):
        if direction == UP:
            return self.pixelset[0]
        elif direction == DOWN:
            return self.pixelset[-1]
        elif direction == LEFT:
            return list(map(lambda x: x[0], self.__pixelset))
        elif direction == RIGHT:
            return list(map(lambda x: x[-1], self.__pixelset))
        elif direction == UP_LEFT:
            return [self.pixelset[0][0]]
        elif direction == UP_RIGHT:
            return [self.pixelset[0][-1]]
        elif direction == DOWN_LEFT:
            return [self.pixelset[-1][0]]
        elif direction == DOWN_RIGHT:
            return [self.pixelset[-1][-1]]
    
    def render(self, screen, *args, render_cfg=None, **kwargs):
        x, y, size = args

        image = pygame.transform.scale(self.__image, size)
        
        if not kwargs['is_single']:
            rect = image.get_rect(x=x, y=y)

            mouse_pos = pygame.mouse.get_pos()
            if rect.collidepoint(mouse_pos):
                surf = pygame.Surface(size, pygame.SRCALPHA)
                surf.fill((*BLACK, 128))
                
                image.blit(surf, (0, 0))
        
        screen.blit(image, (x, y))
    
    @property
    def image(self):
        return self.__image

    @property
    def pixelset(self):
        return self.__pixelset

    @property
    def idx(self):
        return self.__idx
    
    def __eq__(self, other):
        return self.pixelset == other.pixelset
    
    def __hash__(self):
        return hash(tuple(map(lambda x: tuple(x), self.pixelset)))

    def __repr__(self):
        return f'{self.idx}'
