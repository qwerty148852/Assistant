"""
Registration Screen for Qwerich Desktop Application (PySide6 Version)
"""

import re
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, 
    QPushButton, QCheckBox, QFormLayout, QFrame
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont


class RegistrationScreen(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.setup_ui()

    def setup_ui(self):
        # Main layout
        main_layout = QVBoxLayout()
        main_layout.setAlignment(Qt.AlignCenter)
        
        # Main frame
        main_frame = QFrame()
        main_frame.setObjectName("register_frame")
        main_frame.setStyleSheet("""
            QFrame#register_frame {
                background-color: #3c3f41;
                border-radius: 10px;
                border: 1px solid #555555;
                padding: 20px;
            }
        """)
        
        frame_layout = QVBoxLayout(main_frame)
        
        # Title
        title_label = QLabel("Создать аккаунт")
        title_font = QFont()
        title_font.setPointSize(20)
        title_font.setBold(True)
        title_label.setFont(title_font)
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("color: #e7e7e7;")
        frame_layout.addWidget(title_label)
        
        # Subtitle
        subtitle_label = QLabel("Заполните форму регистрации")
        subtitle_font = QFont()
        subtitle_font.setPointSize(14)
        subtitle_label.setFont(subtitle_font)
        subtitle_label.setAlignment(Qt.AlignCenter)
        subtitle_label.setStyleSheet("color: #cccccc;")
        frame_layout.addWidget(subtitle_label)
        frame_layout.addSpacing(30)
        
        # Form layout for inputs
        form_layout = QFormLayout()
        form_layout.setSpacing(10)
        form_layout.setFieldGrowthPolicy(QFormLayout.ExpandingFieldsGrow)
        
        # Username field
        self.username_entry = QLineEdit()
        self.username_entry.setPlaceholderText("Имя пользователя")
        self.username_entry.setMinimumWidth(300)
        self.username_entry.setStyleSheet("""
            QLineEdit {
                padding: 10px;
                font-size: 14px;
            }
        """)
        form_layout.addRow("Имя пользователя:", self.username_entry)
        
        # Email field
        self.email_entry = QLineEdit()
        self.email_entry.setPlaceholderText("Email")
        self.email_entry.setMinimumWidth(300)
        self.email_entry.setStyleSheet("""
            QLineEdit {
                padding: 10px;
                font-size: 14px;
            }
        """)
        form_layout.addRow("Email:", self.email_entry)
        
        # Password field
        self.password_entry = QLineEdit()
        self.password_entry.setPlaceholderText("Пароль")
        self.password_entry.setEchoMode(QLineEdit.Password)
        self.password_entry.setMinimumWidth(300)
        self.password_entry.setStyleSheet("""
            QLineEdit {
                padding: 10px;
                font-size: 14px;
            }
        """)
        form_layout.addRow("Пароль:", self.password_entry)
        
        # Confirm password field
        self.confirm_password_entry = QLineEdit()
        self.confirm_password_entry.setPlaceholderText("Повторите пароль")
        self.confirm_password_entry.setEchoMode(QLineEdit.Password)
        self.confirm_password_entry.setMinimumWidth(300)
        self.confirm_password_entry.setStyleSheet("""
            QLineEdit {
                padding: 10px;
                font-size: 14px;
            }
        """)
        form_layout.addRow("Повторите пароль:", self.confirm_password_entry)
        
        frame_layout.addLayout(form_layout)
        frame_layout.addSpacing(15)
        
        # Robot checkbox
        self.robot_checkbox = QCheckBox("Я не робот")
        self.robot_checkbox.setStyleSheet("""
            QCheckBox {
                color: #e7e7e7;
                font-size: 14px;
            }
            QCheckBox::indicator {
                width: 18px;
                height: 18px;
            }
            QCheckBox::indicator:checked {
                background-color: #0078d4;
                border: 1px solid #0078d4;
            }
        """)
        frame_layout.addWidget(self.robot_checkbox, alignment=Qt.AlignLeft)
        frame_layout.addSpacing(20)
        
        # Buttons layout
        buttons_layout = QVBoxLayout()
        
        # Register button
        self.register_button = QPushButton("Создать аккаунт")
        self.register_button.setObjectName("primary")
        self.register_button.clicked.connect(self.register)
        self.register_button.setMinimumHeight(40)
        buttons_layout.addWidget(self.register_button)
        
        # Back to login button
        self.back_button = QPushButton("Назад к входу")
        self.back_button.setObjectName("secondary")
        self.back_button.clicked.connect(self.go_to_login)
        self.back_button.setMinimumHeight(40)
        buttons_layout.addWidget(self.back_button)
        
        frame_layout.addLayout(buttons_layout)
        
        # Add main frame to main layout
        main_layout.addWidget(main_frame)
        self.setLayout(main_layout)

    def validate_email(self, email):
        """Validate email format"""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None

    def register(self):
        username = self.username_entry.text().strip()
        email = self.email_entry.text().strip()
        password = self.password_entry.text().strip()
        confirm_password = self.confirm_password_entry.text().strip()
        is_robot_checked = self.robot_checkbox.isChecked()

        # Validate inputs
        if not username:
            self.show_error("Введите имя пользователя")
            return

        if not email:
            self.show_error("Введите email")
            return

        if not self.validate_email(email):
            self.show_error("Некорректный формат email")
            return

        if not password:
            self.show_error("Введите пароль")
            return

        if len(password) < 6:
            self.show_error("Пароль должен содержать не менее 6 символов")
            return

        if password != confirm_password:
            self.show_error("Пароли не совпадают")
            return

        if not is_robot_checked:
            self.show_error("Подтвердите, что вы не робот")
            return

        # Register user
        app = self.parent
        success = app.db.register_user(username, email, password)

        if success:
            self.show_success("Регистрация прошла успешно!")
            self.go_to_login()
        else:
            self.show_error("Пользователь с таким email или именем уже существует")

    def go_to_login(self):
        self.parent.show_login_screen()

    def show_error(self, message):
        from PySide6.QtWidgets import QMessageBox
        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Warning)
        msg_box.setText(message)
        msg_box.setWindowTitle("Ошибка")
        msg_box.exec()

    def show_success(self, message):
        from PySide6.QtWidgets import QMessageBox
        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Information)
        msg_box.setText(message)
        msg_box.setWindowTitle("Успешно")
        msg_box.exec()