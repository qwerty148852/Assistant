"""
Qwerich Desktop Application - Main Entry Point
A cross-platform desktop application with GUI built with Kivy and KivyMD
"""

import os
import sys
from kivy.core.window import Window
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.lang import Builder

# Add project root to path to import modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import modules
from database import Database
from modules.auth.login_screen import LoginScreen
from modules.auth.registration_screen import RegistrationScreen

# Load main KV file
Builder.load_file('styles/themes.kv')

class MainApp(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.db = Database()
        self.current_user = None
        
    def build(self):
        # Set window size
        Window.size = (1200, 800)
        
        # Create screen manager
        sm = ScreenManager()
        
        # Add screens
        sm.add_widget(LoginScreen(name='login'))
        sm.add_widget(RegistrationScreen(name='register'))
        
        return sm

if __name__ == '__main__':
    MainApp().run()