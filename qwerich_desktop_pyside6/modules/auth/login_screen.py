"""
Login Screen for Qwerich Desktop Application (PySide6 Version)
"""

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, 
    QPushButton, QCheckBox, QFormLayout, QFrame, QSizePolicy
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont


class LoginScreen(QWidget):
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
        main_frame.setObjectName("login_frame")
        main_frame.setStyleSheet("""
            QFrame#login_frame {
                background-color: #3c3f41;
                border-radius: 10px;
                border: 1px solid #555555;
                padding: 20px;
            }
        """)
        
        frame_layout = QVBoxLayout(main_frame)
        
        # Title
        title_label = QLabel("Добро пожаловать в Qwerich")
        title_font = QFont()
        title_font.setPointSize(20)
        title_font.setBold(True)
        title_label.setFont(title_font)
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("color: #e7e7e7;")
        frame_layout.addWidget(title_label)
        
        # Subtitle
        subtitle_label = QLabel("Войдите в свой аккаунт")
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
        
        # Username/Email field
        self.username_entry = QLineEdit()
        self.username_entry.setPlaceholderText("Email или имя пользователя")
        self.username_entry.setMinimumWidth(300)
        self.username_entry.setStyleSheet("""
            QLineEdit {
                padding: 10px;
                font-size: 14px;
            }
        """)
        form_layout.addRow("Email или имя пользователя:", self.username_entry)
        
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
        
        # Login button
        self.login_button = QPushButton("Войти")
        self.login_button.setObjectName("primary")
        self.login_button.clicked.connect(self.login)
        self.login_button.setMinimumHeight(40)
        buttons_layout.addWidget(self.login_button)
        
        # Register button
        self.register_button = QPushButton("Зарегистрироваться")
        self.register_button.setObjectName("secondary")
        self.register_button.clicked.connect(self.go_to_register)
        self.register_button.setMinimumHeight(40)
        buttons_layout.addWidget(self.register_button)
        
        frame_layout.addLayout(buttons_layout)
        
        # Add main frame to main layout
        main_layout.addWidget(main_frame)
        self.setLayout(main_layout)

    def login(self):
        username_or_email = self.username_entry.text().strip()
        password = self.password_entry.text().strip()
        is_robot_checked = self.robot_checkbox.isChecked()
        
        # Validate inputs
        if not username_or_email:
            self.show_error("Введите email или имя пользователя")
            return
        
        if not password:
            self.show_error("Введите пароль")
            return
        
        if not is_robot_checked:
            self.show_error("Подтвердите, что вы не робот")
            return
        
        # Authenticate user
        app = self.parent
        user = app.db.authenticate_user(username_or_email, password)
        
        if user:
            app.current_user = user
            # Navigate to main app screen after successful login
            app.show_main_app_screen()
        else:
            self.show_error("Неверные учетные данные")

    def go_to_register(self):
        self.parent.show_registration_screen()

    def show_error(self, message):
        from PySide6.QtWidgets import QMessageBox
        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Warning)
        msg_box.setText(message)
        msg_box.setWindowTitle("Ошибка")
        msg_box.exec()