"""
Login Screen for Qwerich Desktop Application
"""

from kivy.uix.screenmanager import Screen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.label import MDLabel
from kivymd.uix.selectioncontrol import MDSwitch
from kivymd.uix.dialog import MDDialog
from kivy.metrics import dp


class LoginScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.setup_ui()
    
    def setup_ui(self):
        layout = MDBoxLayout(
            orientation="vertical",
            padding=dp(50),
            spacing=dp(20),
            pos_hint={'center_x': 0.5, 'center_y': 0.5},
            size_hint=(0.6, 0.8)
        )
        
        # Title
        title = MDLabel(
            text="Добро пожаловать в Qwerich",
            halign="center",
            theme_text_color="Primary",
            font_style="H4"
        )
        layout.add_widget(title)
        
        subtitle = MDLabel(
            text="Войдите в свой аккаунт",
            halign="center",
            theme_text_color="Secondary",
            font_style="Subtitle1"
        )
        layout.add_widget(subtitle)
        
        # Username/Email field
        self.username_field = MDTextField(
            hint_text="Email или имя пользователя",
            mode="outlined",
            size_hint_y=None,
            height=dp(55)
        )
        layout.add_widget(self.username_field)
        
        # Password field
        self.password_field = MDTextField(
            hint_text="Пароль",
            mode="outlined",
            password=True,
            size_hint_y=None,
            height=dp(55)
        )
        layout.add_widget(self.password_field)
        
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
        
        # Login button
        self.login_button = MDRaisedButton(
            text="Войти",
            size_hint_y=None,
            height=dp(50),
            on_release=self.login
        )
        layout.add_widget(self.login_button)
        
        # Register button
        self.register_button = MDRaisedButton(
            text="Зарегистрироваться",
            size_hint_y=None,
            height=dp(50),
            md_bg_color=(0.2, 0.6, 1, 1),
            on_release=self.go_to_register
        )
        layout.add_widget(self.register_button)
        
        self.add_widget(layout)
    
    def login(self, instance):
        username_or_email = self.username_field.text.strip()
        password = self.password_field.text.strip()
        is_robot_checked = self.robot_checkbox.active
        
        # Validate inputs
        if not username_or_email:
            self.show_error("Введите email или имя пользователя")
            return
        
        if not password:
            self.show_error("Введите пароль")
            return
        
        if not is_robot_checked:
            self.show_error("Подтвердите, что вы не робот")
            return
        
        # Authenticate user
        app = self.manager.parent
        user = app.db.authenticate_user(username_or_email, password)
        
        if user:
            app.current_user = user
            # TODO: Navigate to main screen after successful login
            print(f"Login successful for user: {user['username']}")
        else:
            self.show_error("Неверные учетные данные")
    
    def go_to_register(self, instance):
        self.manager.current = 'register'
    
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