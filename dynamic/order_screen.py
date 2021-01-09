import pygame

from AppScreen import AppScreen

class OrderScreen(AppScreen):
    
    def __init__(self):
        super().__init__()
        self._app = None

        pygame.font.init()
        font_title = pygame.font.SysFont('Comic Sans MS', 53)

        font_milkshakes = pygame.font.SysFont('Comic Sans MS', 33)
        self._milkshakes = [
            font_title.render('Banana', True, (255, 255, 255)),
            font_title.render('Strawberry', True, (255, 255, 255)),
            font_title.render('Peach', True, (255, 255, 255)),
            font_title.render('Kiwi', True, (255, 255, 255)),
            font_title.render('Chocolate', True, (255, 255, 255)),
        ]

        self._chosen_milkshake = 0

    def draw(self, surface) -> None:
        surface.blit(self._bg, (0, self._app.h - self._bg.get_height()))

        for i, milkshake in enumerate(self._milkshakes):
            surface.blit(milkshake, self._milkshakes_positions[i])

            if self._chosen_milkshake == i:
                r = milkshake.get_rect()
                r.move_ip(*self._milkshakes_positions[i])
                pygame.draw.rect(surface, (202, 0, 182), r, 2)

    def on_thumb_up(self) -> None:
        self._app.show_screen("Size", self._chosen_milkshake)

    def on_thumb_down(self) -> None:
        self._app.show_screen("Welcome")

    def on_left_to_right_swipe(self) -> None:
        pass

    def on_right_to_left_swipe(self) -> None:
        pass

    def on_up_to_down_swipe(self) -> None:
        self._chosen_milkshake -= 1
        if self._chosen_milkshake < 0:
            self._chosen_milkshake = len(self._milkshakes) - 1

    def on_down_to_up_swipe(self) -> None:
        self._chosen_milkshake = (self._chosen_milkshake + 1) % len(self._milkshakes)

    def on_registered_in_app(self, app) -> None:
        self._app = app
        self._bg = pygame.transform.smoothscale(pygame.image.load('./bg_img/order_screen.png'), (self._app.w, self._app.h))

        self._milkshakes_positions = [
            (app.w / 4, 300 + i * milkshake.get_rect().height) for i, milkshake in enumerate(self._milkshakes)
        ]

    def on_show(self, *args, **kwargs) -> None:
        pass

    def on_hide(self) -> None:
        pass

    def on_destroy(self) -> None:
        pass