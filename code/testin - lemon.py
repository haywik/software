from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.clock import Clock
from kivy.uix.textinput import TextInput
import time

from contextlib import asynccontextmanager
import asyncio

class MyLayout(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.orientation = 'vertical'  # top-to-bottom layout
        self.padding = 20
        self.spacing = 10

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



    async def enter_chatroom(self, instance):
        name = self.name_input.text.strip()
        age = self.age_input.text.strip()
        age = int(age)

        if name and age and age >= 16:   #let me try
            # Loading Popup
            popup = Popup(title=f'Welcome, {name}!',
                          content=Label(text=f'Hang on tight as we prepare a few things for you!'),
                          size_hint=(None, None), size=(700, 200))
            popup.open()

        elif name and age and age < 16:
            print("triggered")
            #Age access = DENIED
            popup = Popup(title=f'Error',
                        content=Label(text=f'You do not meet the minimum age requirements.'),
                        size_hint=(None, None), size=(700, 200))
            popup.open()
            asyncio.sleep(5)
            #then have it loop back to main screen
            #No, if its not correct age, we need to kick them out compleately.      or be nice just restart the app
            # But then kids will realise and they will jsut make there age 18+


        else:
            # No entry if no name or age
            popup = Popup(title='Error',
                          content=Label(text='Please enter your name and age first.'),
                          size_hint=(None, None), size=(700, 200))
            popup.open()


class MyApp(App):
    def build(self):
        return MyLayout()


if __name__ == '__main__':
    MyApp().run()
