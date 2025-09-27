from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.clock import Clock
from kivy.uix.textinput import TextInput
from kivy.core.audio import SoundLoader
import time

from contextlib import asynccontextmanager
import asyncio

'''

#SOUNDS:
self.background_music = SoundLoader.load('bg_menu.mp3)





'''











class MyLayout(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.orientation = 'vertical'  # top-to-bottom layout
        self.padding = 20
        self.spacing = 10

        if self.background_music:
            self.background_music.loop = True
            self.background_music.play()

        # Title
        self.add_widget(Label(text="Please enter your name to begin talking!"))

        # Name
        self.name_input = TextInput(hint_text="Enter name.", multiline=False)
        self.add_widget(self.name_input)

        #another title
        self.add_widget(Label(text="Please enter your age. (This will not be shown to anyone.)"))

        # Age
        self.age_input = TextInput(hint_text="Enter Age.", multiline=False)
        self.add_widget(self.age_input)

        # Enter
        enter_button = Button(text="Click me to enter the chat room")
        enter_button.bind(on_press=self.enter_chatroom)
        self.add_widget(enter_button)



    def enter_chatroom(self, instance):
        age = False
        name = False
        name = self.name_input.text.strip()
        age = self.age_input.text.strip()

        if not age.isnumeric():
            age = False
        else:
            age = int(age)




        if name and age and age >= 16:   #let me try
            # Loading Popup
            popup = Popup(title=f'Welcome, {name}!',
                          content=Label(text=f'Hang on tight as we prepare a few things for you!'),
                          size_hint=(None, None), size=(700, 200))
            popup.open()


        elif name and age and age < 16:


            # Create a layout to hold multiple widgets
            layout = BoxLayout(orientation='vertical', spacing=10, padding=10)

            # Add label and button
            message = Label(text="You do not meet the minimum age requirements.")
            btn = Button(text="Go Back")
            layout.add_widget(message)
            layout.add_widget(btn)

            # Create popup
            popup = Popup(
                title='Error',
                content=layout,
                size_hint=(None, None),
                size=(700, 200)
            )

            # Close
            btn.bind(on_press=popup.dismiss)

            # Show
            popup.open()




        else:
            # No entry if no name or age
            popup = Popup(title='Error',
                          content=Label(text='Age and Name required.'),
                          size_hint=(None, None), size=(700, 200))
            popup.open()


class MyApp(App):
    def build(self):
        return MyLayout()


if __name__ == '__main__':
    MyApp().run()
