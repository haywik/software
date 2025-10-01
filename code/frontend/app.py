from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout  # <-- ADDED IMPORT
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.popup import Popup
from kivy.clock import Clock
from kivy.core.audio import SoundLoader
from kivy.core.window import Window
from kivy.metrics import dp
from kivy.graphics import Color, Rectangle
import webbrowser

# -------------------- CONFIG --------------------
APP_NAME = "OpenBox [TEMP]"
APP_ICON = "images/icon.png"
font = "Fonts/BebasNeue-Regular.ttf"
ToSTXT = "WARNING: This chat room is ZERO tolerance. No dating, sexual content, personal contact \nsharing, harassment, hate speech, illegal activity, spam, malware, impersonation, or disruption. Break any rule and you \nwill be banned and reported to authorities or platforms. No excuses, no warnings, no exceptions. By staying, you agree \nto follow these rules. You can see more online at:"
# ------------------------------------------------

# Set window icon BEFORE App runs (or it gets glitchy glitchison)
Window.icon = APP_ICON


def responsive_font(percent=0.04):
    return int(Window.height * percent)


# ---------------- Welcome / Sign Up Page ----------------
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
            text=f"Welcome to {APP_NAME}",
            font_size=responsive_font(0.045),
            font_name=font,
            bold=True,
            size_hint=(1, 0.1),
            color=(0.15, 0.35, 0.6, 1)
        ))

        # Name Input
        self.add_widget(Label(text="Name:", size_hint=(1, 0.05), font_size=responsive_font(0.03)))
        self.name_input = TextInput(
            hint_text="Enter your name:",
            font_name=font,
            multiline=False,
            size_hint=(1, 0.08),
            font_size=responsive_font(0.03)
        )
        self.add_widget(self.name_input)

        # Age Input
        self.add_widget(Label(text="Age:", size_hint=(1, 0.05), font_size=responsive_font(0.03)))
        self.age_input = TextInput(
            font_name=font,
            hint_text="Enter your age:",
            multiline=False,
            size_hint=(1, 0.08),
            font_size=responsive_font(0.03),
            input_filter='int'
        )
        self.add_widget(self.age_input)

        # TOS
        tos_label = Label(
            text="By clicking continue, you agree to the [ref=tos][color=1a5999][u]Terms and Conditions[/u][/color][/ref]",
            markup=True,
            font_size=responsive_font(0.025),
            font_name=font,
            size_hint_y=None,
            height=dp(40)
        )
        # This tells the label to wrap its text based on its width, which allows halign to work
        tos_label.bind(width=lambda *x: setattr(tos_label, 'text_size', (tos_label.width, None)))
        tos_label.bind(on_ref_press=self.open_link)


        # Enter button
        enter_button = Button(
            text="Continue",
            font_name=font,
            size_hint=(1, 0.1),
            background_color=(0.15, 0.35, 0.6, 1),
            color=(1, 1, 1, 1),
            font_size=responsive_font(0.035)
        )
        enter_button.bind(on_press=self.enter_chatroom)

        # Add ToS first, then button
        self.add_widget(tos_label)
        self.add_widget(enter_button)

    def open_link(self, instance, value):
        """Called when the Terms and Conditions link is clicked!!!"""
        if value == 'tos':
            webbrowser.open("app.haywik.com/tos")

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

        if not age_text.isdigit() or int(age_text) < 16:
            self.show_popup("Error", "You do not meet our age requirement.", is_error=True)
            return

        loading_screen = self.screen_manager.get_screen('loading')
        loading_screen.set_user_name(name)
        self.screen_manager.current = 'loading'


# ---------------- Screens ----------------
class WelcomeScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.bg_music = None
        self.fade_event = None
        self.music_played = False


    def on_enter(self):
        self.clear_widgets()


        root_layout = FloatLayout()


        welcome_box_layout = WelcomeLayout(screen_manager=self.manager)
        root_layout.add_widget(welcome_box_layout)

        # The developer only code box
        code_input = TextInput(
            hint_text="Code",
            multiline=False,
            size_hint=(0.15, 0.07), # Small size
            pos_hint={'right': 0.98, 'top': 0.98}, # Position top-right
            font_size=responsive_font(0.025)
        )
        code_input.bind(text=self.check_code) # Check code on every text change
        root_layout.add_widget(code_input)

        self.add_widget(root_layout)

        if not self.music_played:
            self.bg_music = SoundLoader.load('audio/menuBg.wav')
            if self.bg_music:
                self.bg_music.volume = 1.0
                self.bg_music.loop = True
                self.bg_music.play()
                self.music_played = True

    def check_code(self, instance, value):
        """Checks the input text and skips to menu if it matches."""
        if value == "3609":
            # Get the menu screen and set a default name
            menu_screen = self.manager.get_screen('menu')
            menu_screen.set_welcome_message("Developer")
            self.manager.current = 'menu'


    def on_pre_leave(self):
        if self.bg_music:
            if self.fade_event:
                self.fade_event.cancel()
            self.fade_event = Clock.schedule_interval(self.fade_out_music, 0.1)

    def fade_out_music(self, dt):
        if self.bg_music.volume > 0.05:
            self.bg_music.volume -= 0.05
        else:
            if self.bg_music:
                self.bg_music.stop()
            self.bg_music = None
            if self.fade_event:
                self.fade_event.cancel()
            self.fade_event = None
            self.music_played = False


class LoadingScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.user_name = ""
        self.layout = BoxLayout(orientation='vertical', padding=40, spacing=20)
        self.label = Label(text="Loading, please wait...", font_size=responsive_font(0.035))
        self.tos = Label(text=f"{ToSTXT}", font_size=responsive_font(0.025))
        self.layout.add_widget(self.label)
        self.layout.add_widget(self.tos)
        self.add_widget(self.layout)

    def set_user_name(self, name):
        self.user_name = name
        Clock.schedule_once(self.go_to_menu, 5)

    def go_to_menu(self, dt):
        menu_screen = self.manager.get_screen('menu')
        menu_screen.set_welcome_message(self.user_name)
        self.manager.current = 'menu'


class ConnectingScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=40, spacing=20)
        label = Label(text="Connecting...", font_size=responsive_font(0.045))
        self.tos2 = Label(text=f"{ToSTXT}", font_size=responsive_font(0.025))
        layout.add_widget(label)
        layout.add_widget(self.tos2)
        self.add_widget(layout)

    def on_enter(self):
        Clock.schedule_once(self.go_to_chat, 3)

    def go_to_chat(self, dt):
        self.manager.current = 'chat'


class MenuScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.bg_music = None
        self.layout = BoxLayout(orientation='vertical', padding=40, spacing=20)

        # Background styling
        with self.layout.canvas.before:
            Color(0.95, 0.95, 0.95, 1)
            self.bg_rect = Rectangle(pos=self.layout.pos, size=self.layout.size)
        self.layout.bind(pos=lambda inst, val: setattr(self.bg_rect, 'pos', val))
        self.layout.bind(size=lambda inst, val: setattr(self.bg_rect, 'size', val))

        # Tokens label
        self.tokens_label = Label(text="Tokens: 0", font_size=responsive_font(0.03),
                                  color=(1.0, 0.843, 0.0, 1),
                                  font_name="Fonts/BebasNeue-Regular.ttf",
                                  size_hint=(1, 0.05), halign='left', valign='middle')
        self.tokens_label.bind(size=lambda inst, val: setattr(inst, 'text_size', val))
        self.layout.add_widget(self.tokens_label)

        self.label = Label(text="", font_size=responsive_font(0.04), size_hint=(1, 0.1))
        self.layout.add_widget(self.label)

        button_height = 0.12
        font_size = responsive_font(0.035)

        def styled_button(text, callback):
            btn = Button(
                text=text,
                size_hint=(1, button_height),
                font_size=font_size,
                background_normal='',
                background_color=(0.15, 0.35, 0.6, 1),
                color=(1, 1, 1, 1)
            )
            btn.bind(on_press=callback)
            return btn

        self.layout.add_widget(styled_button("Connect", self.go_to_connecting))
        self.layout.add_widget(styled_button("Rewards", self.open_rewards))
        self.layout.add_widget(styled_button("Help/Report", self.open_help))
        self.layout.add_widget(styled_button("Exit", self.exit_app))

        self.add_widget(self.layout)

    def on_enter(self):
        if not self.bg_music:
            self.bg_music = SoundLoader.load('audio/mnMenu.wav')
            if self.bg_music:
                self.bg_music.volume = 1.0
                self.bg_music.loop = True
                self.bg_music.play()

    def on_pre_leave(self):
        if self.bg_music:
            self.bg_music.stop()
            self.bg_music = None

    def set_welcome_message(self, name):
        self.label.text = f"Welcome, {name}, to {APP_NAME}!"
        self.label.color = (0.5, 0.5, 0.5, 1)

    def exit_app(self, instance):
        App.get_running_app().stop()

    def go_to_connecting(self, instance):
        self.manager.current = 'connecting'

    def open_rewards(self, instance):
        content = BoxLayout(orientation='vertical', padding=10, spacing=10)
        content.add_widget(Label(text="Buy rewards with your tokens:", font_size=responsive_font(0.03)))
        for reward in ["£5 amazon gift card - 1000 tokens",
                       "Customizabble chat sticker - 100 tokens",
                       "Basic Soundboard - 350 tokens",
                       "Advanced Soundboard - 750 tokens",
                       "£10 Uber gift card - 1750 tokens"]:
            btn = Button(text=reward, size_hint=(1, None), height=40)
            content.add_widget(btn)
        close_btn = Button(text="Close", size_hint=(1, None), height=40)
        content.add_widget(close_btn)
        popup = Popup(title="Rewards", content=content, size_hint=(None, None), size=(400, 400))
        close_btn.bind(on_press=popup.dismiss)
        popup.open()

    def open_help(self, instance):
        content = BoxLayout(orientation='vertical', padding=10, spacing=10)
        content.add_widget(Label(text="Help is being worked on!", font_size=responsive_font(0.03)))
        close_btn = Button(text="Close", size_hint=(1, None), height=40)
        content.add_widget(close_btn)
        popup = Popup(title="Help", content=content, size_hint=(None, None), size=(400, 300))
        close_btn.bind(on_press=popup.dismiss)
        popup.open()


class ChatScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        main_layout = BoxLayout(orientation='vertical')

        # Top bar with back button and title
        top_bar = BoxLayout(size_hint_y=None, height=dp(50), padding=dp(5), spacing=dp(5))
        with top_bar.canvas.before:
            Color(0.07, 0.37, 0.33, 1)
            top_bar.bg_rect = Rectangle(pos=top_bar.pos, size=top_bar.size)
        top_bar.bind(pos=lambda inst, val: setattr(top_bar.bg_rect, 'pos', val))
        top_bar.bind(size=lambda inst, val: setattr(top_bar.bg_rect, 'size', val))

        back_btn = Button(text="Back", size_hint=(None, 1), width=dp(50), font_size=responsive_font(0.05),
                          background_color=(0, 0, 0, 0), color=(1, 1, 1, 1))
        back_btn.bind(on_press=self.go_back)
        top_bar.add_widget(back_btn)
        top_bar.add_widget(Label(text=APP_NAME, font_size=responsive_font(0.045), bold=True, color=(1, 1, 1, 1)))
        main_layout.add_widget(top_bar)

        # Chat messages container
        chat_body = BoxLayout(orientation='vertical', padding=dp(10), spacing=dp(10))
        self.chat_body = chat_body

        main_layout.add_widget(chat_body)

        # Text input and send button
        input_container = BoxLayout(size_hint_y=None, height=dp(60), padding=dp(5), spacing=dp(5))
        self.chat_input = TextInput(
            multiline=False,
            size_hint=(0.85, 1),
            font_size=responsive_font(0.035),
            hint_text="Type your message...",
            padding=(dp(10), dp(10)),
            background_color=(1, 1, 1, 1),
            foreground_color=(0, 0, 0, 1),
        )
        input_container.add_widget(self.chat_input)

        send_btn = Button(
            text="Send",
            size_hint=(0.15, 1),
            font_size=responsive_font(0.035),
            background_color=(0.07, 0.37, 0.33, 1),
            color=(1, 1, 1, 1)
        )
        send_btn.bind(on_press=lambda inst: None)
        input_container.add_widget(send_btn)

        main_layout.add_widget(input_container)
        self.add_widget(main_layout)

    def go_back(self, instance):
        self.manager.current = 'menu'


# ---------------- Application ----------------
class MyApp(App):
    def build(self):

        self.title = APP_NAME
        self.icon = APP_ICON

        sm = ScreenManager()
        sm.add_widget(WelcomeScreen(name='welcome'))
        sm.add_widget(LoadingScreen(name='loading'))
        sm.add_widget(MenuScreen(name='menu'))
        sm.add_widget(ConnectingScreen(name='connecting'))
        sm.add_widget(ChatScreen(name='chat'))
        return sm


if __name__ == '__main__':
    MyApp().run()