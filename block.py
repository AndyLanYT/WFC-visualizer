import random
from tile import Tile
from constants import SIDE_PAD, TOP_PAD, BLOCK_WIDTH, BLOCK_HEIGHT, TILES_COUNT_IN_ROW, TILE_WIDTH, TILE_HEIGHT, TILE_GAP


class Block:
    def __init__(self, tileset, x, y):
        self.__tiles = tileset
        
        self.__x = x + SIDE_PAD
        self.__y = y + TOP_PAD
    
    def set_random_tile(self, probabilities):
        self.tiles = random.choices(self.__tiles, [probabilities[tile.idx] for tile in self.__tiles])

    @property
    def tiles(self):
        return self.__tiles
    
    @tiles.setter
    def tiles(self, val):
        if isinstance(val, Tile):
            self.__tiles = [val]
        elif isinstance(val, list):
            self.__tiles = val
        
    @property
    def x(self):
        return self.__x
    
    @property
    def y(self):
        return self.__y

    def render(self, screen):
        if len(self.__tiles) == 1:
            for tile in self.__tiles:
                x = self.__x
                y = self.__y
                size = BLOCK_WIDTH, BLOCK_HEIGHT
                tile.render(screen, x, y, size, True)

        else:
            for tile in self.__tiles:
                x = self.__x + tile.idx % TILES_COUNT_IN_ROW * (TILE_WIDTH + TILE_GAP)
                y = self.__y + tile.idx // TILES_COUNT_IN_ROW * (TILE_HEIGHT + TILE_GAP)
                size = TILE_WIDTH, TILE_HEIGHT

                tile.render(screen, x, y, size)
    
    def __getitem__(self, key):
        for tile in self.__tiles:
            if tile.idx == key:
                return tile
    
    def __setitem__(self, key, val):
        self.__tiles[key] = val
    
    def __len__(self):
        return len(self.__tiles)
    
    def __contains__(self, key):
        if isinstance(key, Tile):
            return key in self.__tiles
        elif isinstance(key, int):
            return key in map(lambda tile: tile.idx, self.__tiles)
    
    def __eq__(self, other):
        return self.__tiles == other.tiles
    
    def __iter__(self):
        return iter(self.__tiles)

    def __repr__(self):
        return str(self.__tiles)
