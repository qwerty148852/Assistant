"""
Main Application Screen for Qwerich Desktop Application (PySide6 Version)
This is the main screen that appears after successful login
"""

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, 
    QTextEdit, QFrame, QSplitter, QScrollArea, QTabWidget
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont


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
        self.nav_frame.setFixedWidth(200)
        self.nav_frame.setStyleSheet("""
            QFrame {
                background-color: #3c3f41;
                border-right: 1px solid #555555;
                padding: 10px;
            }
        """)
        
        nav_layout = QVBoxLayout(self.nav_frame)
        nav_layout.setAlignment(Qt.AlignTop)
        
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
        
        for text, command in nav_buttons:
            btn = QPushButton(text)
            btn.setStyleSheet("""
                QPushButton {
                    background-color: #4a4d4f;
                    border: 1px solid #555555;
                    border-radius: 5px;
                    padding: 10px;
                    color: #e7e7e7;
                    text-align: left;
                    font-size: 14px;
                }
                QPushButton:hover {
                    background-color: #5a5d5f;
                }
                QPushButton:pressed {
                    background-color: #3a3d3f;
                }
            """)
            btn.clicked.connect(command)
            nav_layout.addWidget(btn)
        
        # Content area
        self.content_frame = QFrame()
        self.content_frame.setStyleSheet("""
            QFrame {
                background-color: #2d2d30;
                border: none;
                padding: 10px;
            }
        """)
        
        self.content_layout = QVBoxLayout(self.content_frame)
        
        # Add frames to splitter
        splitter.addWidget(self.nav_frame)
        splitter.addWidget(self.content_frame)
        splitter.setSizes([200, 980])  # Initial sizes
        
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
        
        # Placeholder for chat screen
        chat_widget = QWidget()
        chat_layout = QVBoxLayout(chat_widget)
        
        title_label = QLabel("Чат с Qwerich")
        title_font = QFont()
        title_font.setPointSize(16)
        title_font.setBold(True)
        title_label.setFont(title_font)
        title_label.setStyleSheet("color: #e7e7e7;")
        chat_layout.addWidget(title_label)
        
        # Chat interface placeholder
        chat_placeholder = QLabel("Интерфейс чата будет реализован здесь")
        chat_placeholder.setStyleSheet("color: #e7e7e7; font-size: 14px;")
        chat_layout.addWidget(chat_placeholder)
        
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
        
        # Messenger content placeholder
        msg_widget = QWidget()
        msg_layout = QVBoxLayout(msg_widget)
        
        title_label = QLabel("LAN Мессенджер")
        title_font = QFont()
        title_font.setPointSize(16)
        title_font.setBold(True)
        title_label.setFont(title_font)
        title_label.setStyleSheet("color: #e7e7e7;")
        msg_layout.addWidget(title_label)
        
        msg_text = QTextEdit()
        msg_text.setPlainText(
            "LAN мессенджер будет работать здесь.\n"
            "В реальном приложении вы сможете общаться с другими пользователями в локальной сети."
        )
        msg_text.setReadOnly(True)
        msg_text.setStyleSheet("""
            QTextEdit {
                background-color: #333333;
                border: 1px solid #555555;
                border-radius: 5px;
                color: #e7e7e7;
                font-size: 14px;
            }
        """)
        msg_layout.addWidget(msg_text)
        
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
        
        # Documentation content placeholder
        docs_widget = QWidget()
        docs_layout = QVBoxLayout(docs_widget)
        
        title_label = QLabel("Документация")
        title_font = QFont()
        title_font.setPointSize(16)
        title_font.setBold(True)
        title_label.setFont(title_font)
        title_label.setStyleSheet("color: #e7e7e7;")
        docs_layout.addWidget(title_label)
        
        docs_text = QTextEdit()
        docs_text.setPlainText("Интерфейс документации будет реализован здесь")
        docs_text.setReadOnly(True)
        docs_text.setStyleSheet("""
            QTextEdit {
                background-color: #333333;
                border: 1px solid #555555;
                border-radius: 5px;
                color: #e7e7e7;
                font-size: 14px;
            }
        """)
        docs_layout.addWidget(docs_text)
        
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
        
        # Settings content placeholder
        settings_widget = QWidget()
        settings_layout = QVBoxLayout(settings_widget)
        
        title_label = QLabel("Настройки")
        title_font = QFont()
        title_font.setPointSize(16)
        title_font.setBold(True)
        title_label.setFont(title_font)
        title_label.setStyleSheet("color: #e7e7e7;")
        settings_layout.addWidget(title_label)
        
        settings_text = QTextEdit()
        settings_text.setPlainText("Интерфейс настроек будет реализован здесь")
        settings_text.setReadOnly(True)
        settings_text.setStyleSheet("""
            QTextEdit {
                background-color: #333333;
                border: 1px solid #555555;
                border-radius: 5px;
                color: #e7e7e7;
                font-size: 14px;
            }
        """)
        settings_layout.addWidget(settings_text)
        
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