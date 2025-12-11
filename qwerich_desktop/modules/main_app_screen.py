"""
Main Application Screen for Qwerich Desktop Application
This is the main screen that appears after successful login
"""

import tkinter as tk
from tkinter import ttk
import ttkbootstrap as ttkb
from ttkbootstrap.constants import *


class MainAppScreen(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.setup_ui()
    
    def setup_ui(self):
        # Clear existing widgets
        for widget in self.winfo_children():
            widget.destroy()
        
        # Create main layout with navigation sidebar and content area
        self.main_container = ttk.Frame(self)
        self.main_container.pack(fill='both', expand=True)
        
        # Navigation sidebar
        self.nav_frame = ttk.Frame(self.main_container, width=200)
        self.nav_frame.pack(side='left', fill='y', padx=(0, 10), pady=10)
        self.nav_frame.pack_propagate(False)  # Maintain fixed width
        
        # Navigation buttons
        nav_buttons = [
            ("Главная", self.show_home),
            ("Чат с Qwerich", self.show_chat),
            ("Системная информация", self.show_system_info),
            ("LAN Мессенджер", self.show_messenger),
            ("Документация", self.show_docs),
            ("Настройки", self.show_settings),
            ("Выйти", self.logout)
        ]
        
        for i, (text, command) in enumerate(nav_buttons):
            btn = ttk.Button(
                self.nav_frame,
                text=text,
                command=command,
                bootstyle="secondary"
            )
            btn.pack(fill='x', pady=2, padx=5)
        
        # Content area
        self.content_frame = ttk.Frame(self.main_container)
        self.content_frame.pack(side='right', fill='both', expand=True, pady=10)
        
        # Show initial content
        self.show_home()
    
    def show_home(self):
        self.clear_content()
        
        # Home content
        home_frame = ttk.Frame(self.content_frame)
        home_frame.pack(fill='both', expand=True)
        
        title_label = ttk.Label(
            home_frame,
            text="Добро пожаловать в Qwerich!",
            font=("Arial", 20, "bold")
        )
        title_label.pack(pady=(0, 20))
        
        welcome_text = (
            "Qwerich - ваш персональный помощник для управления системой и общения.\n\n"
            "Используйте навигационное меню слева для доступа к различным функциям:\n"
            "• Чат с Qwerich - для общения с ассистентом\n"
            "• Системная информация - для мониторинга состояния системы\n"
            "• LAN Мессенджер - для общения с другими пользователями в локальной сети\n"
            "• Документация - для получения справочной информации\n"
            "• Настройки - для настройки приложения"
        )
        
        text_label = ttk.Label(
            home_frame,
            text=welcome_text,
            font=("Arial", 12),
            justify='left'
        )
        text_label.pack(anchor='w', padx=20, pady=10)
    
    def show_chat(self):
        self.clear_content()
        
        # Import the chat screen here to avoid circular imports
        from modules.assistant_chat.chat_screen import ChatScreen
        chat_screen = ChatScreen(self.content_frame, self.controller)
        chat_screen.pack(fill='both', expand=True)
    
    def show_system_info(self):
        self.clear_content()
        
        # Import the system info module here
        from modules.system_info.monitor import SystemMonitor
        sys_frame = ttk.Frame(self.content_frame)
        sys_frame.pack(fill='both', expand=True)
        
        title_label = ttk.Label(
            sys_frame,
            text="Системная информация",
            font=("Arial", 16, "bold")
        )
        title_label.pack(pady=(0, 10))
        
        # Create a text widget to display system info
        info_text = tk.Text(
            sys_frame,
            wrap=tk.WORD,
            state='normal',
            height=20
        )
        info_text.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Create system monitor and get info
        monitor = SystemMonitor()
        all_info = monitor.get_all_info()
        
        # Display system information
        info_text.insert(tk.END, "=== Системная информация ===\n\n")
        
        # CPU Info
        cpu_info = all_info['cpu']
        info_text.insert(tk.END, f"CPU Cores (Physical): {cpu_info['count_physical']}\n")
        info_text.insert(tk.END, f"CPU Cores (Logical): {cpu_info['count_logical']}\n")
        info_text.insert(tk.END, f"CPU Usage (%): {cpu_info['percentages']}\n")
        info_text.insert(tk.END, f"CPU Temperature: {cpu_info['temperature']}°C\n")
        info_text.insert(tk.END, f"CPU Frequency: {cpu_info['freq_current']:.2f} MHz\n\n")
        
        # Memory Info
        mem_info = all_info['memory']
        info_text.insert(tk.END, f"=== Память ===\n")
        info_text.insert(tk.END, f"Total Memory: {mem_info['total']} GB\n")
        info_text.insert(tk.END, f"Used Memory: {mem_info['used']} GB\n")
        info_text.insert(tk.END, f"Available Memory: {mem_info['available']} GB\n")
        info_text.insert(tk.END, f"Memory Usage: {mem_info['percent']}%\n\n")
        
        # Disk Info
        disk_info = all_info['disk']
        info_text.insert(tk.END, f"=== Диски ===\n")
        for disk in disk_info:
            info_text.insert(tk.END, f"Device: {disk['device']}\n")
            info_text.insert(tk.END, f"Mount Point: {disk['mountpoint']}\n")
            info_text.insert(tk.END, f"File System: {disk['file_system']}\n")
            info_text.insert(tk.END, f"Total: {disk['total']} GB\n")
            info_text.insert(tk.END, f"Used: {disk['used']} GB\n")
            info_text.insert(tk.END, f"Free: {disk['free']} GB\n")
            info_text.insert(tk.END, f"Usage: {disk['percent']}%\n")
            info_text.insert(tk.END, "---\n")
        info_text.insert(tk.END, "\n")
        
        # Network Info
        net_info = all_info['network']
        info_text.insert(tk.END, f"=== Сеть ===\n")
        info_text.insert(tk.END, f"Primary IP: {net_info['primary_ip']}\n\n")
        
        info_text.config(state='disabled')
    
    def show_messenger(self):
        self.clear_content()
        
        # Messenger content placeholder
        msg_frame = ttk.Frame(self.content_frame)
        msg_frame.pack(fill='both', expand=True)
        
        title_label = ttk.Label(
            msg_frame,
            text="LAN Мессенджер",
            font=("Arial", 16, "bold")
        )
        title_label.pack(pady=(0, 10))
        
        msg_text = tk.Text(
            msg_frame,
            wrap=tk.WORD,
            state='normal',
            height=15
        )
        msg_text.pack(fill='both', expand=True, padx=10, pady=(0, 10))
        
        msg_text.insert(tk.END, "LAN мессенджер будет работать здесь.\n")
        msg_text.insert(tk.END, "В реальном приложении вы сможете общаться с другими пользователями в локальной сети.\n")
        
        msg_text.config(state='disabled')
    
    def show_docs(self):
        self.clear_content()
        
        # Import the documentation screen here
        from modules.documentation.docs_screen import DocsScreen
        docs_screen = DocsScreen(self.content_frame, self.controller)
        docs_screen.pack(fill='both', expand=True)
    
    def show_settings(self):
        self.clear_content()
        
        # Import the settings screen here
        from modules.settings.settings_screen import SettingsScreen
        settings_screen = SettingsScreen(self.content_frame, self.controller)
        settings_screen.pack(fill='both', expand=True)
    
    def logout(self):
        self.controller.show_frame("LoginScreen")
    
    def clear_content(self):
        for widget in self.content_frame.winfo_children():
            widget.destroy()