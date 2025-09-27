from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.spinner import Spinner
from kivy.clock import Clock
from kivy.uix.image import Image

name = input("Enter your name: ")

# --- Screens ---
class LoadingScreen(Screen):
    def on_enter(self):
        # Simulate loading work with a delay
        Clock.schedule_once(self.switch_to_main, 3)  # 3 seconds

    def switch_to_main(self, dt):
        self.manager.current = 'main'

class MainScreen(Screen):
    def on_enter(self):
        print("Main screen loaded")

# --- App ---
class LoadingApp(App):
    def build(self):
        sm = ScreenManager(transition=FadeTransition())

        # Loading Screen UI
        loading_layout = BoxLayout(orientation='vertical', spacing=10, padding=50)
        loading_layout.add_widget(Label(text='Loading, please wait a few moments for lemon to load...', font_size=24))
        loading_layout.add_widget(Spinner(text='Loading...', values=('Loading...',), size_hint=(None, None), size=(100, 44)))
        loading_screen = LoadingScreen(name='loading')
        loading_screen.add_widget(loading_layout)

        # Main Screen UI
        main_layout = BoxLayout(orientation='vertical', padding=50)
        main_layout.add_widget(Label(text=f'Welcome to the Chat! {name}', font_size=32))
        main_screen = MainScreen(name='main')
        main_screen.add_widget(main_layout)

        sm.add_widget(loading_screen)
        sm.add_widget(main_screen)

        return sm

if __name__ == '__main__':
    LoadingApp().run()
