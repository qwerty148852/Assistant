"""
Settings Screen for Qwerich Desktop Application
GUI component for the settings functionality
"""

import tkinter as tk
from tkinter import ttk
import ttkbootstrap as ttkb
from ttkbootstrap.constants import *


class SettingsScreen(ttk.Frame):
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
        main_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        title_label = ttk.Label(
            main_frame,
            text="Настройки",
            font=("Arial", 16, "bold")
        )
        title_label.pack(pady=(0, 20))
        
        # Create notebook for different setting categories
        notebook = ttk.Notebook(main_frame)
        notebook.pack(fill='both', expand=True)
        
        # Appearance tab
        self.create_appearance_tab(notebook)
        
        # Account tab
        self.create_account_tab(notebook)
        
        # Privacy tab
        self.create_privacy_tab(notebook)
        
        # Messenger tab
        self.create_messenger_tab(notebook)
    
    def create_appearance_tab(self, notebook):
        appearance_frame = ttk.Frame(notebook)
        notebook.add(appearance_frame, text="Внешний вид")
        
        # Theme selection
        theme_label = ttk.Label(appearance_frame, text="Выберите тему:")
        theme_label.pack(anchor='w', padx=20, pady=(20, 5))
        
        theme_options = [
            "Deep Forest (Основная)",
            "Ocean Blue", 
            "Dark Amethyst",
            "Light Breeze",
            "True Black"
        ]
        
        self.theme_var = tk.StringVar()
        theme_combo = ttk.Combobox(
            appearance_frame,
            textvariable=self.theme_var,
            values=theme_options,
            state="readonly"
        )
        theme_combo.pack(anchor='w', padx=20, pady=5)
        theme_combo.set(theme_options[0])  # Default selection
        
        # Animation toggle
        self.animation_var = tk.BooleanVar(value=True)
        animation_check = ttk.Checkbutton(
            appearance_frame,
            text="Включить анимации",
            variable=self.animation_var
        )
        animation_check.pack(anchor='w', padx=20, pady=10)
        
        # Font size selection
        font_label = ttk.Label(appearance_frame, text="Размер шрифта:")
        font_label.pack(anchor='w', padx=20, pady=(20, 5))
        
        font_options = ["Маленький", "Нормальный", "Большой", "Очень большой"]
        self.font_var = tk.StringVar()
        font_combo = ttk.Combobox(
            appearance_frame,
            textvariable=self.font_var,
            values=font_options,
            state="readonly"
        )
        font_combo.pack(anchor='w', padx=20, pady=5)
        font_combo.set(font_options[1])  # Default to normal
    
    def create_account_tab(self, notebook):
        account_frame = ttk.Frame(notebook)
        notebook.add(account_frame, text="Учетная запись")
        
        # Current user info
        if self.controller.current_user:
            user_info = f"Текущий пользователь: {self.controller.current_user['username']}"
            user_label = ttk.Label(account_frame, text=user_info)
            user_label.pack(anchor='w', padx=20, pady=20)
        
        # Change username
        username_label = ttk.Label(account_frame, text="Имя пользователя:")
        username_label.pack(anchor='w', padx=20, pady=(10, 5))
        
        self.username_var = tk.StringVar()
        if self.controller.current_user:
            self.username_var.set(self.controller.current_user['username'])
        
        username_entry = ttk.Entry(account_frame, textvariable=self.username_var)
        username_entry.pack(anchor='w', padx=20, pady=5, fill='x')
        
        # Change email
        email_label = ttk.Label(account_frame, text="Email:")
        email_label.pack(anchor='w', padx=20, pady=(10, 5))
        
        self.email_var = tk.StringVar()
        if self.controller.current_user:
            self.email_var.set(self.controller.current_user['email'])
        
        email_entry = ttk.Entry(account_frame, textvariable=self.email_var)
        email_entry.pack(anchor='w', padx=20, pady=5, fill='x')
        
        # Change password
        password_label = ttk.Label(account_frame, text="Новый пароль:")
        password_label.pack(anchor='w', padx=20, pady=(10, 5))
        
        self.password_var = tk.StringVar()
        password_entry = ttk.Entry(account_frame, textvariable=self.password_var, show="*")
        password_entry.pack(anchor='w', padx=20, pady=5, fill='x')
        
        confirm_label = ttk.Label(account_frame, text="Подтвердите пароль:")
        confirm_label.pack(anchor='w', padx=20, pady=(10, 5))
        
        self.confirm_var = tk.StringVar()
        confirm_entry = ttk.Entry(account_frame, textvariable=self.confirm_var, show="*")
        confirm_entry.pack(anchor='w', padx=20, pady=5, fill='x')
        
        # Save button
        save_btn = ttk.Button(
            account_frame,
            text="Сохранить изменения",
            bootstyle="primary",
            command=self.save_account_changes
        )
        save_btn.pack(pady=20)
    
    def create_privacy_tab(self, notebook):
        privacy_frame = ttk.Frame(notebook)
        notebook.add(privacy_frame, text="Конфиденциальность")
        
        # Data collection toggle
        self.data_collection_var = tk.BooleanVar(value=True)
        data_check = ttk.Checkbutton(
            privacy_frame,
            text="Разрешить анонимную сбору статистики",
            variable=self.data_collection_var
        )
        data_check.pack(anchor='w', padx=20, pady=10)
        
        # Data sharing toggle
        self.data_sharing_var = tk.BooleanVar(value=False)
        sharing_check = ttk.Checkbutton(
            privacy_frame,
            text="Разрешить обмен данными с другими пользователями",
            variable=self.data_sharing_var
        )
        sharing_check.pack(anchor='w', padx=20, pady=10)
        
        # Save button
        save_btn = ttk.Button(
            privacy_frame,
            text="Сохранить настройки",
            bootstyle="primary",
            command=self.save_privacy_settings
        )
        save_btn.pack(pady=20)
    
    def create_messenger_tab(self, notebook):
        messenger_frame = ttk.Frame(notebook)
        notebook.add(messenger_frame, text="Мессенджер")
        
        # Port setting
        port_label = ttk.Label(messenger_frame, text="Порт для мессенджера:")
        port_label.pack(anchor='w', padx=20, pady=(20, 5))
        
        self.port_var = tk.StringVar(value="12345")
        port_entry = ttk.Entry(messenger_frame, textvariable=self.port_var)
        port_entry.pack(anchor='w', padx=20, pady=5)
        
        # Nickname setting
        nickname_label = ttk.Label(messenger_frame, text="Никнейм в сети:")
        nickname_label.pack(anchor='w', padx=20, pady=(20, 5))
        
        self.nickname_var = tk.StringVar()
        if self.controller.current_user:
            self.nickname_var.set(self.controller.current_user['username'])
        
        nickname_entry = ttk.Entry(messenger_frame, textvariable=self.nickname_var)
        nickname_entry.pack(anchor='w', padx=20, pady=5)
        
        # Sound notifications
        self.sound_var = tk.BooleanVar(value=True)
        sound_check = ttk.Checkbutton(
            messenger_frame,
            text="Включить звуковые уведомления",
            variable=self.sound_var
        )
        sound_check.pack(anchor='w', padx=20, pady=10)
        
        # Save button
        save_btn = ttk.Button(
            messenger_frame,
            text="Сохранить настройки",
            bootstyle="primary",
            command=self.save_messenger_settings
        )
        save_btn.pack(pady=20)
    
    def save_account_changes(self):
        # In a real app, this would save changes to the database
        success_msg = tk.Toplevel(self)
        success_msg.title("Успешно")
        success_msg.geometry("300x100")
        success_msg.transient(self)
        success_msg.grab_set()
        
        ttk.Label(success_msg, text="Изменения сохранены!").pack(pady=20)
        
        ttk.Button(
            success_msg, 
            text="OK", 
            command=success_msg.destroy
        ).pack(pady=(0, 20))
    
    def save_privacy_settings(self):
        # In a real app, this would save privacy settings
        success_msg = tk.Toplevel(self)
        success_msg.title("Успешно")
        success_msg.geometry("300x100")
        success_msg.transient(self)
        success_msg.grab_set()
        
        ttk.Label(success_msg, text="Настройки конфиденциальности сохранены!").pack(pady=20)
        
        ttk.Button(
            success_msg, 
            text="OK", 
            command=success_msg.destroy
        ).pack(pady=(0, 20))
    
    def save_messenger_settings(self):
        # In a real app, this would save messenger settings
        success_msg = tk.Toplevel(self)
        success_msg.title("Успешно")
        success_msg.geometry("300x100")
        success_msg.transient(self)
        success_msg.grab_set()
        
        ttk.Label(success_msg, text="Настройки мессенджера сохранены!").pack(pady=20)
        
        ttk.Button(
            success_msg, 
            text="OK", 
            command=success_msg.destroy
        ).pack(pady=(0, 20))