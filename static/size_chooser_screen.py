import pygame

from AppScreen import AppScreen

class SizeChooserScreen(AppScreen):
    
    def __init__(self):
        super().__init__()
        self._app = None

        pygame.font.init()
        font_title = pygame.font.SysFont('Comic Sans MS', 53)

        font_milkshakes = pygame.font.SysFont('Comic Sans MS', 43)
        self._sizes = [
            font_title.render('S', True, (255, 255, 255)),
            font_title.render('M', True, (255, 255, 255)),
            font_title.render('L', True, (255, 255, 255)),
        ]

        self._chosen_milkshake = 0
        self._chosen_size = 0

    def draw(self, surface) -> None:
        surface.blit(self._bg, (0, self._app.h - self._bg.get_height()))

        for i, size in enumerate(self._sizes):
            surface.blit(size, self._sizes_positions[i])

            if self._chosen_size == i:
                r = size.get_rect()
                r.move_ip(*self._sizes_positions[i])
                pygame.draw.rect(surface, (202, 0, 182), r, 2)

    def on_ok(self) -> None:
        self._app.show_screen("Ack", self._chosen_milkshake, self._chosen_size)

    def on_back(self) -> None:
        self._app.show_screen("Order")

    def on_down_right(self) -> None:
        self._chosen_size = (self._chosen_size + 1) % len(self._sizes)

    def on_up_left(self) -> None:
        self._chosen_size -= 1
        if self._chosen_size < 0:
            self._chosen_size = len(self._sizes) - 1

    def on_registered_in_app(self, app) -> None:
        self._app = app
        self._bg = pygame.transform.smoothscale(pygame.image.load('./bg_img/size_screen.png'), (self._app.w, self._app.h))

        self._sizes_positions = [
            (app.w / 3 + 300 * i, app.h / 3) for i, size_label in enumerate(self._sizes)
        ]

    def on_show(self, *args, **kwargs) -> None:
        self._chosen_milkshake = args[0]

    def on_hide(self) -> None:
        pass

    def on_destroy(self) -> None:
        pass