import pygame
from AppScreen import AppScreen

class AckScreen(AppScreen):

    def __init__(self):
        super().__init__()
        self._app = None

        pygame.font.init()
        font_title = pygame.font.SysFont('Comic Sans MS', 53)
        self._title_text_surface = font_title.render('Order sum up', True, (255, 255, 255))

        self._font_sum_up = pygame.font.SysFont('Comic Sans MS', 43)

        self._milkshake_tastes = ['Banana', 'Strawberry', 'Peach', 'Kiwi', 'Chocolate']
        self._sizes = ['S', 'M', 'L']

    def draw(self, surface) -> None:
        surface.fill((158, 237, 240))
        surface.blit(self._title_text_surface, self._title_position)

        surface.blit(self._milkshake_text_img, self._milkshake_text_position)
        surface.blit(self._size_text_img, self._size_text_position)

    def on_ok(self) -> None:
        self._app.show_screen("OrderSent", self._chosen_milkshake, self._chosen_size)

    def on_back(self) -> None:
        self._app.show_screen("Order")

    def on_up_left(self) -> None:
        pass

    def on_down_right(self) -> None:
        pass

    def on_registered_in_app(self, app) -> None:
        self._app = app
        tw = self._title_text_surface.get_rect().width
        th = self._title_text_surface.get_rect().height
        self._title_position = (app.w / 2 - tw / 2, 300 - th)

    def on_show(self, *args, **kwargs) -> None:
        self._chosen_milkshake = args[0]
        self._chosen_size = args[1]

        milkshake_text = "Milkshake: " + self._milkshake_tastes[self._chosen_milkshake]
        size_text = "Size: " + self._sizes[self._chosen_size]

        self._milkshake_text_img = self._font_sum_up.render(milkshake_text, True, (255, 203, 203))
        self._size_text_img = self._font_sum_up.render(size_text, True, (255, 203, 203))

        self._milkshake_text_position = (self._app.w / 4, 300 + 0 * self._milkshake_text_img.get_rect().height)
        self._size_text_position = (self._app.w / 4, 300 + 1 * self._size_text_img.get_rect().height)

    def on_hide(self) -> None:
        pass

    def on_destroy(self) -> None:
        pass