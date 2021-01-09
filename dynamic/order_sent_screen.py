import pygame

from AppScreen import AppScreen

class OrderSentScreen(AppScreen):

    def __init__(self):
        super().__init__()
        self._app = None

        pygame.font.init()

    def draw(self, surface) -> None:
        surface.blit(self._bg, (0, self._app.h - self._bg.get_height()))

        seconds = (pygame.time.get_ticks() - self._start_ticks) / 1000
        if seconds >= 15:
            self._app.show_screen("Welcome")

    def on_thumb_up(self) -> None:
        self._app.show_screen("Welcome")

    def on_thumb_down(self) -> None:
        pass

    def on_left_to_right_swipe(self) -> None:
        pass

    def on_right_to_left_swipe(self) -> None:
        pass

    def on_up_to_down_swipe(self) -> None:
        pass

    def on_down_to_up_swipe(self) -> None:
        pass

    def on_registered_in_app(self, app) -> None:
        self._app = app
        self._bg = pygame.transform.smoothscale(pygame.image.load('./bg_img/sent_screen.png'), (self._app.w, self._app.h))

    def on_show(self, *args, **kwargs) -> None:
        self._chosen_milkshake = args[0]
        self._chosen_size = args[1]

        self._start_ticks = pygame.time.get_ticks()

    def on_hide(self) -> None:
        pass

    def on_destroy(self) -> None:
        pass