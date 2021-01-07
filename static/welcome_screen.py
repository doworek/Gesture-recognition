import pygame
from AppScreen import AppScreen

class WelcomeScreen(AppScreen):

    def __init__(self):
        super().__init__()
        self._app = None

        pygame.font.init()
        font = pygame.font.SysFont('Comic Sans MS', 100)
        self._text_surface = font.render('Milkshake', True, (255, 255, 255))

    def draw(self, surface) -> None:
        surface.fill((255, 203, 203))
        surface.blit(self._text_surface, self._text_position)

    def on_ok(self) -> None:
        self._app.show_screen("Order")

    def on_registered_in_app(self, app) -> None:
        self._app = app
        tw = self._text_surface.get_rect().width
        th = self._text_surface.get_rect().height
        self._text_position = (app.w / 2 - tw / 2, app.h / 2 - th / 2)

    def on_show(self, *args, **kwargs) -> None:
        pass

    def on_hide(self) -> None:
        pass

    def on_destroy(self) -> None:
        pass