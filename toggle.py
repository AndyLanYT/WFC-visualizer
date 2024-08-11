import pygame

from IRenderable import IRenderable
from IClickable import IClickable

# from constants import TOGGLE_WIDTH, TOGGLE_HEIGHT
from colors import BLACK, DARK_GREEN, DARK_RED


class Toggle(IRenderable, IClickable):
    def __init__(self, pos, render_cfg):
        self.__is_pressed = False
        self.__status = True

        self.__bottom_rect = pygame.Rect(pos, (render_cfg.toggle_width, render_cfg.toggle_height))

        top_height = int(0.9 * render_cfg.toggle_height)
        top_width = top_height
        top_y = pos[1] + (render_cfg.toggle_height - top_height) // 2
        
        self.__top_rect = pygame.Rect((pos[0], top_y), (top_width, top_height))

    def check_click(self):
        mouse_pos = pygame.mouse.get_pos()

        if self.__bottom_rect.collidepoint(mouse_pos):
            if pygame.mouse.get_pressed()[0]:
                self.__is_pressed = True
            else:
                if self.__is_pressed:
                    self.__is_pressed = False
                    self.__status = not self.__status

                    return True
    
    def render(self, screen, *args, **kwargs):
        pygame.draw.rect(screen, BLACK, self.__bottom_rect, border_radius=self.__bottom_rect.height // 2)
        
        if self.__status:
            self.__top_rect.x = self.__bottom_rect.x + self.__bottom_rect.width - self.__top_rect.width - (self.__bottom_rect.height - self.__top_rect.height) // 2
            pygame.draw.rect(screen, DARK_GREEN, self.__top_rect, border_radius=self.__top_rect.height // 2)
        else:
            self.__top_rect.x = self.__bottom_rect.x + (self.__bottom_rect.height - self.__top_rect.height) // 2
            pygame.draw.rect(screen, DARK_RED, self.__top_rect, border_radius=self.__top_rect.height // 2)
