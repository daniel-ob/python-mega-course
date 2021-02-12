import json
from datetime import datetime

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen

Builder.load_file('design.kv')  # connects .py with .kv


class LoginScreen(Screen):
    def sign_up(self):
        self.manager.transition.direction = "left"
        self.manager.current = "sign_up_screen"

    def login(self, user, pwd):
        with open("users.json") as file:
            users = json.load(file)
        if user in users:
            if users[user]['password'] == pwd:
                self.manager.transition.direction = "left"
                self.manager.current = "main_screen"
            else:
                self.ids.login_wrong.text = "wrong password"
        else:
            self.ids.login_wrong.text = "user does not exists"


class SignUpScreen(Screen):
    def add_user(self, user, pwd):
        # load users file into a dictionary
        with open("users.json") as file:
            users = json.load(file)

        if user:
            if user not in users:
                # add user to dictionary
                datetime_format = "%Y-%m-%d %H:%M:%S.%f"
                users[user] = {'username': user, 'password': pwd, 'created': datetime.now().strftime(datetime_format)}

                # overwrite users file
                with open("users.json", "w") as file:
                    json.dump(users, file)

                self.manager.current = "sign_up_success_screen"
            else:
                self.ids.wrong_signup.text = "Username already exists"
        else:
            self.ids.wrong_signup.text = "Enter a valid username"


class SignUpSuccessScreen(Screen):
    def go_to_login(self):
        self.manager.transition.direction = "right"
        self.manager.current = "login_screen"


class MainScreen(Screen):
    def log_out(self):
        self.manager.transition.direction = "right"
        self.manager.current = "login_screen"


class RootWidget(ScreenManager):
    pass


class MainApp(App):
    def build(self):
        return RootWidget()


if __name__ == "__main__":
    MainApp().run()
