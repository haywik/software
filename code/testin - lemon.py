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
from kivy.metrics import dp
from kivy.graphics import Color, RoundedRectangle, Rectangle


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

        # Sponsorship text in top-right
        sponsor_label = Label(
            text="By signing up, you agree to our ToS and Conditions.",
            font_size=responsive_font(0.02),
            size_hint=(None, None),
            size=(Window.width * 0.5, dp(30)),
            halign='right',
            valign='middle',
            color=(0.3, 0.3, 0.3, 1),
            pos_hint={"right": 1, "top": 1}
        )
        sponsor_label.bind(size=lambda inst, val: setattr(inst, 'text_size', val))
        self.add_widget(sponsor_label)

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

        if not age_text.isdigit() or int(age_text) < 16:
            self.show_popup("Error", "You do not meet our age requirement.", is_error=True)
            return

        loading_screen = self.screen_manager.get_screen('loading')
        loading_screen.set_user_name(name)
        self.screen_manager.current = 'loading'


# Sign up screen
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
            self.fade_event = Clock.schedule_interval(self.fade_out_music, 0.1)

    def fade_out_music(self, dt):
        if self.bg_music.volume > 0.05:
            self.bg_music.volume -= 0.05
        else:
            self.bg_music.stop()
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


# Connecting
class ConnectingScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=40, spacing=20)
        label = Label(text="Connecting...", font_size=responsive_font(0.045))
        layout.add_widget(label)
        self.add_widget(layout)

    def on_enter(self):
        Clock.schedule_once(self.go_to_chat, 3)

    def go_to_chat(self, dt):
        self.manager.current = 'chat'


# Menu screen
class MenuScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.bg_music = None
        self.layout = BoxLayout(orientation='vertical', padding=40, spacing=20)
        self.label = Label(text="", font_size=responsive_font(0.04), size_hint=(1, 0.1))
        self.layout.add_widget(self.label)

        button_height = 0.12
        font_size = responsive_font(0.035)

        enter_chat_btn = Button(text="Enter A Chat", size_hint=(1, button_height), font_size=font_size)
        enter_chat_btn.bind(on_press=self.go_to_connecting)
        self.layout.add_widget(enter_chat_btn)

        settings_btn = Button(text="Settings", size_hint=(1, button_height), font_size=font_size)
        settings_btn.bind(on_press=self.open_settings)
        self.layout.add_widget(settings_btn)

        help_btn = Button(text="Help", size_hint=(1, button_height), font_size=font_size)
        help_btn.bind(on_press=self.open_help)
        self.layout.add_widget(help_btn)

        quit_btn = Button(
            text="Quit", size_hint=(1, button_height), font_size=font_size,
            on_press=self.exit_app
        )
        self.layout.add_widget(quit_btn)

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
        self.label.text = f"Welcome, {name}!"

    def exit_app(self, instance):
        App.get_running_app().stop()

    def go_to_connecting(self, instance):
        self.manager.current = 'connecting'

    def open_settings(self, instance):
        content = BoxLayout(orientation='vertical', padding=10, spacing=10)
        content.add_widget(Label(text="Settings are not implemented yet. While you wait, visit CATA STUDIOS on roblox!", font_size=responsive_font(0.03)))
        close_btn = Button(text="Close", size_hint=(1, None), height=40)
        content.add_widget(close_btn)
        popup = Popup(title="Settings", content=content, size_hint=(None, None), size=(400, 300))
        close_btn.bind(on_press=popup.dismiss)
        popup.open()

    def open_help(self, instance):
        content = BoxLayout(orientation='vertical', padding=10, spacing=10)
        content.add_widget(Label(text="Help is not implemented yet.", font_size=responsive_font(0.03)))
        close_btn = Button(text="Close", size_hint=(1, None), height=40)
        content.add_widget(close_btn)
        popup = Popup(title="Help", content=content, size_hint=(None, None), size=(400, 300))
        close_btn.bind(on_press=popup.dismiss)
        popup.open()


# Chat screen
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

        back_btn = Button(text="←", size_hint=(None, 1), width=dp(50), font_size=responsive_font(0.05),
                          background_color=(0, 0, 0, 0), color=(1, 1, 1, 1))
        back_btn.bind(on_press=self.go_back)
        top_bar.add_widget(back_btn)
        top_bar.add_widget(Label(text="[APP NAME]", font_size=responsive_font(0.045), bold=True, color=(1, 1, 1, 1)))
        main_layout.add_widget(top_bar)

        # Chat messages container
        chat_body = BoxLayout(orientation='vertical', padding=dp(10), spacing=dp(10))
        self.chat_body = chat_body

        # Received message bubble
        received_msg = Label(
            text="Hey! have you played catastrophic studio's new game?",
            size_hint=(None, None),
            width=Window.width * 0.7,
            text_size=(Window.width * 0.7 - dp(20), None),
            halign='left',
            valign='middle',
            padding=(dp(10), dp(10)),
            font_size=responsive_font(0.035),
            color=(0, 0, 0, 1),
            markup=True,
        )
        received_msg.bind(texture_size=lambda inst, val: setattr(inst, 'height', val[1]))
        received_container = BoxLayout(size_hint_y=None, padding=(dp(10), dp(5), Window.width * 0.3, dp(5)))
        received_container.add_widget(received_msg)
        received_container.bind(minimum_height=received_container.setter('height'))
        with received_msg.canvas.before:
            Color(0.9, 0.9, 0.9, 1)
            received_msg.bg = RoundedRectangle(pos=received_msg.pos, size=received_msg.size, radius=[15])
        received_msg.bind(pos=lambda inst, val: setattr(inst.bg, 'pos', val))
        received_msg.bind(size=lambda inst, val: setattr(inst.bg, 'size', val))

        # Sent message bubble
        sent_msg = Label(
            text="OMG YES! I LOVE secrets of the saharah!",
            size_hint=(None, None),
            width=Window.width * 0.7,
            text_size=(Window.width * 0.7 - dp(20), None),
            halign='left',
            valign='middle',
            padding=(dp(10), dp(10)),
            font_size=responsive_font(0.035),
            color=(1, 1, 1, 1),
            markup=True,
        )
        sent_msg.bind(texture_size=lambda inst, val: setattr(inst, 'height', val[1]))
        sent_container = BoxLayout(size_hint_y=None, padding=(Window.width * 0.3, dp(5), dp(10), dp(5)))
        sent_container.add_widget(sent_msg)
        sent_container.bind(minimum_height=sent_container.setter('height'))
        with sent_msg.canvas.before:
            Color(0.07, 0.37, 0.33, 1)
            sent_msg.bg = RoundedRectangle(pos=sent_msg.pos, size=sent_msg.size, radius=[15])
        sent_msg.bind(pos=lambda inst, val: setattr(inst.bg, 'pos', val))
        sent_msg.bind(size=lambda inst, val: setattr(inst.bg, 'size', val))

        chat_body.add_widget(received_container)
        chat_body.add_widget(sent_container)
        main_layout.add_widget(chat_body)

        # Text input and send button
        input_container = BoxLayout(size_hint_y=None, height=dp(60), padding=dp(5), spacing=dp(5))
        self.chat_input = TextInput(
            multiline=True,
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
        send_btn.bind(on_press=lambda inst: None)  # still a dead button
        input_container.add_widget(send_btn)

        main_layout.add_widget(input_container)
        self.add_widget(main_layout)

    def go_back(self, instance):
        self.manager.current = 'menu'


class MyApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(WelcomeScreen(name='welcome'))
        sm.add_widget(LoadingScreen(name='loading'))
        sm.add_widget(MenuScreen(name='menu'))
        sm.add_widget(ConnectingScreen(name='connecting'))
        sm.add_widget(ChatScreen(name='chat'))
        return sm


if __name__ == '__main__':
    MyApp().run()
