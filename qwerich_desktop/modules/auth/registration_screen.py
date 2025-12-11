"""
Registration Screen for Qwerich Desktop Application
"""

import tkinter as tk
from tkinter import ttk
import ttkbootstrap as ttkb
from ttkbootstrap.constants import *
import re


class RegistrationScreen(ttk.Frame):
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
            text="Создать аккаунт",
            font=("Arial", 24, "bold")
        )
        title_label.pack(pady=(0, 10))
        
        # Subtitle
        subtitle_label = ttk.Label(
            main_frame,
            text="Заполните форму регистрации",
            font=("Arial", 14)
        )
        subtitle_label.pack(pady=(0, 30))
        
        # Username field
        username_label = ttk.Label(main_frame, text="Имя пользователя:")
        username_label.pack(anchor='w', padx=20)
        
        self.username_var = tk.StringVar()
        self.username_entry = ttk.Entry(
            main_frame,
            textvariable=self.username_var,
            font=("Arial", 12),
            width=30
        )
        self.username_entry.pack(pady=(5, 20), padx=20, fill='x')
        
        # Email field
        email_label = ttk.Label(main_frame, text="Email:")
        email_label.pack(anchor='w', padx=20)
        
        self.email_var = tk.StringVar()
        self.email_entry = ttk.Entry(
            main_frame,
            textvariable=self.email_var,
            font=("Arial", 12),
            width=30
        )
        self.email_entry.pack(pady=(5, 20), padx=20, fill='x')
        
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
        
        # Confirm password field
        confirm_password_label = ttk.Label(main_frame, text="Повторите пароль:")
        confirm_password_label.pack(anchor='w', padx=20)
        
        self.confirm_password_var = tk.StringVar()
        self.confirm_password_entry = ttk.Entry(
            main_frame,
            textvariable=self.confirm_password_var,
            font=("Arial", 12),
            width=30,
            show="*"
        )
        self.confirm_password_entry.pack(pady=(5, 20), padx=20, fill='x')
        
        # "I'm not a robot" checkbox
        self.robot_var = tk.BooleanVar()
        self.robot_checkbox = ttk.Checkbutton(
            main_frame,
            text="Я не робот",
            variable=self.robot_var
        )
        self.robot_checkbox.pack(anchor='w', padx=20, pady=(0, 20))
        
        # Register button
        self.register_button = ttk.Button(
            main_frame,
            text="Создать аккаунт",
            bootstyle="primary",
            command=self.register
        )
        self.register_button.pack(pady=(0, 10), padx=20, fill='x')
        
        # Back to login button
        self.back_button = ttk.Button(
            main_frame,
            text="Назад к входу",
            bootstyle="secondary",
            command=self.go_to_login
        )
        self.back_button.pack(pady=(0, 20), padx=20, fill='x')
    
    def validate_email(self, email):
        """Validate email format"""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None
    
    def register(self):
        username = self.username_var.get().strip()
        email = self.email_var.get().strip()
        password = self.password_var.get().strip()
        confirm_password = self.confirm_password_var.get().strip()
        is_robot_checked = self.robot_var.get()
        
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
        app = self.controller
        success = app.db.register_user(username, email, password)
        
        if success:
            self.show_success("Регистрация прошла успешно!")
            self.go_to_login()
        else:
            self.show_error("Пользователь с таким email или именем уже существует")
    
    def go_to_login(self):
        self.controller.show_frame("LoginScreen")
    
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
    
    def show_success(self, message):
        success_window = tk.Toplevel(self)
        success_window.title("Успешно")
        success_window.geometry("300x150")
        success_window.transient(self)
        success_window.grab_set()
        
        ttk.Label(success_window, text=message, wraplength=250).pack(pady=20)
        
        ttk.Button(
            success_window, 
            text="OK", 
            command=success_window.destroy
        ).pack(pady=(0, 20))