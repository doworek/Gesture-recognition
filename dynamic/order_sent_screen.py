import pygame

from AppScreen import AppScreen

class OrderSentScreen(AppScreen):

    def __init__(self):
        super().__init__()
        self._app = None

        pygame.font.init()
        font_title = pygame.font.SysFont('Comic Sans MS', 100)
        self._title_text_surface = font_title.render('Thank you for your order!', True, (255, 255, 255))

    def draw(self, surface) -> None:
        surface.fill((252, 234, 234))
        surface.blit(self._title_text_surface, self._title_position)

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
        tw = self._title_text_surface.get_rect().width
        th = self._title_text_surface.get_rect().height
        self._title_position = (app.w / 2 - tw / 2, 300 - th)

    def on_show(self, *args, **kwargs) -> None:
        self._chosen_milkshake = args[0]
        self._chosen_size = args[1]

        self._start_ticks = pygame.time.get_ticks()

    def on_hide(self) -> None:
        pass

    def on_destroy(self) -> None:
        pass
