from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.core.window import Window
from kivy.animation import Animation

# Set the default window size
Window.size = (400, 600)

# Define the Welcome Screen
class WelcomeScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Add a background image
        self.background = Image(source='download.jpg', allow_stretch=True, keep_ratio=False)
        self.add_widget(self.background)

        # Layout for content
        layout = BoxLayout(orientation='vertical', spacing=20, padding=50, pos_hint={"center_x": 0.5, "center_y": 0.5})

        # Add a title label with animation
        self.title = Label(
            text="BUDDY",
            font_size=50,  # Use numeric value
            color=(1, 1, 1, 1),  # White text
            bold=True,
            pos_hint={"center_x": 0.5, "center_y": 0.7}
        )
        layout.add_widget(self.title)
        self.add_widget(layout)

        # Add animation to the title
        self.animate_title()

    def animate_title(self):
        anim = Animation(font_size=60, d=1.5, t='in_out_bounce') + Animation(font_size=50, d=1)
        anim.repeat = True
        anim.start(self.title)

    def on_touch_down(self, touch):
        """Handle tap anywhere on the screen."""
        self.manager.current = "main"


# Define the Main Screen
class MainScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', spacing=20, padding=50)

        # Add a label to indicate this is the main screen
        label = Label(
            text="Welcome to the Main Screen!",
            font_size=24,
            color=(0.3, 0.3, 0.3, 1)
        )
        layout.add_widget(label)

        self.add_widget(layout)


# ScreenManager to manage screens
class BuddyApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(WelcomeScreen(name="welcome"))
        sm.add_widget(MainScreen(name="main"))
        return sm


# Run the app
if __name__ == "__main__":
    BuddyApp().run()
