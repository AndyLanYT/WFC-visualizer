import json


class TilesheetConfig:
    def __init__(self, tileset_name):
        try:
            with open(f'smth/WFCvisualizer/metadata.json') as json_file:
                data = json.load(json_file)[tileset_name]

                self.__tileset_name = tileset_name
                self.__tile_width = data['sheet_tile_width']
                self.__tile_height = data['sheet_tile_height']
                self.__gap = data['sheet_gap']
                self.__rows = data['rows']
                self.__cols = data['cols']
                self.__tiles_count = data['tiles_count']
                self.__symmetry = data["symmetry"]
                self.__rotation = data["rotation"]
        
        except FileNotFoundError:
            raise SystemExit('File metadata.json does not exist')
        
        except KeyError:
            raise SystemExit(f'Tileset {tileset_name} does not exist')

    @property
    def tileset_name(self):
        return self.__tileset_name

    @property
    def tile_width(self):
        return self.__tile_width

    @property
    def tile_height(self):
        return self.__tile_height
    
    @property
    def gap(self):
        return self.__gap
    
    @property
    def rows(self):
        return self.__rows
    
    @property
    def cols(self):
        return self.__cols
    
    @property
    def symmetry(self):
        return self.__symmetry
    
    @property
    def rotation(self):
        return self.__rotation
    
    @property
    def tiles_count(self):
        return self.__tiles_count
