import pygame

from waveFunction import WaveFunction
from button import Button
from toggle import Toggle
from tilesheet import Tilesheet

from colors import DARK_GREY
from constants import SCREEN_WIDTH, SCREEN_HEIGHT, SIDE_PAD, TOP_PAD, FIELD_WIDTH, FIELD_HEIGHT, BLOCK_WIDTH, BLOCK_HEIGHT, BLOCK_GAP, TILES_COUNT_IN_ROW, SHEET_TILE_WIDTH, SHEET_TILE_HEIGHT, OUTPUT_SIZE, TILE_WIDTH, TILE_HEIGHT, TILE_GAP


pygame.init()
pygame.font.init()


class Visualizer:
    def __init__(self):
        self.__screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption('WFC visualizer')
        
        self.__clock = pygame.time.Clock()

        tilesheet = Tilesheet('assets/tiles.png')
        self.__wave_function = WaveFunction(tilesheet.tile_images)

        self.__collapse_button = Button('Collapse', (595, 150))
        self.__renovate_button = Button('Renovate', (595, 210))
        self.__save_button = Button('Save', (595, 270))
        self.__propagation_toggle = Toggle((595, 330))

        self.__to_propagate = True
        self.__start = False

        self.__runner = True

    def get_col_row_idx(self, mouse_x, mouse_y):
        col, row, idx = None, None, None

        if SIDE_PAD <= mouse_x <= SIDE_PAD + FIELD_WIDTH and TOP_PAD <= mouse_y <= TOP_PAD + FIELD_HEIGHT:
            col = (mouse_x - SIDE_PAD) // (BLOCK_WIDTH + BLOCK_GAP)
            row = (mouse_y - TOP_PAD) // (BLOCK_HEIGHT + BLOCK_GAP)

            block = self.__wave_function.coeffs[row][col]
            if block.x <= mouse_x <= block.x + BLOCK_WIDTH and block.y <= mouse_y <= block.y + BLOCK_HEIGHT:
                x = (mouse_x - SIDE_PAD) % (BLOCK_WIDTH + BLOCK_GAP) // (TILE_WIDTH + TILE_GAP)
                y = (mouse_y - TOP_PAD) % (BLOCK_HEIGHT + BLOCK_GAP) // (TILE_HEIGHT + TILE_GAP)

                idx = y * TILES_COUNT_IN_ROW + x

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
        image = pygame.Surface((SHEET_TILE_WIDTH * OUTPUT_SIZE[0], SHEET_TILE_HEIGHT * OUTPUT_SIZE[1]))

        for i, row in enumerate(self.__wave_function.coeffs):
            for j, block in enumerate(row):
                image.blit(block.tiles[0].image, (SHEET_TILE_WIDTH * j, SHEET_TILE_HEIGHT * i))

        return image
    
    def save_image(self, filename):
        image = self.image()
        pygame.image.save(image, f'{filename}.png')
    
    def render(self):
        self.__screen.fill(DARK_GREY)
        self.__wave_function.render(self.__screen)
        self.__collapse_button.render(self.__screen)
        self.__renovate_button.render(self.__screen)
        self.__save_button.render(self.__screen)
        self.__propagation_toggle.render(self.__screen)
        
        pygame.display.flip()

    def run(self):
        while self.__runner:
            # self.__clock.tick(FPS)

            if self.__start:
                try:
                    next(collapse_gen)
                except StopIteration:
                    self.__start = False

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.__runner = False
                
                elif event.type == pygame.KEYDOWN and not self.__start:
                    if event.key == pygame.K_c:
                        collapse_gen = self.__wave_function.collapse()
                        self.__start = True
                    
                    elif event.key == pygame.K_r:
                        self.__wave_function.renovate()
                    
                    elif event.key == pygame.K_p:
                        self.__to_propagate = not self.__to_propagate
            
            if not self.__start:
                if self.check_clicked_tile():
                    collapse_gen = self.__wave_function.propagate()
                    self.__start = True

                if self.__collapse_button.check_click():
                    collapse_gen = self.__wave_function.collapse()
                    self.__start = True

                if self.__renovate_button.check_click():
                    self.__wave_function.renovate()

                if self.__wave_function.is_collapsed() and self.__save_button.check_click():
                    self.save_image(input('filename: '))
                
                if self.__propagation_toggle.check_click():
                    self.__to_propagate = not self.__to_propagate

            self.render()

        pygame.quit()


Visualizer().run()
