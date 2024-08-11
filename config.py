import json
from math import ceil, sqrt


CONFIG = None


class Config:
    def __init__(self, filename):
        try:
            with open(f'smth/WFCvisualizer/metadata.json') as json_file:
                data = json.load(json_file)[filename]
                print(data)

                self.__tileset_name = filename
                self.__tile_width = data['sheet_tile_width']
                self.__tile_height = data['sheet_tile_height']
                self.__gap = data['sheet_gap']
                self.__rows = data['rows']
                self.__cols = data['cols']
                self.__tiles_count = data['tiles_count']
                self.__symmetry = data['symmetry']
                self.__rotation = data['rotation']
        
        except FileNotFoundError:
            raise SystemExit('File metadata.json does not exist')
        
        except KeyError:
            raise SystemExit(f'Tileset {filename} does not exist')

        self.__screen_width = 800
        self.__screen_height = 600

        self.__output_size = 7, 7       
        
        max_field_width = 550
        max_field_height = 550

        self.__tile_gap = 0
        self.__block_gap = 1#min(max(70 // max(OUTPUT_SIZE), 1), 10)

        self.__tiles_count_in_row = ceil(sqrt(self.__tiles_count))

        self.__tile_width = int(((max_field_width - self.__block_gap * (max(self.__output_size) - 1)) / max(self.__output_size) + self.__tile_gap) / self.__tiles_count_in_row - self.__tile_gap)
        self.__tile_height = int(((max_field_height - self.__block_gap * (max(self.__output_size) - 1)) / max(self.__output_size) + self.__tile_gap) / self.__tiles_count_in_row - self.__tile_gap)

        self.__block_width = self.__tiles_count_in_row * (self.__tile_width + self.__tile_gap) - self.__tile_gap
        self.__block_height = self.__tiles_count_in_row * (self.__tile_height + self.__tile_gap) - self.__tile_gap

        self.__canvas_width = self.__block_width * self.__output_size[0] + self.__block_gap * (self.__output_size[0] - 1)
        self.__canvas_height = self.__block_height * self.__output_size[1] + self.__block_gap * (self.__output_size[1] - 1)

        self.__side_pad = 30
        self.__top_pad = (self.__screen_height - self.__canvas_height) // 2

        self.__button_width = 150
        self.__button_height = 40

        self.__toggle_width = 45
        self.__toggle_height = 20

        self.__fps = 15

    @classmethod
    def load_config(cls, filename, force_load=False):
        global CONFIG

        if CONFIG is not None and not force_load:
            return

        CONFIG = cls(filename)
    
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
    
    @property
    def screen_width(self):
        return self.__screen_width
    
    @property
    def screen_height(self):
        return self.__screen_height
    
    @property
    def output_size(self):
        return self.__output_size
    
    @property
    def tile_gap(self):
        return self.__tile_gap
    
    @property
    def block_gap(self):
        return self.__block_gap
    
    @property
    def tiles_count_in_row(self):
        return self.__tiles_count_in_row
    
    @property
    def tile_width(self):
        return self.__tile_width
    
    @property
    def tile_height(self):
        return self.__tile_height
    
    @property
    def block_width(self):
        return self.__block_width
    
    @property
    def block_height(self):
        return self.__block_height
    
    @property
    def canvas_width(self):
        return self.__canvas_width
    
    @property
    def canvas_height(self):
        return self.__canvas_height
    
    @property
    def side_pad(self):
        return self.__side_pad
    
    @property
    def top_pad(self):
        return self.__top_pad
    
    @property
    def button_width(self):
        return self.__button_width
    
    @property
    def button_height(self):
        return self.__button_height
    
    @property
    def toggle_width(self):
        return self.__toggle_width
    
    @property
    def toggle_height(self):
        return self.__toggle_height
    
    @property
    def fps(self):
        return self.__fps


Config.load_config('some file')

print(CONFIG)
