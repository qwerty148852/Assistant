"""
Login Screen for Qwerich Desktop Application
"""

import tkinter as tk
from tkinter import ttk
import ttkbootstrap as ttkb
from ttkbootstrap.constants import *


class LoginScreen(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.setup_ui()
    
    def setup_ui(self):
        # Clear existing widgets
        for widget in self.winfo_children():
            widget.destroy()
            
        # Main frame
        main_frame = ttk.Frame(self)
        main_frame.pack(expand=True, fill='both', padx=50, pady=20)
        
        # Title
        title_label = ttk.Label(
            main_frame,
            text="Добро пожаловать в Qwerich",
            font=("Arial", 24, "bold")
        )
        title_label.pack(pady=(0, 10))
        
        # Subtitle
        subtitle_label = ttk.Label(
            main_frame,
            text="Войдите в свой аккаунт",
            font=("Arial", 14)
        )
        subtitle_label.pack(pady=(0, 30))
        
        # Username/Email field
        username_label = ttk.Label(main_frame, text="Email или имя пользователя:")
        username_label.pack(anchor='w', padx=20)
        
        self.username_var = tk.StringVar()
        self.username_entry = ttk.Entry(
            main_frame,
            textvariable=self.username_var,
            font=("Arial", 12),
            width=30
        )
        self.username_entry.pack(pady=(5, 20), padx=20, fill='x')
        
        # Password field
        password_label = ttk.Label(main_frame, text="Пароль:")
        password_label.pack(anchor='w', padx=20)
        
        self.password_var = tk.StringVar()
        self.password_entry = ttk.Entry(
            main_frame,
            textvariable=self.password_var,
            font=("Arial", 12),
            width=30,
            show="*"
        )
        self.password_entry.pack(pady=(5, 20), padx=20, fill='x')
        
        # "I'm not a robot" checkbox
        self.robot_var = tk.BooleanVar()
        self.robot_checkbox = ttk.Checkbutton(
            main_frame,
            text="Я не робот",
            variable=self.robot_var
        )
        self.robot_checkbox.pack(anchor='w', padx=20, pady=(0, 20))
        
        # Login button
        self.login_button = ttk.Button(
            main_frame,
            text="Войти",
            bootstyle="primary",
            command=self.login
        )
        self.login_button.pack(pady=(0, 10), padx=20, fill='x')
        
        # Register button
        self.register_button = ttk.Button(
            main_frame,
            text="Зарегистрироваться",
            bootstyle="secondary",
            command=self.go_to_register
        )
        self.register_button.pack(pady=(0, 20), padx=20, fill='x')

    def login(self):
        username_or_email = self.username_var.get().strip()
        password = self.password_var.get().strip()
        is_robot_checked = self.robot_var.get()
        
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
        app = self.controller
        user = app.db.authenticate_user(username_or_email, password)
        
        if user:
            app.current_user = user
            # Navigate to main app screen after successful login
            app.show_frame("MainAppScreen")
        else:
            self.show_error("Неверные учетные данные")
    
    def go_to_register(self):
        self.controller.show_frame("RegistrationScreen")
    
    def show_error(self, message):
        error_window = tk.Toplevel(self)
        error_window.title("Ошибка")
        error_window.geometry("300x150")
        error_window.transient(self)
        error_window.grab_set()
        
        ttk.Label(error_window, text=message, wraplength=250).pack(pady=20)
        
        ttk.Button(
            error_window, 
            text="OK", 
            command=error_window.destroy
        ).pack(pady=(0, 20))