class AppScreen:
    
    def __init__(self):
        super().__init__()

    def draw(self, surface) -> None:
        raise NotImplementedError("draw is an abstract method")

    def on_thumb_up(self) -> None:
        pass

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
        pass

    def on_show(self, *args, **kwargs) -> None:
        pass

    def on_hide(self) -> None:
        pass

    def on_destroy(self) -> None:
        pass