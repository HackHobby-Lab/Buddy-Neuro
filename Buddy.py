from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.uix.spinner import Spinner
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.animation import Animation
from kivy.uix.widget import Widget

# Set the default window size
Window.size = (240, 320)

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


# Define the Main Screen with Pomodoro Timer
class MainScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.timer_running = False
        self.time_left = 0
        self.background = Image(source='download (1).jpg', allow_stretch=True, keep_ratio=False)
        self.add_widget(self.background)

        # Layout for timer and controls
        layout = BoxLayout(orientation='vertical', spacing=10, padding=20)


        # Add a label for timer display
        self.timer_label = Label(
            text="00:00", 
            font_size=50, 
            color=(1, 1, 255, 1),
            halign='center'
        )
        layout.add_widget(self.timer_label)

        # Add a spinner for selecting work duration
        self.work_duration_spinner = Spinner(
            text='5',
            values=('5', '10', '15', '20', '25', '30'),
            size_hint=(None, None),
            size=(200, 44),
            pos_hint={'center_x': 0.5}
        )
        layout.add_widget(self.work_duration_spinner)

        # Add a spinner for selecting break duration
        self.break_duration_spinner = Spinner(
            text='5',
            values=('5', '10', '15', '20', '25'),
            size_hint=(None, None),
            size=(200, 44),
            pos_hint={'center_x': 0.5}
        )
        layout.add_widget(self.break_duration_spinner)

        # Start button
        self.start_button = Button(
            text="Start Timer",
            size_hint=(None, None),
            size=(200, 50),
            pos_hint={"center_x": 0.5},
            background_normal='',  # Remove default background
            background_color=(0.2, 0.6, 0.2, 1),  # Green color
            font_size=18
        )
        self.start_button.bind(on_press=self.start_timer)
        layout.add_widget(self.start_button)

        # Reset button
        self.reset_button = Button(
            text="Reset Timer",
            size_hint=(None, None),
            size=(200, 50),
            pos_hint={"center_x": 0.5},
            background_normal='',  # Remove default background
            background_color=(0.8, 0.2, 0.2, 1),  # Red color
            font_size=18
        )
        self.reset_button.bind(on_press=self.reset_timer)
        layout.add_widget(self.reset_button)

        # Go Back Button
        self.go_back_button = Button(
            text="Go Back",
            size_hint=(None, None),
            size=(200, 50),
            pos_hint={"center_x": 0.5},
            background_normal='',  # Remove default background
            background_color=(0.6, 0.2, 0.6, 1),  # Purple color
            font_size=18
        )
        self.go_back_button.bind(on_press=self.go_back)
        layout.add_widget(self.go_back_button)

        self.add_widget(layout)

    def start_timer(self, instance):
        if not self.timer_running:
            # Get the work and break duration from the spinners
            work_duration = int(self.work_duration_spinner.text)
            break_duration = int(self.break_duration_spinner.text)

            # Set the timer to work session time (in seconds)
            self.time_left = work_duration * 60
            self.timer_running = True

            # Update the timer display every second
            Clock.schedule_interval(self.update_timer, 1)

    def update_timer(self, dt):
        if self.time_left > 0:
            # Decrement the timer and update the label
            minutes, seconds = divmod(self.time_left, 60)
            self.timer_label.text = f"{minutes:02}:{seconds:02}"
            self.time_left -= 1
        else:
            # Timer ends, notify user and switch to break time
            self.timer_label.text = "Break Time!"
            self.timer_running = False
            Clock.unschedule(self.update_timer)

            # Switch to break timer after work session ends
            Clock.schedule_once(self.start_break_timer, 3)

    def start_break_timer(self, dt):
        # Get the break duration from the spinner
        break_duration = int(self.break_duration_spinner.text)
        self.time_left = break_duration * 60
        self.timer_running = True

        # Start countdown for break timer
        Clock.schedule_interval(self.update_timer, 1)

    def reset_timer(self, instance):
        # Reset everything
        self.timer_running = False
        self.time_left = 0
        self.timer_label.text = "00:00"
        Clock.unschedule(self.update_timer)

    def go_back(self, instance):
        """Handle 'Go Back' button."""
        self.manager.current = "welcome"


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
