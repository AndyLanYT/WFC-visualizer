import pygame

from waveFunction import WaveFunction
from button import Button
from toggle import Toggle
from tilesheet import Tilesheet
from renderConfig import RenderConfig
from tilesheetConfig import TilesheetConfig

from colors import DARK_GREY

import time


pygame.init()
pygame.font.init()


class Visualizer:
    def __init__(self):
        tileset_name = input('tileset name: ')
        self.__tilesheet_cfg = TilesheetConfig(tileset_name)
        self.__render_cfg = RenderConfig(self.__tilesheet_cfg)

        self.__screen = pygame.display.set_mode((self.__render_cfg.screen_width, self.__render_cfg.screen_height))
        pygame.display.set_caption('WFC visualizer')
        
        self.__clock = pygame.time.Clock()

        tilesheet = Tilesheet(self.__tilesheet_cfg)
        
        self.__wave_function = WaveFunction(tilesheet.tile_images, self.__tilesheet_cfg, self.__render_cfg)

        self.__collapse_button = Button('Collapse', (595, 150), self.__render_cfg)
        self.__renovate_button = Button('Renovate', (595, 210), self.__render_cfg)
        self.__save_button = Button('Save', (595, 270), self.__render_cfg)

        self.__propagation_toggle = Toggle((595, 330), self.__render_cfg)
        self.__update_toggle = Toggle((650, 330), self.__render_cfg)

        self.__to_propagate = True
        self.__to_update = True
        self.__start = False

        self.__runner = True

    def get_col_row_idx(self, mouse_x, mouse_y):
        col, row, idx = None, None, None

        if self.__render_cfg.side_pad <= mouse_x <= self.__render_cfg.side_pad + self.__render_cfg.canvas_width and self.__render_cfg.top_pad <= mouse_y <= self.__render_cfg.top_pad + self.__render_cfg.canvas_height:
            col = (mouse_x - self.__render_cfg.side_pad) // (self.__render_cfg.block_width + self.__render_cfg.block_gap)
            row = (mouse_y - self.__render_cfg.top_pad) // (self.__render_cfg.block_height + self.__render_cfg.block_gap)

            block = self.__wave_function.coeffs[row][col]
            if block.x <= mouse_x <= block.x + self.__render_cfg.block_width and block.y <= mouse_y <= block.y + self.__render_cfg.block_height:
                x = (mouse_x - self.__render_cfg.side_pad) % (self.__render_cfg.block_width + self.__render_cfg.block_gap) // (self.__render_cfg.tile_width + self.__render_cfg.tile_gap)
                y = (mouse_y - self.__render_cfg.top_pad) % (self.__render_cfg.block_height + self.__render_cfg.block_gap) // (self.__render_cfg.tile_height + self.__render_cfg.tile_gap)

                idx = y * self.__render_cfg.tiles_count_in_row + x

        return col, row, idx
    
    def check_clicked_tile(self):
        if pygame.mouse.get_pressed()[0]:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            col, row, idx = self.get_col_row_idx(mouse_x, mouse_y)

            if idx is not None:
                block = self.__wave_function.coeffs[row][col]

                if len(block) != 1 and idx in block:
                    tile = block[idx]
                    block.tiles = tile
                    self.__wave_function.add_to_stack((col, row))
                    
                    return self.__to_propagate
    
    def image(self):
        image = pygame.Surface((self.__tilesheet_cfg.tile_width * self.__render_cfg.output_size[0], self.__tilesheet_cfg.tile_height * self.__render_cfg.output_size[1]))

        for i, row in enumerate(self.__wave_function.coeffs):
            for j, block in enumerate(row):
                image.blit(block.tiles[0].image, (self.__tilesheet_cfg.tile_width * j, self.__tilesheet_cfg.tile_height * i))

        return image
    
    def save_image(self, filename):
        image = self.image()
        pygame.image.save(image, f'{filename}.png')
    
    def process_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.__runner = False
            
            elif event.type == pygame.KEYDOWN:
                if not self.__start:
                    if event.key == pygame.K_c:
                        self.__wave_function.collapse()
                        self.__start = True
                    
                    elif event.key == pygame.K_r:
                        self.__wave_function.renovate(self.__tilesheet_cfg, self.__render_cfg)
                        self.__start = False
                    
                    elif event.key == pygame.K_p:
                        self.__to_propagate = not self.__to_propagate
                
                if event.key == pygame.K_n:
                    try:
                        self.__wave_function.update()
                    except StopIteration:
                        self.__start = False
            
            if self.check_clicked_tile():
                self.__wave_function.propagate()
                self.__start = True

            elif self.__collapse_button.check_click():
                self.start_time = time.time()
                self.__wave_function.collapse()
                self.__start = True

            elif self.__renovate_button.check_click():
                self.__wave_function.renovate(self.__tilesheet_cfg, self.__render_cfg)
                self.__start = False

            elif self.__wave_function.is_collapsed() and self.__save_button.check_click():
                self.save_image(input('filename: '))
            
            elif self.__propagation_toggle.check_click():
                self.__to_propagate = not self.__to_propagate
            
            elif self.__update_toggle.check_click():
                self.__to_update = not self.__to_update

    def update(self):
        if self.__start and self.__to_update:
            try:
                self.__wave_function.update()
            except StopIteration:
                print(f'Generation time: {self.__tilesheet_cfg.tileset_name}; {self.__render_cfg.output_size}; {time.time() - self.start_time}')
                self.__start = False

    def render(self):
        self.__screen.fill(DARK_GREY)
        
        self.__wave_function.render(self.__screen, self.__render_cfg)
        
        self.__collapse_button.render(self.__screen)
        self.__renovate_button.render(self.__screen)
        self.__save_button.render(self.__screen)

        self.__propagation_toggle.render(self.__screen)
        self.__update_toggle.render(self.__screen)
        
        pygame.display.flip()

    def run(self):
        while self.__runner:
            # self.__clock.tick(FPS)

            self.process_input()
            self.update()
            self.render()

        pygame.quit()


Visualizer().run()
