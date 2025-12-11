"""
Enhanced LAN Messenger Screen for Qwerich Desktop Application (PySide6 Version)
Beautiful GUI with animations and gray-green theme
"""

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, 
    QTextEdit, QLineEdit, QFrame, QScrollArea, QListWidget,
    QListWidgetItem, QSplitter
)
from PySide6.QtCore import Qt, QEasingCurve, QPropertyAnimation, QRect, QThread, Signal
from PySide6.QtGui import QFont, QColor, QPalette


class AnimatedButton(QPushButton):
    """Custom animated button with hover effects"""
    def __init__(self, text="", parent=None):
        super().__init__(text, parent)
        self.setMinimumHeight(40)
        self.setCursor(Qt.PointingHandCursor)
        self._animation = QPropertyAnimation(self, b"geometry")
        self._animation.setDuration(100)
        self._animation.setEasingCurve(QEasingCurve.InOutQuad)
        
    def enterEvent(self, event):
        original_geo = self.geometry()
        self._animation.setStartValue(original_geo)
        self._animation.setEndValue(
            QRect(
                original_geo.x() - 1, 
                original_geo.y() - 1, 
                original_geo.width() + 2, 
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
                original_geo.x() + 1, 
                original_geo.y() + 1, 
                original_geo.width() - 2, 
                original_geo.height() - 2
            )
        )
        self._animation.start()
        super().leaveEvent(event)


class ChatMessageWidget(QLabel):
    """Custom widget for displaying chat messages"""
    def __init__(self, sender, message, is_user=False, parent=None):
        super().__init__(parent)
        self.sender = sender
        self.message = message
        self.is_user = is_user
        self.setup_ui()
    
    def setup_ui(self):
        full_text = f"{self.sender}: {self.message}"
        self.setText(full_text)
        self.setWordWrap(True)
        self.setMargin(10)
        self.setMinimumHeight(40)
        
        if self.is_user:
            self.setStyleSheet("""
                QLabel {
                    background-color: #4CAF50;
                    color: white;
                    border-radius: 15px;
                    padding: 10px;
                    font-size: 14px;
                }
            """)
        else:
            self.setStyleSheet("""
                QLabel {
                    background-color: #555555;
                    color: white;
                    border-radius: 15px;
                    padding: 10px;
                    font-size: 14px;
                }
            """)


class MessengerScreen(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.current_user = "User"  # This would come from parent app
        self.setup_ui()
    
    def setup_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(15)
        
        # Title
        title_label = QLabel("LAN Мессенджер")
        title_font = QFont()
        title_font.setPointSize(18)
        title_font.setBold(True)
        title_label.setFont(title_font)
        title_label.setStyleSheet("color: #E0E0E0; margin-bottom: 10px;")
        title_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(title_label)
        
        # Create splitter for sidebar and chat area
        splitter = QSplitter(Qt.Horizontal)
        
        # Contacts sidebar
        contacts_frame = QFrame()
        contacts_frame.setFixedWidth(250)
        contacts_frame.setStyleSheet("""
            QFrame {
                background-color: #2D2D30;
                border: 1px solid #555555;
                border-radius: 8px;
            }
        """)
        
        contacts_layout = QVBoxLayout(contacts_frame)
        contacts_layout.setContentsMargins(10, 10, 10, 10)
        
        contacts_title = QLabel("Контакты")
        contacts_title.setStyleSheet("color: #E0E0E0; font-weight: bold; font-size: 16px;")
        contacts_layout.addWidget(contacts_title)
        
        self.contacts_list = QListWidget()
        self.contacts_list.setStyleSheet("""
            QListWidget {
                background-color: #3C3C3C;
                border: 1px solid #555555;
                border-radius: 6px;
                color: #E0E0E0;
            }
            QListWidget::item {
                padding: 10px;
                border-bottom: 1px solid #555555;
            }
            QListWidget::item:selected {
                background-color: #4CAF50;
            }
        """)
        
        # Add some sample contacts
        sample_contacts = [
            "Алексей Петров", "Мария Смирнова", "Иван Иванов", 
            "Елена Козлова", "Дмитрий Волков", "Ольга Морозова"
        ]
        
        for contact in sample_contacts:
            item = QListWidgetItem(contact)
            item.setFont(QFont("Arial", 12))
            self.contacts_list.addItem(item)
        
        contacts_layout.addWidget(self.contacts_list)
        
        splitter.addWidget(contacts_frame)
        
        # Chat area
        chat_frame = QFrame()
        chat_frame.setStyleSheet("""
            QFrame {
                background-color: #2D2D30;
                border: 1px solid #555555;
                border-radius: 8px;
            }
        """)
        
        chat_layout = QVBoxLayout(chat_frame)
        chat_layout.setContentsMargins(15, 15, 15, 15)
        
        # Chat header
        chat_header = QFrame()
        chat_header.setFixedHeight(50)
        chat_header.setStyleSheet("""
            QFrame {
                background-color: #3C3C3C;
                border-radius: 6px;
                padding: 10px;
            }
        """)
        
        header_layout = QHBoxLayout(chat_header)
        header_layout.setContentsMargins(10, 0, 10, 0)
        
        self.current_chat_label = QLabel("Выберите контакт для начала чата")
        self.current_chat_label.setStyleSheet("color: #E0E0E0; font-weight: bold; font-size: 14px;")
        header_layout.addWidget(self.current_chat_label)
        
        chat_layout.addWidget(chat_header)
        
        # Messages display area
        self.messages_area = QTextEdit()
        self.messages_area.setReadOnly(True)
        self.messages_area.setMinimumHeight(400)
        self.messages_area.setStyleSheet("""
            QTextEdit {
                background-color: #1E1E1E;
                border: 1px solid #555555;
                border-radius: 6px;
                padding: 15px;
                color: #E0E0E0;
                font-size: 14px;
            }
        """)
        
        chat_layout.addWidget(self.messages_area)
        
        # Message input area
        input_frame = QFrame()
        input_frame.setStyleSheet("""
            QFrame {
                background-color: #3C3C3C;
                border-radius: 6px;
                padding: 5px;
            }
        """)
        
        input_layout = QHBoxLayout(input_frame)
        input_layout.setContentsMargins(10, 10, 10, 10)
        
        self.message_input = QLineEdit()
        self.message_input.setPlaceholderText("Введите сообщение...")
        self.message_input.setStyleSheet("""
            QLineEdit {
                background-color: #2D2D30;
                border: 1px solid #555555;
                border-radius: 20px;
                padding: 8px 15px;
                color: #E0E0E0;
                font-size: 14px;
            }
            QLineEdit:focus {
                border: 2px solid #4CAF50;
            }
        """)
        self.message_input.returnPressed.connect(self.send_message)
        input_layout.addWidget(self.message_input)
        
        send_button = AnimatedButton("➤")
        send_button.setFixedSize(40, 40)
        send_button.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                border-radius: 20px;
                font-weight: bold;
                font-size: 16px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QPushButton:pressed {
                background-color: #3d8b40;
            }
        """)
        send_button.clicked.connect(self.send_message)
        input_layout.addWidget(send_button)
        
        chat_layout.addWidget(input_frame)
        
        splitter.addWidget(chat_frame)
        splitter.setSizes([250, 730])
        
        main_layout.addWidget(splitter)
        
        # Connect contact selection to chat
        self.contacts_list.itemClicked.connect(self.select_contact)
        
        # Add welcome message
        self.add_system_message("Добро пожаловать в LAN Мессенджер! Выберите контакт для начала общения.")
    
    def select_contact(self, item):
        contact_name = item.text()
        self.current_chat_label.setText(f"Чат с: {contact_name}")
        self.add_system_message(f"Начат чат с {contact_name}")
    
    def send_message(self):
        message = self.message_input.text().strip()
        if message and self.current_chat_label.text() != "Выберите контакт для начала чата":
            # Add user message
            current_contact = self.current_chat_label.text().replace("Чат с: ", "")
            self.add_message(current_contact, message, is_user=True)
            self.message_input.clear()
            
            # Simulate response after a delay
            import threading
            import time
            
            def simulate_response():
                time.sleep(1.5)  # Simulate typing time
                responses = [
                    "Ок, понял.",
                    "Спасибо за сообщение!",
                    "Как дела?",
                    "Отличный вопрос!",
                    "Позже отвечу подробнее.",
                    "Интересная мысль!",
                    "Согласен с вами.",
                    "Могу ли я чем-то помочь?"
                ]
                import random
                response = random.choice(responses)
                self.add_message(current_contact, response, is_user=False)
            
            thread = threading.Thread(target=simulate_response)
            thread.daemon = True
            thread.start()
    
    def add_message(self, sender, message, is_user=False):
        # Format message differently based on sender
        if is_user:
            formatted_msg = f'''
            <div style="margin: 8px 0; text-align: right;">
                <div style="display: inline-block; background-color: #4CAF50; 
                           color: white; padding: 10px 15px; border-radius: 18px; 
                           max-width: 80%; box-shadow: 0 2px 5px rgba(0,0,0,0.2);">
                    <div style="font-weight: bold; font-size: 12px; margin-bottom: 3px; color: #d0f0d0;">Вы</div>
                    {message}
                </div>
            </div>
            '''
        else:
            formatted_msg = f'''
            <div style="margin: 8px 0; text-align: left;">
                <div style="display: inline-block; background-color: #3C3C3C; 
                           color: #E0E0E0; padding: 10px 15px; border-radius: 18px; 
                           max-width: 80%; box-shadow: 0 2px 5px rgba(0,0,0,0.2);">
                    <div style="font-weight: bold; font-size: 12px; margin-bottom: 3px; color: #a0a0a0;">{sender}</div>
                    {message}
                </div>
            </div>
            '''
        
        self.messages_area.append(formatted_msg)
        self.messages_area.ensureCursorVisible()
    
    def add_system_message(self, message):
        formatted_msg = f'''
        <div style="margin: 8px 0; text-align: center;">
            <div style="display: inline-block; background-color: #555555; 
                       color: #AAAAAA; padding: 8px 15px; border-radius: 18px; 
                       font-style: italic; font-size: 12px;">
                {message}
            </div>
        </div>
        '''
        self.messages_area.append(formatted_msg)
        self.messages_area.ensureCursorVisible()


class ModernMessengerScreen(QWidget):
    """Modern messenger screen with enhanced features"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
    
    def setup_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Create header
        header = QFrame()
        header.setFixedHeight(70)
        header.setStyleSheet("""
            QFrame {
                background-color: #2C2C2C;
                border-bottom: 1px solid #444444;
            }
        """)
        
        header_layout = QHBoxLayout(header)
        header_layout.setContentsMargins(20, 0, 20, 0)
        
        header_title = QLabel("LAN Мессенджер")
        header_title_font = QFont()
        header_title_font.setPointSize(18)
        header_title_font.setBold(True)
        header_title.setFont(header_title_font)
        header_title.setStyleSheet("color: #E0E0E0;")
        header_layout.addWidget(header_title)
        
        # Status indicator
        status_frame = QFrame()
        status_frame.setFixedSize(20, 20)
        status_frame.setStyleSheet("""
            QFrame {
                background-color: #4CAF50;
                border-radius: 10px;
            }
        """)
        header_layout.addWidget(status_frame)
        
        status_label = QLabel("В сети")
        status_label.setStyleSheet("color: #E0E0E0;")
        header_layout.addWidget(status_label)
        
        header_layout.addStretch()
        
        main_layout.addWidget(header)
        
        # Main content area
        content_area = QSplitter(Qt.Horizontal)
        content_area.setStyleSheet("""
            QSplitter::handle {
                background-color: #444444;
                width: 2px;
            }
        """)
        
        # Contacts sidebar
        contacts_frame = QFrame()
        contacts_frame.setStyleSheet("""
            QFrame {
                background-color: #252526;
                border-right: 1px solid #444444;
            }
        """)
        
        contacts_layout = QVBoxLayout(contacts_frame)
        contacts_layout.setContentsMargins(0, 0, 0, 0)
        
        # Search bar
        search_frame = QFrame()
        search_frame.setStyleSheet("""
            QFrame {
                background-color: #2D2D30;
                padding: 10px;
            }
        """)
        
        search_layout = QHBoxLayout(search_frame)
        search_layout.setContentsMargins(10, 5, 10, 5)
        
        search_input = QLineEdit()
        search_input.setPlaceholderText("Поиск контактов...")
        search_input.setStyleSheet("""
            QLineEdit {
                background-color: #3C3C3C;
                border: 1px solid #555555;
                border-radius: 15px;
                padding: 8px 15px;
                color: #E0E0E0;
            }
            QLineEdit:focus {
                border: 2px solid #4CAF50;
            }
        """)
        search_layout.addWidget(search_input)
        
        contacts_layout.addWidget(search_frame)
        
        # Contacts list
        self.contacts_list = QListWidget()
        self.contacts_list.setStyleSheet("""
            QListWidget {
                background-color: #252526;
                border: none;
                color: #E0E0E0;
            }
            QListWidget::item {
                padding: 15px 10px;
                border-bottom: 1px solid #3C3C3C;
            }
            QListWidget::item:selected {
                background-color: #3C3C3C;
            }
        """)
        
        # Add sample contacts with status
        sample_contacts = [
            ("Алексей Петров", "online"),
            ("Мария Смирнова", "away"),
            ("Иван Иванов", "online"),
            ("Елена Козлова", "offline"),
            ("Дмитрий Волков", "online"),
            ("Ольга Морозова", "away"),
            ("Сергей Волков", "online"),
            ("Анна Соколова", "online")
        ]
        
        for contact, status in sample_contacts:
            item = QListWidgetItem(contact)
            item.setFont(QFont("Arial", 12))
            
            # Add status indicator
            widget = QFrame()
            widget_layout = QHBoxLayout(widget)
            widget_layout.setContentsMargins(15, 0, 15, 0)
            
            status_indicator = QFrame()
            status_indicator.setFixedSize(12, 12)
            if status == "online":
                status_indicator.setStyleSheet("QFrame { background-color: #4CAF50; border-radius: 6px; }")
            elif status == "away":
                status_indicator.setStyleSheet("QFrame { background-color: #FFC107; border-radius: 6px; }")
            else:
                status_indicator.setStyleSheet("QFrame { background-color: #757575; border-radius: 6px; }")
            
            name_label = QLabel(contact)
            name_label.setStyleSheet("color: #E0E0E0; font-size: 14px;")
            
            widget_layout.addWidget(status_indicator)
            widget_layout.addWidget(name_label)
            widget_layout.addStretch()
            
            self.contacts_list.addItem(item)
            self.contacts_list.setItemWidget(item, widget)
        
        contacts_layout.addWidget(self.contacts_list)
        
        content_area.addWidget(contacts_frame)
        
        # Chat area
        chat_frame = QFrame()
        chat_frame.setStyleSheet("""
            QFrame {
                background-color: #1E1E1E;
            }
        """)
        
        chat_layout = QVBoxLayout(chat_frame)
        chat_layout.setContentsMargins(0, 0, 0, 0)
        
        # Chat header (initially hidden until contact is selected)
        self.chat_header = QFrame()
        self.chat_header.setFixedHeight(60)
        self.chat_header.setStyleSheet("""
            QFrame {
                background-color: #2D2D30;
                border-bottom: 1px solid #444444;
                padding: 0 20px;
            }
        """)
        self.chat_header.hide()
        
        chat_header_layout = QHBoxLayout(self.chat_header)
        chat_header_layout.setContentsMargins(0, 0, 0, 0)
        
        self.chat_contact_label = QLabel("")
        self.chat_contact_label.setStyleSheet("color: #E0E0E0; font-size: 16px; font-weight: bold;")
        chat_header_layout.addWidget(self.chat_contact_label)
        
        chat_header_layout.addStretch()
        
        # Status indicator for contact
        self.contact_status = QFrame()
        self.contact_status.setFixedSize(12, 12)
        self.contact_status.setStyleSheet("QFrame { background-color: #4CAF50; border-radius: 6px; }")
        chat_header_layout.addWidget(self.contact_status)
        
        chat_layout.addWidget(self.chat_header)
        
        # Messages area
        self.messages_area = QTextEdit()
        self.messages_area.setReadOnly(True)
        self.messages_area.setStyleSheet("""
            QTextEdit {
                background-color: #1E1E1E;
                border: none;
                color: #CCCCCC;
                font-size: 14px;
                padding: 20px;
            }
        """)
        
        chat_layout.addWidget(self.messages_area)
        
        # Input area
        input_frame = QFrame()
        input_frame.setFixedHeight(70)
        input_frame.setStyleSheet("""
            QFrame {
                background-color: #2D2D30;
                border-top: 1px solid #444444;
                padding: 0 20px;
            }
        """)
        
        input_layout = QHBoxLayout(input_frame)
        input_layout.setContentsMargins(0, 15, 0, 15)
        
        self.message_input = QLineEdit()
        self.message_input.setPlaceholderText("Введите сообщение...")
        self.message_input.setStyleSheet("""
            QLineEdit {
                background-color: #3C3C3C;
                border: 1px solid #555555;
                border-radius: 20px;
                padding: 10px 20px;
                color: #E0E0E0;
                font-size: 14px;
            }
            QLineEdit:focus {
                border: 2px solid #4CAF50;
            }
        """)
        self.message_input.returnPressed.connect(self.send_message)
        input_layout.addWidget(self.message_input)
        
        send_btn = QPushButton("➤")
        send_btn.setFixedSize(45, 45)
        send_btn.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                border-radius: 22px;
                font-weight: bold;
                font-size: 18px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QPushButton:pressed {
                background-color: #3d8b40;
            }
        """)
        send_btn.clicked.connect(self.send_message)
        input_layout.addWidget(send_btn)
        
        chat_layout.addWidget(input_frame)
        
        content_area.addWidget(chat_frame)
        content_area.setSizes([300, 700])
        
        main_layout.addWidget(content_area)
        
        # Connect contact selection
        self.contacts_list.itemClicked.connect(self.select_contact)
        
        # Add welcome message
        self.add_system_message("Добро пожаловать в современный LAN Мессенджер!")
    
    def select_contact(self, item):
        contact_name = item.text()
        self.chat_contact_label.setText(contact_name)
        self.chat_header.show()
        self.add_system_message(f"Начат чат с {contact_name}")
    
    def send_message(self):
        message = self.message_input.text().strip()
        if message and self.chat_header.isVisible():
            contact_name = self.chat_contact_label.text()
            self.add_message(contact_name, message, is_user=True)
            self.message_input.clear()
            
            # Simulate response
            import threading
            import time
            
            def simulate_response():
                time.sleep(1)  # Simulate typing time
                responses = [
                    "Принято!",
                    "Спасибо, я получил ваше сообщение.",
                    "Как дела?",
                    "Хороший вопрос!",
                    "Подумаю и отвечу позже.",
                    "Интересная мысль!",
                    "Согласен.",
                    "Есть чем поделиться?"
                ]
                import random
                response = random.choice(responses)
                self.add_message(contact_name, response, is_user=False)
            
            thread = threading.Thread(target=simulate_response)
            thread.daemon = True
            thread.start()
    
    def add_message(self, sender, message, is_user=False):
        if is_user:
            formatted_msg = f'''
            <div style="margin: 10px 0; text-align: right;">
                <div style="display: inline-block; background-color: #4CAF50; 
                           color: white; padding: 12px 16px; border-radius: 18px; 
                           max-width: 75%; box-shadow: 0 2px 5px rgba(0,0,0,0.2);">
                    <div style="font-weight: bold; font-size: 12px; margin-bottom: 4px; color: #d0f0d0;">Вы</div>
                    {message}
                </div>
            </div>
            '''
        else:
            formatted_msg = f'''
            <div style="margin: 10px 0; text-align: left;">
                <div style="display: inline-block; background-color: #3C3C3C; 
                           color: #E0E0E0; padding: 12px 16px; border-radius: 18px; 
                           max-width: 75%; box-shadow: 0 2px 5px rgba(0,0,0,0.2);">
                    <div style="font-weight: bold; font-size: 12px; margin-bottom: 4px; color: #a0a0a0;">{sender}</div>
                    {message}
                </div>
            </div>
            '''
        
        self.messages_area.append(formatted_msg)
        self.messages_area.ensureCursorVisible()
    
    def add_system_message(self, message):
        formatted_msg = f'''
        <div style="margin: 15px 0; text-align: center;">
            <div style="display: inline-block; background-color: #3C3C3C; 
                       color: #AAAAAA; padding: 8px 16px; border-radius: 18px; 
                       font-style: italic; font-size: 13px; box-shadow: 0 2px 5px rgba(0,0,0,0.2);">
                {message}
            </div>
        </div>
        '''
        self.messages_area.append(formatted_msg)
        self.messages_area.ensureCursorVisible()