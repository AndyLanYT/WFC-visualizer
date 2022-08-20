from constants import DIRECTIONS


class Index:
    def __init__(self, tileset):
        self.__rules = {}
        for tile in tileset:
            self.__rules[tile.idx] = {}
            
            for direction in DIRECTIONS:
                self.__rules[tile.idx][direction] = []
                
                for neighbor in tileset:
                    if self.__is_similar(tile, neighbor, direction):
                        self.__rules[tile.idx][direction].append(neighbor.idx)
    
    def __is_similar(self, tile, neighbor, direction, k=0.8):
        opposite_direction = -direction[0], -direction[1]
        
        tile_pixels = tile.edge_pixels(direction)
        neighbor_pixels = neighbor.edge_pixels(opposite_direction)

        lst = list(map(lambda idx: tile_pixels[idx] == neighbor_pixels[idx], range(len(tile_pixels))))

        return lst.count(True) / len(lst) >= k
    
    def is_possible_neighbor(self, tile, neighbor, direction):
        return neighbor.idx in self.__rules[tile.idx][direction]
