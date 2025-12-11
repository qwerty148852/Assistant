"""
Main Application Screen for Qwerich Desktop Application (PySide6 Version)
This is the main screen that appears after successful login
"""

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, 
    QTextEdit, QFrame, QSplitter, QScrollArea, QTabWidget
)
from PySide6.QtCore import Qt, QEasingCurve, QPropertyAnimation, QRect
from PySide6.QtGui import QFont


class AnimatedButton(QPushButton):
    """Custom animated button with hover effects"""
    def __init__(self, text="", parent=None):
        super().__init__(text, parent)
        self.setMinimumHeight(45)
        self.setCursor(Qt.PointingHandCursor)
        self._animation = QPropertyAnimation(self, b"geometry")
        self._animation.setDuration(100)
        self._animation.setEasingCurve(QEasingCurve.InOutQuad)
        
    def enterEvent(self, event):
        original_geo = self.geometry()
        self._animation.setStartValue(original_geo)
        self._animation.setEndValue(
            QRect(
                original_geo.x() - 2, 
                original_geo.y() - 1, 
                original_geo.width() + 4, 
                original_geo.height() + 2
            )
        )
        self._animation.start()
        super().enterEvent(event)
    
    def leaveEvent(self, event):
        original_geo = self.geometry()
        self._animation.setStartValue(original_geo)
        self._animation.setEndValue(
            QRect(
                original_geo.x() + 2, 
                original_geo.y() + 1, 
                original_geo.width() - 4, 
                original_geo.height() - 2
            )
        )
        self._animation.start()
        super().leaveEvent(event)


class MainAppScreen(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.setup_ui()
    
    def setup_ui(self):
        # Main layout
        main_layout = QHBoxLayout()
        
        # Create splitter for navigation and content
        splitter = QSplitter(Qt.Horizontal)
        
        # Navigation sidebar
        self.nav_frame = QFrame()
        self.nav_frame.setFixedWidth(220)
        self.nav_frame.setStyleSheet("""
            QFrame {
                background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, 
                                                 stop: 0 #2C2C2C, stop: 1 #1E1E1E);
                border-right: 1px solid #444444;
                padding: 15px;
            }
        """)
        
        nav_layout = QVBoxLayout(self.nav_frame)
        nav_layout.setAlignment(Qt.AlignTop)
        
        # App logo/title in sidebar
        logo_label = QLabel("QWERICH")
        logo_font = QFont()
        logo_font.setPointSize(16)
        logo_font.setBold(True)
        logo_label.setFont(logo_font)
        logo_label.setStyleSheet("color: #4CAF50; margin-bottom: 20px; text-align: center;")
        logo_label.setAlignment(Qt.AlignCenter)
        nav_layout.addWidget(logo_label)
        
        # Navigation buttons
        nav_buttons = [
            ("🏠 Главная", self.show_home),
            ("💬 Чат с Qwerich", self.show_chat),
            ("💻 Системная информация", self.show_system_info),
            ("📡 LAN Мессенджер", self.show_messenger),
            ("📖 Документация", self.show_docs),
            ("⚙️ Настройки", self.show_settings),
            ("🚪 Выйти", self.logout)
        ]
        
        for text, command in nav_buttons:
            btn = AnimatedButton(text)
            btn.setStyleSheet("""
                QPushButton {
                    background-color: #3C3F41;
                    border: 1px solid #555555;
                    border-radius: 8px;
                    padding: 12px;
                    color: #e7e7e7;
                    text-align: left;
                    font-size: 14px;
                    margin-bottom: 8px;
                }
                QPushButton:hover {
                    background-color: #4A4D4F;
                    border: 1px solid #4CAF50;
                }
                QPushButton:pressed {
                    background-color: #2D2D30;
                }
            """)
            btn.clicked.connect(command)
            nav_layout.addWidget(btn)
        
        # Add stretch to push buttons to the top
        nav_layout.addStretch()
        
        # User info in sidebar
        if self.parent.current_user:
            user_info = QLabel(f"👤 {self.parent.current_user['username']}")
            user_info.setStyleSheet("color: #AAAAAA; font-size: 12px; margin-top: 10px;")
            user_info.setAlignment(Qt.AlignCenter)
            nav_layout.addWidget(user_info)
        
        # Content area
        self.content_frame = QFrame()
        self.content_frame.setStyleSheet("""
            QFrame {
                background-color: #1E1E1E;
                border: none;
                padding: 15px;
            }
        """)
        
        self.content_layout = QVBoxLayout(self.content_frame)
        
        # Add frames to splitter
        splitter.addWidget(self.nav_frame)
        splitter.addWidget(self.content_frame)
        splitter.setSizes([220, 980])  # Initial sizes
        
        main_layout.addWidget(splitter)
        self.setLayout(main_layout)
        
        # Show initial content
        self.show_home()
    
    def show_home(self):
        # Clear existing content
        self.clear_content()
        
        # Home content
        home_widget = QWidget()
        home_layout = QVBoxLayout(home_widget)
        
        # Title
        title_label = QLabel("Добро пожаловать в Qwerich!")
        title_font = QFont()
        title_font.setPointSize(20)
        title_font.setBold(True)
        title_label.setFont(title_font)
        title_label.setStyleSheet("color: #e7e7e7;")
        home_layout.addWidget(title_label, alignment=Qt.AlignCenter)
        home_layout.addSpacing(20)
        
        # Welcome text
        welcome_text = (
            "Qwerich - ваш персональный помощник для управления системой и общения.\n\n"
            "Используйте навигационное меню слева для доступа к различным функциям:\n"
            "• Чат с Qwerich - для общения с ассистентом\n"
            "• Системная информация - для мониторинга состояния системы\n"
            "• LAN Мессенджер - для общения с другими пользователями в локальной сети\n"
            "• Документация - для получения справочной информации\n"
            "• Настройки - для настройки приложения"
        )
        
        text_label = QLabel(welcome_text)
        text_label.setWordWrap(True)
        text_label.setStyleSheet("color: #e7e7e7; font-size: 14px;")
        home_layout.addWidget(text_label)
        
        # Add to content layout
        scroll_area = QScrollArea()
        scroll_area.setWidget(home_widget)
        scroll_area.setWidgetResizable(True)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        scroll_area.setStyleSheet("""
            QScrollArea {
                border: none;
                background-color: transparent;
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
        
        self.content_layout.addWidget(scroll_area)
    
    def show_chat(self):
        self.clear_content()
        
        # Import and use the enhanced chat screen
        from .assistant_chat.chat_screen_pyside6 import ModernChatScreen
        chat_widget = ModernChatScreen()
        
        # Add to content layout
        scroll_area = QScrollArea()
        scroll_area.setWidget(chat_widget)
        scroll_area.setWidgetResizable(True)
        scroll_area.setStyleSheet("""
            QScrollArea {
                border: none;
                background-color: transparent;
            }
        """)
        
        self.content_layout.addWidget(scroll_area)
    
    def show_system_info(self):
        self.clear_content()
        
        # System info content
        sys_widget = QWidget()
        sys_layout = QVBoxLayout(sys_widget)
        
        title_label = QLabel("Системная информация")
        title_font = QFont()
        title_font.setPointSize(16)
        title_font.setBold(True)
        title_label.setFont(title_font)
        title_label.setStyleSheet("color: #e7e7e7;")
        sys_layout.addWidget(title_label)
        
        # Create a text widget to display system info
        info_text = QTextEdit()
        info_text.setReadOnly(True)
        info_text.setStyleSheet("""
            QTextEdit {
                background-color: #333333;
                border: 1px solid #555555;
                border-radius: 5px;
                color: #e7e7e7;
                font-family: monospace;
                font-size: 12px;
            }
        """)
        
        try:
            # Create system monitor and get info
            from modules.system_info.monitor import SystemMonitor
            monitor = SystemMonitor()
            all_info = monitor.get_all_info()
            
            # Display system information
            info_text.append("=== Системная информация ===\n")
            
            # CPU Info
            cpu_info = all_info['cpu']
            info_text.append(f"CPU Cores (Physical): {cpu_info['count_physical']}")
            info_text.append(f"CPU Cores (Logical): {cpu_info['count_logical']}")
            info_text.append(f"CPU Usage (%): {cpu_info['percentages']}")
            info_text.append(f"CPU Temperature: {cpu_info['temperature']}°C")
            info_text.append(f"CPU Frequency: {cpu_info['freq_current']:.2f} MHz\n")
            
            # Memory Info
            mem_info = all_info['memory']
            info_text.append("=== Память ===")
            info_text.append(f"Total Memory: {mem_info['total']} GB")
            info_text.append(f"Used Memory: {mem_info['used']} GB")
            info_text.append(f"Available Memory: {mem_info['available']} GB")
            info_text.append(f"Memory Usage: {mem_info['percent']}%\n")
            
            # Disk Info
            disk_info = all_info['disk']
            info_text.append("=== Диски ===")
            for disk in disk_info:
                info_text.append(f"Device: {disk['device']}")
                info_text.append(f"Mount Point: {disk['mountpoint']}")
                info_text.append(f"File System: {disk['file_system']}")
                info_text.append(f"Total: {disk['total']} GB")
                info_text.append(f"Used: {disk['used']} GB")
                info_text.append(f"Free: {disk['free']} GB")
                info_text.append(f"Usage: {disk['percent']}%")
                info_text.append("---")
            info_text.append("\n")
            
            # Network Info
            net_info = all_info['network']
            info_text.append("=== Сеть ===")
            info_text.append(f"Primary IP: {net_info['primary_ip']}\n")
            
        except ImportError:
            info_text.append("Модуль системной информации недоступен")
        except Exception as e:
            info_text.append(f"Ошибка при получении системной информации: {str(e)}")
        
        sys_layout.addWidget(info_text)
        
        # Add to content layout
        scroll_area = QScrollArea()
        scroll_area.setWidget(sys_widget)
        scroll_area.setWidgetResizable(True)
        scroll_area.setStyleSheet("""
            QScrollArea {
                border: none;
                background-color: transparent;
            }
        """)
        
        self.content_layout.addWidget(scroll_area)
    
    def show_messenger(self):
        self.clear_content()
        
        # Import and use the enhanced messenger screen
        from .messenger.messenger_screen_pyside6 import ModernMessengerScreen
        msg_widget = ModernMessengerScreen()
        
        # Add to content layout
        scroll_area = QScrollArea()
        scroll_area.setWidget(msg_widget)
        scroll_area.setWidgetResizable(True)
        scroll_area.setStyleSheet("""
            QScrollArea {
                border: none;
                background-color: transparent;
            }
        """)
        
        self.content_layout.addWidget(scroll_area)
    
    def show_docs(self):
        self.clear_content()
        
        # Import and use the enhanced documentation screen
        from .documentation.docs_screen_pyside6 import ModernDocumentationScreen
        docs_widget = ModernDocumentationScreen()
        
        # Add to content layout
        scroll_area = QScrollArea()
        scroll_area.setWidget(docs_widget)
        scroll_area.setWidgetResizable(True)
        scroll_area.setStyleSheet("""
            QScrollArea {
                border: none;
                background-color: transparent;
            }
        """)
        
        self.content_layout.addWidget(scroll_area)
    
    def show_settings(self):
        self.clear_content()
        
        # Import and use the enhanced settings screen
        from .settings.settings_screen_pyside6 import SettingsScreen
        settings_widget = SettingsScreen(parent=self.parent)
        
        # Add to content layout
        scroll_area = QScrollArea()
        scroll_area.setWidget(settings_widget)
        scroll_area.setWidgetResizable(True)
        scroll_area.setStyleSheet("""
            QScrollArea {
                border: none;
                background-color: transparent;
            }
        """)
        
        self.content_layout.addWidget(scroll_area)
    
    def logout(self):
        self.parent.show_login_screen()
    
    def clear_content(self):
        # Remove all widgets from content layout
        while self.content_layout.count():
            child = self.content_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()