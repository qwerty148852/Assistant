#!/usr/bin/env python3
"""
Qwerich Desktop Application - Main Entry Point (PySide6 Version)
A cross-platform desktop application with beautiful GUI built with PySide6
"""

import os
import sys
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
    QStackedWidget, QLabel, QPushButton, QLineEdit, QCheckBox, 
    QMessageBox, QFrame, QScrollArea, QTextEdit, QListWidget, QSplitter,
    QSizePolicy
)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QFont, QIcon, QPixmap, QColor, QPalette

# Add project root to path to import modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import modules
from database import Database
from modules.auth.login_screen import LoginScreen
from modules.auth.registration_screen import RegistrationScreen
from modules.main_app_screen import MainAppScreen


class MainApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Qwerich Desktop Application")
        self.setGeometry(100, 100, 1200, 800)
        
        # Apply beautiful theme
        self.apply_theme()
        
        self.db = Database()
        self.current_user = None
        
        # Initialize central widget and stacked widget for navigation
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)
        
        self.stacked_widget = QStackedWidget()
        self.layout.addWidget(self.stacked_widget)
        
        # Create all screens
        self.login_screen = LoginScreen(self)
        self.registration_screen = RegistrationScreen(self)
        self.main_app_screen = MainAppScreen(self)
        
        # Add screens to stacked widget
        self.stacked_widget.addWidget(self.login_screen)
        self.stacked_widget.addWidget(self.registration_screen)
        self.stacked_widget.addWidget(self.main_app_screen)
        
        # Show initial screen
        self.show_login_screen()

    def show_login_screen(self):
        self.stacked_widget.setCurrentWidget(self.login_screen)
        self.setWindowTitle("Qwerich Desktop Application - Вход")

    def show_registration_screen(self):
        self.stacked_widget.setCurrentWidget(self.registration_screen)
        self.setWindowTitle("Qwerich Desktop Application - Регистрация")

    def show_main_app_screen(self):
        self.stacked_widget.setCurrentWidget(self.main_app_screen)
        self.setWindowTitle(f"Qwerich Desktop Application - Привет, {self.current_user['username']}!")

    def apply_theme(self):
        """Apply beautiful dark theme"""
        palette = self.palette()
        palette.setColor(QPalette.Window, QColor(45, 45, 48))
        palette.setColor(QPalette.WindowText, QColor(231, 231, 231))
        palette.setColor(QPalette.Base, QColor(30, 30, 30))
        palette.setColor(QPalette.AlternateBase, QColor(45, 45, 48))
        palette.setColor(QPalette.ToolTipBase, QColor(255, 255, 220))
        palette.setColor(QPalette.ToolTipText, QColor(0, 0, 0))
        palette.setColor(QPalette.Text, QColor(231, 231, 231))
        palette.setColor(QPalette.Button, QColor(60, 63, 65))
        palette.setColor(QPalette.ButtonText, QColor(231, 231, 231))
        palette.setColor(QPalette.BrightText, QColor(255, 0, 0))
        palette.setColor(QPalette.Highlight, QColor(61, 174, 233))
        palette.setColor(QPalette.HighlightedText, QColor(0, 0, 0))
        self.setPalette(palette)
        
        # Set application style sheet for better appearance
        self.setStyleSheet("""
            QMainWindow {
                background-color: #2d2d30;
            }
            
            QPushButton {
                background-color: #3c3f41;
                border: 1px solid #555555;
                border-radius: 5px;
                padding: 8px;
                color: #e7e7e7;
                font-size: 14px;
            }
            
            QPushButton:hover {
                background-color: #4a4d4f;
            }
            
            QPushButton:pressed {
                background-color: #323537;
            }
            
            QPushButton#primary {
                background-color: #0078d4;
                border: 1px solid #0078d4;
                color: white;
            }
            
            QPushButton#primary:hover {
                background-color: #106ebe;
            }
            
            QPushButton#secondary {
                background-color: #686868;
                border: 1px solid #686868;
                color: white;
            }
            
            QPushButton#secondary:hover {
                background-color: #787878;
            }
            
            QLineEdit {
                background-color: #333333;
                border: 1px solid #555555;
                border-radius: 5px;
                padding: 8px;
                color: #e7e7e7;
                font-size: 14px;
            }
            
            QLineEdit:focus {
                border: 1px solid #0078d4;
            }
            
            QLabel {
                color: #e7e7e7;
                font-size: 14px;
            }
            
            QFrame {
                border: 1px solid #555555;
                border-radius: 5px;
            }
            
            QTextEdit, QListWidget {
                background-color: #333333;
                border: 1px solid #555555;
                border-radius: 5px;
                color: #e7e7e7;
            }
            
            QScrollBar:vertical {
                background: #3c3f41;
                width: 15px;
                border-radius: 7px;
            }
            
            QScrollBar::handle:vertical {
                background: #686868;
                border-radius: 7px;
                min-height: 20px;
            }
            
            QScrollBar::handle:vertical:hover {
                background: #787878;
            }
        """)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    
    # Set application properties
    app.setApplicationName("Qwerich Desktop Application")
    app.setApplicationVersion("1.0")
    
    window = MainApp()
    window.show()
    
    sys.exit(app.exec())