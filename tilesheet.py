import pygame
from constants import TILES_COUNT, SHEET_TILE_WIDTH, SHEET_TILE_HEIGHT, SHEET_GAP


class Tilesheet:
    def __init__(self, filename):
        try:
            self.__sheet = pygame.image.load(filename)
        except FileNotFoundError:
            raise SystemExit(f'File {filename} does not exist')
        
        self.__tile_images = []
        for i in range(TILES_COUNT):
            x = i % 7 * (SHEET_TILE_WIDTH + SHEET_GAP)
            y = i // 7 * (SHEET_TILE_HEIGHT + SHEET_GAP)

            tile_image = self.__get_tile_image(x, y, SHEET_TILE_WIDTH, SHEET_TILE_HEIGHT)
            self.__tile_images.append(tile_image)

    def __get_tile_image(self, x, y, width, height):
        return self.__sheet.subsurface((x, y, width, height))

    @property
    def tile_images(self):
        return self.__tile_images
