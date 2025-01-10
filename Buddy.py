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
from kivy.uix.filechooser import FileChooserListView
from kivy.core.audio import SoundLoader

# Set the default window size
Window.size = (240, 320)

# Global variable for background music
current_music = None


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
            font_size=50,
            color=(1, 1, 1, 1),
            bold=True,
            pos_hint={"center_x": 0.5, "center_y": 0.7}
        )
        layout.add_widget(self.title)
        self.add_widget(layout)

        # Add animation to the title
        self.animate_title()

    def animate_title(self):
        anim = Animation(font_size=60, d=1, t='in_out_bounce') + Animation(font_size=55, d=1)
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
        self.break_music = SoundLoader.load("break_music.mp3")  # Replace with the actual file path
        self.background = Image(source='down.jpg', allow_stretch=True, keep_ratio=False)
        self.add_widget(self.background)

        # Layout for timer and controls
        layout = BoxLayout(orientation='vertical', spacing=5, padding=25)

        # Add a label for timer display
        self.timer_label = Label(
            text="00:00", 
            font_size=50, 
            color=(1, 1, 1, 1),
            halign='center'
        )
        layout.add_widget(self.timer_label)

        # Add a spinner for selecting work duration
        self.work_duration_spinner = Spinner(
            text='5',
            values=('2','5', '10', '15', '20', '25', '30'),
            size_hint=(None, None),
            size=(200, 44),
            pos_hint={'center_x': 0.5}
        )
        layout.add_widget(self.work_duration_spinner)

        # Add a spinner for selecting break duration
        self.break_duration_spinner = Spinner(
            text='5',
            values=('2','5', '10', '15', '20', '25'),
            size_hint=(None, None),
            size=(200, 44),
            pos_hint={'center_x': 0.5}
        )
        layout.add_widget(self.break_duration_spinner)

        # Start button
        self.start_button = Button(
            text="Start Timer",
            size_hint=(None, None),
            size=(150, 30),
            pos_hint={"center_x": 0.5},
            background_normal='',
            background_color=(0.2, 0.6, 0.2, 1),
            font_size=16
        )
        self.start_button.bind(on_press=self.start_timer)
        layout.add_widget(self.start_button)

        # Reset button
        self.reset_button = Button(
            text="Reset Timer",
            size_hint=(None, None),
            size=(150, 30),
            pos_hint={"center_x": 0.5},
            background_normal='',
            background_color=(0.8, 0.2, 0.2, 1),
            font_size=16
        )
        self.reset_button.bind(on_press=self.reset_timer)
        layout.add_widget(self.reset_button)

        # Select Music Button
        self.music_button = Button(
            text="Select Music",
            size_hint=(None, None),
            size=(150, 30),
            pos_hint={"center_x": 0.5},
            background_normal='',
            background_color=(0.6, 0.2, 0.6, 1),
            font_size=16
        )
        self.music_button.bind(on_press=self.go_to_music)
        layout.add_widget(self.music_button)

        # Back button
        back_button = Button(text="Back",
                              size_hint=(None, None),
                                size=(150, 30),
                                  pos_hint={"center_x": 0.5},
                                  font_size=16,
                                  background_color=(0.8, 0.2, 0.2, 1),
                                  )
        back_button.bind(on_press=self.go_backL)
        layout.add_widget(back_button)

        self.add_widget(layout)
    def go_backL(self, instance):
        """Handle 'Go Back' button."""
        self.manager.current = "welcome"

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
            minutes, seconds = divmod(self.time_left, 60)
            self.timer_label.text = f"{minutes:02}:{seconds:02}"
            self.time_left -= 1
        else:
            self.timer_label.text = "Break Time!"
            self.timer_label.font_size = 35
            self.timer_label.color = (1, 1, 1, 1)
            self.timer_running = False
            Clock.unschedule(self.update_timer)
            self.play_break_music()

    def reset_timer(self, instance):
        self.timer_running = False
        self.time_left = 0
        self.timer_label.text = "00:00"
        Clock.unschedule(self.update_timer)
        self.stop_music()

    def go_to_music(self, instance):
        self.manager.current = "music"

    def play_break_music(self):
        global current_music
        if current_music:
            current_music.stop()
        if self.break_music:
            current_music = self.break_music
            current_music.loop = False  # Only play once
            current_music.play()

    def stop_music(self):
        global current_music
        if current_music:
            current_music.stop()


# Define the Music Selection Screen
class MusicScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        layout = BoxLayout(orientation='vertical', spacing=10, padding=20)

        # FileChooser to list only MP3/WAV files
        self.file_chooser = FileChooserListView(
            filters=['*.mp3', '*.wav'],  # Filter for music files
            path=".",  # Start in the current directory
        )
        self.file_chooser.background_color = (0.1, 0.1, 0.1, 1)  # Dark gray background
        self.file_chooser.color = (1, 0, 0, 1)  # White text color
        self.file_chooser.bind(on_selection=self.play_music)  # Play music on selection
        layout.add_widget(self.file_chooser)


        # Play button
        play_button = Button(text="Play Music", size_hint=(None, None), size=(150, 50), background_color=(0.8,2, 0.2, 1), pos_hint={"center_x": 0.5})
        play_button.bind(on_press=self.play_music)
        layout.add_widget(play_button)

        # Back button
        back_button = Button(text="Back", size_hint=(None, None), size=(150, 50), background_color=(1, 0.2, 0.2, 1), pos_hint={"center_x": 0.5})
        back_button.bind(on_press=self.go_back)
        layout.add_widget(back_button)

        self.add_widget(layout)

    def play_music(self, instance):
        global current_music
        if current_music:
            current_music.stop()
        selected_file = self.file_chooser.selection
        if selected_file:
            current_music = SoundLoader.load(selected_file[0])
            if current_music:
                current_music.loop = True
                current_music.play()

    def go_back(self, instance):
        self.manager.current = "main"


# ScreenManager to manage screens
class BuddyApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(WelcomeScreen(name="welcome"))
        sm.add_widget(MainScreen(name="main"))
        sm.add_widget(MusicScreen(name="music"))
        return sm


# Run the app
if __name__ == "__main__":
    BuddyApp().run()
