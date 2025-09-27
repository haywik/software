from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.popup import Popup
from kivy.clock import Clock
from kivy.core.audio import SoundLoader
from kivy.core.window import Window


def responsive_font(percent=0.04):
    return int(Window.height * percent)


# welcome/sign up page
class WelcomeLayout(BoxLayout):
    def __init__(self, screen_manager, **kwargs):
        super().__init__(**kwargs)
        self.screen_manager = screen_manager
        self.orientation = 'vertical'
        self.padding = [Window.width * 0.05, Window.height * 0.05]
        self.spacing = Window.height * 0.02

        # Logo
        logo = Image(
            source='images/logo.png',
            size_hint=(1, 0.3),
            allow_stretch=True,
            keep_ratio=True
        )
        self.add_widget(logo)

        # Title
        self.add_widget(Label(
            text="Welcome to [APP NAME]",
            font_size=responsive_font(0.045),
            bold=True,
            size_hint=(1, 0.1),
            color=(0.15, 0.35, 0.6, 1)
        ))

        # Name Input
        self.add_widget(Label(text="Name:", size_hint=(1, 0.05), font_size=responsive_font(0.03)))
        self.name_input = TextInput(
            hint_text="Enter your name:",
            multiline=False,
            size_hint=(1, 0.08),
            font_size=responsive_font(0.03)
        )
        self.add_widget(self.name_input)

        # Age Input
        self.add_widget(Label(text="Age:", size_hint=(1, 0.05), font_size=responsive_font(0.03)))
        self.age_input = TextInput(
            hint_text="Enter your age:",
            multiline=False,
            size_hint=(1, 0.08),
            font_size=responsive_font(0.03),
            input_filter='int'
        )
        self.add_widget(self.age_input)

        # Enter button
        enter_button = Button(
            text="Create Account",
            size_hint=(1, 0.1),
            background_color=(0.15, 0.35, 0.6, 1),
            color=(1, 1, 1, 1),
            font_size=responsive_font(0.035)
        )
        enter_button.bind(on_press=self.enter_chatroom)
        self.add_widget(enter_button)

    def show_popup(self, title, message, is_error=False):
        color = (0.7, 0.1, 0.1, 1) if is_error else (0.15, 0.35, 0.6, 1)
        layout = BoxLayout(orientation='vertical', padding=15, spacing=10)
        label = Label(text=message, color=color, font_size=responsive_font(0.03))
        btn = Button(text="Close", size_hint=(1, None), height=40, background_color=color, color=(1, 1, 1, 1))
        layout.add_widget(label)
        layout.add_widget(btn)
        popup = Popup(title=title, content=layout, size_hint=(None, None), size=(700, 200))
        btn.bind(on_press=popup.dismiss)
        popup.open()

    def enter_chatroom(self, instance):
        name = self.name_input.text.strip()
        age_text = self.age_input.text.strip()

        if not name or not age_text:
            self.show_popup("Error", "Both name and age are required to sign up.", is_error=True)
            return

        if not age_text.isdigit() or int(age_text) < 16 or int(age_text) > 122:
            self.show_popup("Error", "You do not meet our age requirement.", is_error=True)
            # terminate
            return

        loading_screen = self.screen_manager.get_screen('loading')
        loading_screen.set_user_name(name)
        self.screen_manager.current = 'loading'


# Sign up screen/acc screen
class WelcomeScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.bg_music = None
        self.fade_event = None
        self.music_played = False
        self.layout = None

    def on_enter(self):
        self.clear_widgets()
        self.layout = WelcomeLayout(screen_manager=self.manager)
        self.add_widget(self.layout)

        if not self.music_played:
            self.bg_music = SoundLoader.load('audio/menuBg.wav')
            if self.bg_music:
                self.bg_music.volume = 1.0
                self.bg_music.loop = True
                self.bg_music.play()
                self.music_played = True

    def on_pre_leave(self):
        if self.bg_music:
            if self.fade_event:
                self.fade_event.cancel()
            # slower fade: reduce volume by 0.05 every 0.1 sec (5 seconds total fade)
            self.fade_event = Clock.schedule_interval(self.fade_out_music, 0.1)

    def fade_out_music(self, dt):
        if self.bg_music.volume > 0.05:
            self.bg_music.volume -= 0.05
        else:
            self.bg_music.stop()
            self.bg_music.unload()
            self.bg_music = None
            self.fade_event.cancel()
            self.fade_event = None
            self.music_played = False


# Loading...
class LoadingScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.user_name = ""
        self.layout = BoxLayout(orientation='vertical', padding=40, spacing=20)
        self.label = Label(text="Loading, please wait...", font_size=responsive_font(0.035))
        self.layout.add_widget(self.label)
        self.add_widget(self.layout)

    def set_user_name(self, name):
        self.user_name = name
        Clock.schedule_once(self.go_to_menu, 5)

    def go_to_menu(self, dt):
        menu_screen = self.manager.get_screen('menu')
        menu_screen.set_welcome_message(self.user_name)
        self.manager.current = 'menu'


# menu screen
class MenuScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.bg_music = None
        self.layout = BoxLayout(orientation='vertical', padding=40, spacing=20)
        self.label = Label(text="", font_size=responsive_font(0.04), size_hint=(1, 0.1))
        self.layout.add_widget(self.label)

        button_height = 0.12
        font_size = responsive_font(0.035)

        for text in ["Enter A Chat", "Settings", "Help"]:
            self.layout.add_widget(Button(text=text, size_hint=(1, button_height), font_size=font_size))

        self.layout.add_widget(Button(
            text="Quit", size_hint=(1, button_height), font_size=font_size,
            on_press=self.exit_app
        ))

        self.add_widget(self.layout)

    def on_enter(self):
        # Play menu music here (different track)
        if not self.bg_music:
            self.bg_music = SoundLoader.load('audio/mnMenu.wav')
            if self.bg_music:
                self.bg_music.volume = 1.0
                self.bg_music.loop = True
                self.bg_music.play()

    def on_pre_leave(self):
        # Stop menu music immediately on leaving
        if self.bg_music:
            self.bg_music.stop()
            self.bg_music.unload()
            self.bg_music = None

    def set_welcome_message(self, name):
        self.label.text = f"Welcome, {name}!"

    def exit_app(self, instance):
        App.get_running_app().stop()


# ---------------- MAIN APP ---------------- #
class MyApp(App):
    title = "[APP NAME]"
    icon = "images/icon.png"

    def build(self):
        sm = ScreenManager()
        sm.add_widget(WelcomeScreen(name='welcome'))
        sm.add_widget(LoadingScreen(name='loading'))
        sm.add_widget(MenuScreen(name='menu'))
        sm.current = 'welcome'
        return sm


if __name__ == '__main__':
    MyApp().run()
