from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.textinput import TextInput
from kivy.uix.image import Image
from kivy.core.audio import SoundLoader


class MyLayout(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.orientation = 'vertical'
        self.padding = 40
        self.spacing = 20

        # Background music
        self.bg_music = SoundLoader.load('audio/menuBg.wav')
        if self.bg_music:
            self.bg_music.loop = True
            self.bg_music.volume = 1.0
            self.bg_music.play()
        else:
            print("Failed to load the music.")

        # Add image at the top
        logo = Image(
            source='images/logo.png',
            size_hint=(1, None),
            height=200,
            allow_stretch=True,
            keep_ratio=True
        )
        self.add_widget(logo)

        # Title Label
        title_label = Label(
            text="Welcome to [APP NAME]",
            font_size=28,
            bold=True,
            size_hint=(1, None),
            height=50,
            color=(0.15, 0.35, 0.6, 1)  # Dark blue text
        )
        self.add_widget(title_label)

        # Name prompt
        name_label = Label(
            text="Enter your name:",
            font_size=18,
            size_hint=(1, None),
            height=30,
            color=(0.2, 0.4, 0.7, 1)
        )
        self.add_widget(name_label)

        self.name_input = TextInput(
            hint_text="e.g. Simon",
            multiline=False,
            size_hint_y=None,
            height=40,
            font_size=16,
            background_color=(1, 1, 1, 1),
            foreground_color=(0.1, 0.1, 0.1, 1),
            cursor_color=(0.15, 0.35, 0.6, 1),
            cursor_blink=True,
            padding=[10, 10, 10, 10]
        )
        self.add_widget(self.name_input)

        # Age prompt
        age_label = Label(
            text="Enter your age (not visible to others):",
            font_size=18,
            size_hint=(1, None),
            height=30,
            color=(0.2, 0.4, 0.7, 1)
        )
        self.add_widget(age_label)

        self.age_input = TextInput(
            hint_text="e.g. 27",
            multiline=False,
            size_hint_y=None,
            height=40,
            font_size=16,
            background_color=(1, 1, 1, 1),
            foreground_color=(0.1, 0.1, 0.1, 1),
            cursor_color=(0.15, 0.35, 0.6, 1),
            cursor_blink=True,
            padding=[10, 10, 10, 10]
        )
        self.add_widget(self.age_input)

        # Enter chat button
        enter_button = Button(
            text="Enter Chatroom",
            size_hint=(1, None),
            height=50,
            background_normal='',
            background_color=(0.15, 0.35, 0.6, 1),  # Deep blue
            color=(1, 1, 1, 1),  # White text
            font_size=25,
            bold=True
        )
        enter_button.bind(on_press=self.enter_chatroom)
        self.add_widget(enter_button)

    def create_popup(self, title, message, is_error=False):
        layout = BoxLayout(orientation='vertical', spacing=10, padding=15)

        label_color = (0.7, 0.1, 0.1, 1) if is_error else (0.15, 0.35, 0.6, 1)
        btn_color = (0.7, 0.1, 0.1, 1) if is_error else (0.15, 0.35, 0.6, 1)

        label = Label(text=message, color=label_color, font_size=16)
        btn = Button(
            text="Go Back",
            size_hint=(1, None),
            height=40,
            background_normal='',
            background_color=btn_color,
            color=(1, 1, 1, 1)
        )

        layout.add_widget(label)
        layout.add_widget(btn)

        popup = Popup(
            title=title,
            content=layout,
            size_hint=(None, None),
            size=(500, 200)
        )

        btn.bind(on_press=popup.dismiss)
        popup.open()

    def enter_chatroom(self, instance):
        name = self.name_input.text.strip()
        age_input = self.age_input.text.strip()

        if not age_input.isnumeric():
            age = False
        else:
            age = int(age_input)

        if name and age and age >= 16:
            self.create_popup(
                title=f'Welcome, {name}!',
                message=f'Welcome to the chatroom, {name}!',
                is_error=False
            )

        elif name and age and age < 16:
            self.create_popup(
                title='Error',
                message="You do not meet the minimum age requirements.",
                is_error=True
            )


        else:
            self.create_popup(
                title='Error',
                message='Both name and age are required.',
                is_error=True
            )


class MyApp(App):
    title = "[APP NAME]"
    icon =  "images/icon.png"

    def build(self):
        return MyLayout()


if __name__ == '__main__':
    MyApp().run()
