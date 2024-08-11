import math
import random

from index import Index
from tile import Tile
from block import Block

from IRenderable import IRenderable

from directions import *


class WaveFunction(IRenderable):
    def __init__(self, tile_images, tilesheet_cfg, render_cfg):
        self.size = render_cfg.output_size
        
        self.__coeffs = []
        for i in range(self.size[1]):
            self.__coeffs.append([])
            for j in range(self.size[0]):
                # tileset = list(map(Tile, tile_images))
                tileset = [Tile(img, tilesheet_cfg) for img in tile_images]

                x = j * (render_cfg.block_width + render_cfg.block_gap)
                y = i * (render_cfg.block_width + render_cfg.block_gap)
                
                block = Block(tileset, x, y, render_cfg)
                self.__coeffs[i].append(block)
        
        # self.__tileset = list(map(Tile, tile_images))
        self.__tileset = [Tile(img, tilesheet_cfg) for img in tile_images]
        self.probabilities = {tile.idx: 1 / len(tileset) for tile in tileset}
        self.index = Index(tileset)
        self.__stack = []

        self.__collapse_gen = None
    
    def __entropy(self, pos):
        block = self.block_at_pos(pos)
        if len(block) == 1:
            return 0
        
        return -sum([self.probabilities[tile.idx] * math.log(self.probabilities[tile.idx], 2) for tile in block]) - random.uniform(0, 0.1)
    
    def __min_entropy_pos(self):
        min_entropy = None
        pos = None

        for y in range(self.size[1]):
            for x in range(self.size[0]):
                entropy = self.__entropy((x, y))
                if entropy != 0 and (min_entropy is None or min_entropy > entropy):
                    min_entropy = entropy
                    pos = x, y
        
        return pos
    
    def __valid_directions(self, pos):
        x, y = pos

        directions = []
        if x == 0:
            directions += [RIGHT]

            if y == 0:
                directions += [DOWN, DOWN_RIGHT]
            elif y == self.size[1] - 1:
                directions += [UP, UP_RIGHT]
            else:
                directions += [DOWN, DOWN_RIGHT, UP, UP_RIGHT]
        elif x == self.size[0] - 1:
            directions += [LEFT]

            if y == 0:
                directions += [DOWN, DOWN_LEFT]
            elif y == self.size[1] - 1:
                directions += [UP, UP_LEFT]
            else:
                directions += [DOWN, DOWN_LEFT, UP, UP_LEFT]
        else:
            directions += [LEFT, RIGHT]

            if y == 0:
                directions += [DOWN, DOWN_LEFT, DOWN_RIGHT]
            elif y == self.size[1] - 1:
                directions += [UP, UP_LEFT, UP_RIGHT]
            else:
                directions += [DOWN, DOWN_LEFT, DOWN_RIGHT, UP, UP_LEFT, UP_RIGHT]

        return directions
    
    def is_collapsed(self):
        for row in self.__coeffs:
            for block in row:
                if len(block) > 1:
                    return False
        
        return True
    
    def block_at_pos(self, pos):
        col, row = pos
        return self.__coeffs[row][col]
    
    def __observe(self):
        pos = self.__min_entropy_pos()
        if pos is None:
            return
        
        block = self.block_at_pos(pos)
        block.set_random_tile(self.probabilities)

        self.add_to_stack(pos)
    
    def __propagate(self):
        while len(self.__stack) != 0:
            pos = self.__stack.pop()
            block = self.block_at_pos(pos)

            for direction in self.__valid_directions(pos):
                adjacent_pos = pos[0] + direction[0], pos[1] + direction[1]
                adjacent_block = self.block_at_pos(adjacent_pos)

                is_changed = False
                for neighbor in adjacent_block.tiles[:]:
                    if len(adjacent_block) == 1:
                        break
                    
                    if True not in [self.index.is_possible_neighbor(tile, neighbor, direction) for tile in block]:
                        adjacent_block.tiles.remove(neighbor)
                        is_changed = True

                        yield

                if is_changed:
                    self.add_to_stack(adjacent_pos)

    def add_to_stack(self, pos):
        self.__stack.append(pos)
    
    def __collapse(self):
        while not self.is_collapsed():
            propagation_gen = self.__propagate()
            propagation = True
            
            while propagation:
                try:
                    next(propagation_gen)
                    yield
                except StopIteration:
                    propagation = False

            self.__observe()
            yield
    
    def propagate(self):
        self.__collapse_gen = self.__propagate()

    def collapse(self):
        self.__collapse_gen = self.__collapse()
    
    def update(self):
        next(self.__collapse_gen)
    
    def render(self, screen, render_cfg=None, *args, **kwargs):
        for row in self.__coeffs:
            for block in row:
                block.render(screen, render_cfg)
    
    def renovate(self, tilesheet_cfg, render_cfg):
        self.__collapse_gen = None
        tile_images = list(map(lambda tile: tile.image, self.__tileset))
        
        self.__coeffs = []
        for i in range(self.size[1]):
            self.__coeffs.append([])
            for j in range(self.size[0]):
                tileset = [Tile(img, tilesheet_cfg) for img in tile_images]

                x = j * (render_cfg.block_width + render_cfg.block_gap)
                y = i * (render_cfg.block_height + render_cfg.block_gap)
                
                block = Block(tileset, x, y, render_cfg)
                self.__coeffs[i].append(block)

    @property
    def coeffs(self):
        return self.__coeffs
