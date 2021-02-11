import json
from datetime import datetime

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen

Builder.load_file('design.kv')  # connects .py with .kv


class LoginScreen(Screen):
    def sign_up(self):
        self.manager.current = "sign_up_screen"


class SignUpScreen(Screen):
    def add_user(self, user, pwd):
        # load users file into a dictionary
        with open("users.json") as file:
            users = json.load(file)

        # add user to dictionary
        datetime_format = "%Y-%m-%d %H:%M:%S.%f"
        users[user] = {'username': user, 'password': pwd, 'created': datetime.now().strftime(datetime_format)}

        # overwrite users file
        with open("users.json", "w") as file:
            json.dump(users, file)


class RootWidget(ScreenManager):
    pass


class MainApp(App):
    def build(self):
        return RootWidget()


if __name__ == "__main__":
    MainApp().run()
