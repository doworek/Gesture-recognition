import pygame
from AppScreen import AppScreen

class WelcomeScreen(AppScreen):

    def __init__(self):
        super().__init__()
        self._app = None

        pygame.font.init()

    def draw(self, surface) -> None:
        surface.blit(self._bg, (0, self._app.h - self._bg.get_height()))

    def on_ok(self) -> None:
        self._app.show_screen("Order")

    def on_registered_in_app(self, app) -> None:
        self._app = app
        self._bg = pygame.transform.smoothscale(pygame.image.load('./bg_img/welcome_screen.png'), (self._app.w, self._app.h))

    def on_show(self, *args, **kwargs) -> None:
        pass

    def on_hide(self) -> None:
        pass

    def on_destroy(self) -> None:
        pass