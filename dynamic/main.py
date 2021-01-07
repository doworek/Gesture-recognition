from App import App

from welcome_screen import WelcomeScreen
from order_screen import OrderScreen
from size_chooser_screen import SizeChooserScreen
from ack_screen import AckScreen
from order_sent_screen import OrderSentScreen

if __name__ == "__main__":

    app = App()
    
    app.register_app_screen("Welcome", WelcomeScreen())
    app.register_app_screen("Order", OrderScreen())
    app.register_app_screen("Size", SizeChooserScreen())
    app.register_app_screen("Ack", AckScreen())
    app.register_app_screen("OrderSent", OrderSentScreen())

    app.run("Welcome")
    
