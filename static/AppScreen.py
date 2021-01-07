class AppScreen:
    
    def __init__(self):
        super().__init__()

    def draw(self, surface) -> None:
        raise NotImplementedError("draw is an abstract method")

    def on_ok(self) -> None:
        pass

    def on_up_left(self) -> None:
        pass

    def on_down_right(self) -> None:
        pass

    def on_back(self) -> None:
        pass

    def on_wait(self) -> None:
        pass

    def on_registered_in_app(self, app) -> None:
        pass

    def on_show(self, *args, **kwargs) -> None:
        pass

    def on_hide(self) -> None:
        pass

    def on_destroy(self) -> None:
        pass