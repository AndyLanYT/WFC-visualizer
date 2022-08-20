import pygame
from constants import BUTTON_WIDTH, BUTTON_HEIGHT
from colors import BLACK, WHITE, DARK_RED, DARK_BLUE
from fonts import FONT


class Button:
    def __init__(self, text, pos, width=BUTTON_WIDTH, height=BUTTON_HEIGHT):
        self.__is_pressed = False

        elevation = int(0.14 * height)
        self.__elevation = elevation
        self.__dynamic_elevation = elevation
        self.__y = pos[1]

        self.__bottom_rect = pygame.Rect(pos, (width, height + elevation))
        self.__bottom_color = BLACK

        self.__top_rect = pygame.Rect(pos, (width, height))
        self.__top_color = DARK_BLUE

        self.__text_surf = FONT.render(text, True, WHITE)
        self.__text_rect = self.__text_surf.get_rect(center=self.__top_rect.center)

    def check_click(self):
        mouse_pos = pygame.mouse.get_pos()

        if self.__top_rect.collidepoint(mouse_pos):
            self.__top_color = DARK_RED
            
            if pygame.mouse.get_pressed()[0]:
                self.__is_pressed = True
                self.__dynamic_elevation = 0
            else:
                if self.__is_pressed:
                    self.__is_pressed = False
                    self.__dynamic_elevation = self.__elevation
                    
                    return True
        else:
            self.__top_color = DARK_BLUE
            self.__dynamic_elevation = self.__elevation

    def render(self, screen):
        self.__top_rect.y = self.__y - self.__dynamic_elevation
        self.__text_rect.center = self.__top_rect.center

        self.__bottom_rect.y = self.__top_rect.y
        self.__bottom_rect.height = self.__top_rect.height + self.__dynamic_elevation

        pygame.draw.rect(screen, self.__bottom_color, self.__bottom_rect, border_radius=12)
        pygame.draw.rect(screen, self.__top_color, self.__top_rect, border_radius=12)
        screen.blit(self.__text_surf, self.__text_rect)
