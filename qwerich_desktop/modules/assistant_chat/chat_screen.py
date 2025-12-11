"""
Chat Screen for Qwerich Desktop Application
GUI component for the chat functionality
"""

import tkinter as tk
from tkinter import ttk
import ttkbootstrap as ttkb
from ttkbootstrap.constants import *
from .chat_engine import ChatEngine


class ChatScreen(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.chat_engine = ChatEngine()
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
            text="Чат с Qwerich",
            font=("Arial", 16, "bold")
        )
        title_label.pack(pady=(0, 10))
        
        # Chat display area
        self.chat_display = tk.Text(
            main_frame,
            wrap=tk.WORD,
            state='disabled',
            height=15,
            font=("Arial", 11)
        )
        
        # Add scrollbar to chat display
        chat_scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=self.chat_display.yview)
        self.chat_display.configure(yscrollcommand=chat_scrollbar.set)
        
        # Pack chat display and scrollbar
        chat_frame = ttk.Frame(main_frame)
        chat_frame.pack(fill='both', expand=True, pady=(0, 10))
        
        self.chat_display.pack(side='left', fill='both', expand=True)
        chat_scrollbar.pack(side='right', fill='y')
        
        # Input frame
        input_frame = ttk.Frame(main_frame)
        input_frame.pack(fill='x')
        
        self.chat_input = ttk.Entry(input_frame, font=("Arial", 11))
        self.chat_input.pack(side='left', fill='x', expand=True, padx=(0, 10))
        
        send_button = ttk.Button(
            input_frame,
            text="Отправить",
            bootstyle="primary",
            command=self.send_message
        )
        send_button.pack(side='right')
        
        # Bind Enter key to send message
        self.chat_input.bind('<Return>', lambda event: self.send_message())
        
        # Add initial message
        self.display_message("Qwerich: Привет! Я ваш виртуальный ассистент. Спросите меня что-нибудь!")
    
    def send_message(self):
        message = self.chat_input.get().strip()
        if message:
            self.display_message(f"Вы: {message}")
            self.chat_input.delete(0, tk.END)
            
            # Get response from chat engine
            response = self.chat_engine.get_response(message)
            self.display_message(f"Qwerich: {response}")
    
    def display_message(self, message):
        # Enable text widget, add message, then disable again
        self.chat_display.config(state='normal')
        self.chat_display.insert(tk.END, message + "\n")
        self.chat_display.config(state='disabled')
        self.chat_display.see(tk.END)  # Scroll to bottom