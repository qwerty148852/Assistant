"""
Qwerich Desktop Application - Main Entry Point
A cross-platform desktop application with GUI built with ttkbootstrap
"""

import os
import sys
import tkinter as tk
from tkinter import ttk
import ttkbootstrap as ttkb
from ttkbootstrap.constants import *

# Add project root to path to import modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import modules
from database import Database
from modules.auth.login_screen import LoginScreen
from modules.auth.registration_screen import RegistrationScreen
from modules.main_app_screen import MainAppScreen

class MainApp(ttkb.Window):
    def __init__(self):
        super().__init__()
        self.title("Qwerich Desktop Application")
        self.geometry("1200x800")
        self.db = Database()
        self.current_user = None
        
        # Initialize frames container
        self.frames = {}
        
        # Create main container frame
        container = ttk.Frame(self)
        container.pack(side="top", fill="both", expand=True, padx=10, pady=10)
        
        # Create all screens
        for F in (LoginScreen, RegistrationScreen, MainAppScreen):
            frame = F(parent=container, controller=self)
            self.frames[F.__name__] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        
        # Configure grid weight
        container.rowconfigure(0, weight=1)
        container.columnconfigure(0, weight=1)
        
        # Show initial screen
        self.show_frame("LoginScreen")

    def show_frame(self, frame_name):
        """Show a frame for the given frame name"""
        frame = self.frames[frame_name]
        frame.tkraise()

if __name__ == '__main__':
    app = MainApp()
    app.mainloop()