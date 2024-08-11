import pygame


class Tilesheet:
    def __init__(self, tilesheet_config):
        self.__sheet = pygame.image.load(f'smth/assets/{tilesheet_config.tileset_name}.png')
        
        self.__tile_images = []
        for i in range(tilesheet_config.tiles_count):
            x = i %  tilesheet_config.cols * (tilesheet_config.tile_width + tilesheet_config.gap)
            y = i // tilesheet_config.cols * (tilesheet_config.tile_width + tilesheet_config.gap)

            tile_image = self.__get_tile_image(x, y, tilesheet_config.tile_width, tilesheet_config.tile_height)
            self.__tile_images.append(tile_image)

            if tilesheet_config.symmetry:
                pass

            if tilesheet_config.rotation:
                self.__tile_images.append(pygame.transform.rotate(tile_image, 90))
                self.__tile_images.append(pygame.transform.rotate(tile_image, 180))
                self.__tile_images.append(pygame.transform.rotate(tile_image, 270))

    def __get_tile_image(self, x, y, width, height):
        return self.__sheet.subsurface((x, y, width, height))

    @property
    def tile_images(self):
        return self.__tile_images
