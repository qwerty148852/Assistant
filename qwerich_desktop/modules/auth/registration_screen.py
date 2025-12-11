"""
Registration Screen for Qwerich Desktop Application
"""

from kivy.uix.screenmanager import Screen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.label import MDLabel
from kivymd.uix.selectioncontrol import MDSwitch
from kivymd.uix.dialog import MDDialog
from kivy.metrics import dp
import re


class RegistrationScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.setup_ui()
    
    def setup_ui(self):
        layout = MDBoxLayout(
            orientation="vertical",
            padding=dp(50),
            spacing=dp(20),
            pos_hint={'center_x': 0.5, 'center_y': 0.5},
            size_hint=(0.6, 0.9)
        )
        
        # Title
        title = MDLabel(
            text="Создать аккаунт",
            halign="center",
            theme_text_color="Primary",
            font_style="H4"
        )
        layout.add_widget(title)
        
        subtitle = MDLabel(
            text="Заполните форму регистрации",
            halign="center",
            theme_text_color="Secondary",
            font_style="Subtitle1"
        )
        layout.add_widget(subtitle)
        
        # Username field
        self.username_field = MDTextField(
            hint_text="Имя пользователя",
            mode="outlined",
            size_hint_y=None,
            height=dp(55)
        )
        layout.add_widget(self.username_field)
        
        # Email field
        self.email_field = MDTextField(
            hint_text="Email",
            mode="outlined",
            size_hint_y=None,
            height=dp(55)
        )
        layout.add_widget(self.email_field)
        
        # Password field
        self.password_field = MDTextField(
            hint_text="Пароль",
            mode="outlined",
            password=True,
            size_hint_y=None,
            height=dp(55)
        )
        layout.add_widget(self.password_field)
        
        # Confirm password field
        self.confirm_password_field = MDTextField(
            hint_text="Повторите пароль",
            mode="outlined",
            password=True,
            size_hint_y=None,
            height=dp(55)
        )
        layout.add_widget(self.confirm_password_field)
        
        # "I'm not a robot" checkbox
        checkbox_layout = MDBoxLayout(
            orientation="horizontal",
            size_hint_y=None,
            height=dp(40)
        )
        
        self.robot_checkbox = MDSwitch()
        checkbox_layout.add_widget(self.robot_checkbox)
        
        checkbox_label = MDLabel(
            text="Я не робот",
            theme_text_color="Secondary",
            halign="left",
            valign="middle"
        )
        checkbox_layout.add_widget(checkbox_label)
        
        layout.add_widget(checkbox_layout)
        
        # Register button
        self.register_button = MDRaisedButton(
            text="Создать аккаунт",
            size_hint_y=None,
            height=dp(50),
            on_release=self.register
        )
        layout.add_widget(self.register_button)
        
        # Back to login button
        self.back_button = MDRaisedButton(
            text="Назад к входу",
            size_hint_y=None,
            height=dp(50),
            md_bg_color=(0.2, 0.6, 1, 1),
            on_release=self.go_to_login
        )
        layout.add_widget(self.back_button)
        
        self.add_widget(layout)
    
    def validate_email(self, email):
        """Validate email format"""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None
    
    def register(self, instance):
        username = self.username_field.text.strip()
        email = self.email_field.text.strip()
        password = self.password_field.text.strip()
        confirm_password = self.confirm_password_field.text.strip()
        is_robot_checked = self.robot_checkbox.active
        
        # Validate inputs
        if not username:
            self.show_error("Введите имя пользователя")
            return
        
        if not email:
            self.show_error("Введите email")
            return
        
        if not self.validate_email(email):
            self.show_error("Некорректный формат email")
            return
        
        if not password:
            self.show_error("Введите пароль")
            return
        
        if len(password) < 6:
            self.show_error("Пароль должен содержать не менее 6 символов")
            return
        
        if password != confirm_password:
            self.show_error("Пароли не совпадают")
            return
        
        if not is_robot_checked:
            self.show_error("Подтвердите, что вы не робот")
            return
        
        # Register user
        app = self.manager.parent
        success = app.db.register_user(username, email, password)
        
        if success:
            self.show_success("Регистрация прошла успешно!")
            self.go_to_login(None)
        else:
            self.show_error("Пользователь с таким email или именем уже существует")
    
    def go_to_login(self, instance):
        self.manager.current = 'login'
    
    def show_error(self, message):
        dialog = MDDialog(
            title="Ошибка",
            text=message,
            buttons=[
                MDRaisedButton(
                    text="OK",
                    on_release=lambda x: dialog.dismiss()
                )
            ]
        )
        dialog.open()
    
    def show_success(self, message):
        dialog = MDDialog(
            title="Успешно",
            text=message,
            buttons=[
                MDRaisedButton(
                    text="OK",
                    on_release=lambda x: dialog.dismiss()
                )
            ]
        )
        dialog.open()