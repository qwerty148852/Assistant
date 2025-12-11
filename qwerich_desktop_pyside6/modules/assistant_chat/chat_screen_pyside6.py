"""
Enhanced Chat Screen for Qwerich Desktop Application (PySide6 Version)
Beautiful GUI with animations and gray-green theme
"""

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, 
    QTextEdit, QLineEdit, QFrame, QScrollArea, QScrollBar
)
from PySide6.QtCore import Qt, QSize, QEasingCurve, QPropertyAnimation, QRect, QPoint
from PySide6.QtGui import QFont, QColor, QPainter, QBrush, QPalette, QLinearGradient
from .chat_engine import ChatEngine


class AnimatedButton(QPushButton):
    """Custom animated button with hover effects"""
    def __init__(self, text="", parent=None):
        super().__init__(text, parent)
        self.setMinimumHeight(40)
        self.setCursor(Qt.PointingHandCursor)
        self._animation = QPropertyAnimation(self, b"geometry")
        self._animation.setDuration(150)
        self._animation.setEasingCurve(QEasingCurve.InOutQuad)
        
    def enterEvent(self, event):
        original_geo = self.geometry()
        self._animation.setStartValue(original_geo)
        self._animation.setEndValue(
            QRect(
                original_geo.x() - 2, 
                original_geo.y() - 2, 
                original_geo.width() + 4, 
                original_geo.height() + 4
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
                original_geo.y() + 2, 
                original_geo.width() - 4, 
                original_geo.height() - 4
            )
        )
        self._animation.start()
        super().leaveEvent(event)


class ChatMessageWidget(QLabel):
    """Custom widget for displaying chat messages with styling"""
    def __init__(self, text, is_user=False, parent=None):
        super().__init__(parent)
        self.setText(text)
        self.setWordWrap(True)
        self.setMargin(10)
        self.setMinimumHeight(40)
        
        # Style based on sender
        if is_user:
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


class CustomScrollBar(QScrollBar):
    """Custom styled scrollbar"""
    def __init__(self, orientation, parent=None):
        super().__init__(orientation, parent)
        self.setStyleSheet("""
            QScrollBar:vertical {
                background: #444444;
                width: 12px;
                border-radius: 6px;
            }
            QScrollBar::handle:vertical {
                background: #666666;
                border-radius: 6px;
                min-height: 20px;
            }
            QScrollBar::handle:vertical:hover {
                background: #777777;
            }
        """)


class ChatScreen(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.chat_engine = ChatEngine()
        self.setup_ui()
        
    def setup_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(15)
        
        # Title
        title_label = QLabel("Чат с Qwerich")
        title_font = QFont()
        title_font.setPointSize(18)
        title_font.setBold(True)
        title_label.setFont(title_font)
        title_label.setStyleSheet("color: #E0E0E0; margin-bottom: 10px;")
        title_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(title_label)
        
        # Chat display area with custom scroll
        self.chat_display = QTextEdit()
        self.chat_display.setReadOnly(True)
        self.chat_display.setMinimumHeight(400)
        self.chat_display.setStyleSheet("""
            QTextEdit {
                background-color: #333333;
                border: 2px solid #555555;
                border-radius: 10px;
                padding: 15px;
                color: #E0E0E0;
                font-size: 14px;
            }
        """)
        
        # Replace scrollbar with custom one
        self.scroll_bar = CustomScrollBar(Qt.Vertical)
        self.chat_display.setVerticalScrollBar(self.scroll_bar)
        
        main_layout.addWidget(self.chat_display)
        
        # Input area
        input_layout = QHBoxLayout()
        input_layout.setSpacing(10)
        
        self.chat_input = QLineEdit()
        self.chat_input.setPlaceholderText("Введите сообщение...")
        self.chat_input.setMinimumHeight(40)
        self.chat_input.setStyleSheet("""
            QLineEdit {
                background-color: #333333;
                border: 2px solid #555555;
                border-radius: 20px;
                padding: 0 15px;
                color: #E0E0E0;
                font-size: 14px;
            }
            QLineEdit:focus {
                border-color: #4CAF50;
            }
        """)
        self.chat_input.returnPressed.connect(self.send_message)
        input_layout.addWidget(self.chat_input)
        
        send_button = AnimatedButton("Отправить")
        send_button.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                border-radius: 20px;
                font-weight: bold;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QPushButton:pressed {
                background-color: #3d8b40;
            }
        """)
        send_button.clicked.connect(self.send_message)
        input_layout.addWidget(send_button, 1)
        
        main_layout.addLayout(input_layout)
        
        # Add initial message
        self.display_message("Qwerich: Привет! Я ваш виртуальный ассистент. Спросите меня что-нибудь!", is_user=False)
    
    def send_message(self):
        message = self.chat_input.text().strip()
        if message:
            self.display_message(f"Вы: {message}", is_user=True)
            self.chat_input.clear()
            
            # Simulate typing indicator
            typing_indicator = "Qwerich: Печатает..."
            self.chat_display.append(f'<div style="color: #AAAAAA; font-style: italic;">{typing_indicator}</div>')
            self.chat_display.ensureCursorVisible()
            
            # Get response from chat engine after a short delay to simulate thinking
            import threading
            import time
            
            def delayed_response():
                time.sleep(0.5)  # Simulate processing time
                response = self.chat_engine.get_response(message)
                
                # Remove typing indicator and add response
                cursor = self.chat_display.textCursor()
                cursor.movePosition(cursor.End)
                cursor.select(cursor.LineUnderCursor)
                cursor.removeSelectedText()
                
                self.display_message(f"Qwerich: {response}", is_user=False)
            
            thread = threading.Thread(target=delayed_response)
            thread.daemon = True
            thread.start()
    
    def display_message(self, message, is_user=False):
        # Format message differently based on sender
        if is_user:
            formatted_message = f'''
            <div style="margin: 5px 0; text-align: right;">
                <span style="background-color: #4CAF50; color: white; padding: 8px 15px; 
                             border-radius: 15px; display: inline-block; max-width: 80%;">
                    {message.split(": ", 1)[1] if ": " in message else message}
                </span>
            </div>
            '''
        else:
            formatted_message = f'''
            <div style="margin: 5px 0; text-align: left;">
                <span style="background-color: #555555; color: white; padding: 8px 15px; 
                             border-radius: 15px; display: inline-block; max-width: 80%;">
                    {message.split(": ", 1)[1] if ": " in message else message}
                </span>
            </div>
            '''
        
        self.chat_display.append(formatted_message)
        self.chat_display.ensureCursorVisible()


class ModernChatScreen(QWidget):
    """Modern chat screen with enhanced features"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
        
    def setup_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Create header
        header = QFrame()
        header.setFixedHeight(60)
        header.setStyleSheet("""
            QFrame {
                background-color: #2C2C2C;
                border-bottom: 1px solid #444444;
            }
        """)
        
        header_layout = QHBoxLayout(header)
        header_layout.setContentsMargins(20, 0, 20, 0)
        
        header_title = QLabel("Чат с Qwerich")
        header_title_font = QFont()
        header_title_font.setPointSize(16)
        header_title_font.setBold(True)
        header_title.setFont(header_title_font)
        header_title.setStyleSheet("color: #E0E0E0;")
        header_layout.addWidget(header_title)
        
        main_layout.addWidget(header)
        
        # Create central chat area
        chat_area = QFrame()
        chat_area.setStyleSheet("background-color: #252526;")
        
        chat_layout = QVBoxLayout(chat_area)
        chat_layout.setContentsMargins(20, 20, 20, 20)
        
        # Chat display with custom styling
        self.chat_display = QTextEdit()
        self.chat_display.setReadOnly(True)
        self.chat_display.setStyleSheet("""
            QTextEdit {
                background-color: #1E1E1E;
                border: 1px solid #3C3C3C;
                border-radius: 8px;
                padding: 15px;
                color: #CCCCCC;
                font-size: 14px;
            }
        """)
        
        chat_layout.addWidget(self.chat_display)
        
        # Input area
        input_frame = QFrame()
        input_frame.setStyleSheet("""
            QFrame {
                background-color: #2C2C2C;
                border-top: 1px solid #444444;
                padding: 10px;
            }
        """)
        
        input_layout = QHBoxLayout(input_frame)
        input_layout.setContentsMargins(10, 10, 10, 10)
        
        self.chat_input = QLineEdit()
        self.chat_input.setPlaceholderText("Введите сообщение...")
        self.chat_input.setStyleSheet("""
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
        self.chat_input.returnPressed.connect(self.send_message)
        input_layout.addWidget(self.chat_input)
        
        send_btn = QPushButton("➤")
        send_btn.setFixedSize(40, 40)
        send_btn.setStyleSheet("""
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
        send_btn.clicked.connect(self.send_message)
        input_layout.addWidget(send_btn)
        
        main_layout.addWidget(chat_area)
        main_layout.addWidget(input_frame)
        
        # Add initial message
        self.display_message("Qwerich: Привет! Я ваш виртуальный ассистент. Спросите меня что-нибудь!", is_user=False)
    
    def send_message(self):
        message = self.chat_input.text().strip()
        if message:
            self.display_message(f"Вы: {message}", is_user=True)
            self.chat_input.clear()
            
            # Simulate response
            import threading
            import time
            
            def get_response():
                time.sleep(1)  # Simulate thinking time
                response = f"Это ответ на ваше сообщение: '{message}'. Qwerich всегда готов помочь!"
                self.display_message(f"Qwerich: {response}", is_user=False)
            
            thread = threading.Thread(target=get_response)
            thread.daemon = True
            thread.start()
    
    def display_message(self, message, is_user=False):
        # Format message with different colors based on sender
        if is_user:
            formatted_msg = f'''
            <div style="margin: 8px 0; text-align: right;">
                <div style="display: inline-block; background-color: #4CAF50; 
                           color: white; padding: 10px 15px; border-radius: 18px; 
                           max-width: 80%; box-shadow: 0 2px 5px rgba(0,0,0,0.2);">
                    {message.split(": ", 1)[1] if ": " in message else message}
                </div>
            </div>
            '''
        else:
            formatted_msg = f'''
            <div style="margin: 8px 0; text-align: left;">
                <div style="display: inline-block; background-color: #3C3C3C; 
                           color: #E0E0E0; padding: 10px 15px; border-radius: 18px; 
                           max-width: 80%; box-shadow: 0 2px 5px rgba(0,0,0,0.2);">
                    {message.split(": ", 1)[1] if ": " in message else message}
                </div>
            </div>
            '''
        
        self.chat_display.append(formatted_msg)
        self.chat_display.ensureCursorVisible()