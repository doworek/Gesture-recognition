import pygame
from AppScreen import AppScreen

class AckScreen(AppScreen):

    def __init__(self):
        super().__init__()
        self._app = None

        pygame.font.init()

        self._font_sum_up = pygame.font.SysFont('Comic Sans MS', 43)
        self._milkshake_tastes = ['Banana', 'Strawberry', 'Peach', 'Kiwi', 'Apple']
        self._sizes = ['S', 'M', 'L']

    def draw(self, surface) -> None:
        surface.blit(self._bg, (0, self._app.h - self._bg.get_height()))
        surface.blit(self._milkshake_text_img, self._milkshake_text_position)
        surface.blit(self._size_text_img, self._size_text_position)

    def on_thumb_up(self) -> None:
        self._app.show_screen("OrderSent", self._chosen_milkshake, self._chosen_size)

    def on_thumb_down(self) -> None:
        self._app.show_screen("Order")

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
        self._bg = pygame.transform.smoothscale(pygame.image.load('./bg_img/ack_screen.png'), (self._app.w, self._app.h))

    def on_show(self, *args, **kwargs) -> None:
        self._chosen_milkshake = args[0]
        self._chosen_size = args[1]

        milkshake_text = "Milkshake: " + self._milkshake_tastes[self._chosen_milkshake]
        size_text = "Size: " + self._sizes[self._chosen_size]

        self._milkshake_text_img = self._font_sum_up.render(milkshake_text, True, (255, 255, 255))
        self._size_text_img = self._font_sum_up.render(size_text, True, (255, 255, 255))

        self._milkshake_text_position = (self._app.w / 4, 300 + 0 * self._milkshake_text_img.get_rect().height)
        self._size_text_position = (self._app.w / 4, 300 + 1 * self._size_text_img.get_rect().height)

    def on_hide(self) -> None:
        pass

    def on_destroy(self) -> None:
        pass