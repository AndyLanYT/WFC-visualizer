import random

from tile import Tile

from IRenderable import IRenderable


class Block(IRenderable):
    def __init__(self, tileset, x, y, render_cfg):
        self.__tiles = tileset
        
        self.__x = x + render_cfg.side_pad
        self.__y = y + render_cfg.top_pad
    
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

    def render(self, screen, render_cfg=None, *args, **kwargs):
        if len(self.__tiles) == 1:
            for tile in self.__tiles:
                x = self.__x
                y = self.__y
                size = render_cfg.block_width, render_cfg.block_height
                tile.render(screen, x, y, size, is_single=True)

        else:
            for tile in self.__tiles:
                x = self.__x + tile.idx %  render_cfg.tiles_count_in_row * (render_cfg.tile_width + render_cfg.tile_gap)
                y = self.__y + tile.idx // render_cfg.tiles_count_in_row * (render_cfg.tile_height + render_cfg.tile_gap)
                size = render_cfg.tile_width, render_cfg.tile_height

                tile.render(screen, x, y, size, render_cfg=render_cfg, is_single=False)
    
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
