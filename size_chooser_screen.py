import pygame

from AppScreen import AppScreen

class SizeChooserScreen(AppScreen):
    
    def __init__(self):
        super().__init__()
        self._app = None

        pygame.font.init()
        font_title = pygame.font.SysFont('Comic Sans MS', 53)
        self._title_text_surface = font_title.render('Order - choose size', True, (255, 255, 255))

        font_milkshakes = pygame.font.SysFont('Comic Sans MS', 43)
        self._sizes = [
            font_title.render('S', True, (255, 255, 255)),
            font_title.render('M', True, (255, 255, 255)),
            font_title.render('L', True, (255, 255, 255)),
        ]

        self._chosen_milkshake = 0
        self._chosen_size = 0

    def draw(self, surface) -> None:
        surface.fill((255, 203, 203))
        surface.blit(self._title_text_surface, self._title_position)

        for i, size in enumerate(self._sizes):
            surface.blit(size, self._sizes_positions[i])

            if self._chosen_size == i:
                r = size.get_rect()
                r.move_ip(*self._sizes_positions[i])
                pygame.draw.rect(surface, (255, 0, 0), r, 2)

    def on_thumb_up(self) -> None:
        self._app.show_screen("Ack", self._chosen_milkshake, self._chosen_size)

    def on_thumb_down(self) -> None:
        self._app.show_screen("Order")

    def on_left_to_right_swipe(self) -> None:
        self._chosen_size = (self._chosen_size + 1) % len(self._sizes)

    def on_right_to_left_swipe(self) -> None:
        self._chosen_size -= 1
        if self._chosen_size < 0:
            self._chosen_size = len(self._sizes) - 1

    def on_up_to_down_swipe(self) -> None:
        pass

    def on_down_to_up_swipe(self) -> None:
        pass

    def on_registered_in_app(self, app) -> None:
        self._app = app
        tw = self._title_text_surface.get_rect().width
        th = self._title_text_surface.get_rect().height
        self._title_position = (app.w / 2 - tw / 2, 300 - th)

        self._sizes_positions = [
            (app.w / 3 + 300 * i, app.h / 3) for i, size_label in enumerate(self._sizes)
        ]

    def on_show(self, *args, **kwargs) -> None:
        self._chosen_milkshake = args[0]

    def on_hide(self) -> None:
        pass

    def on_destroy(self) -> None:
        pass