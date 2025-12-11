"""
Enhanced Settings Screen for Qwerich Desktop Application (PySide6 Version)
Beautiful GUI with animations and gray-green theme
"""

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, 
    QTextEdit, QLineEdit, QFrame, QScrollArea, QTabWidget, 
    QCheckBox, QComboBox, QSlider, QGroupBox
)
from PySide6.QtCore import Qt, QEasingCurve, QPropertyAnimation, QRect, QParallelAnimationGroup
from PySide6.QtGui import QFont, QPalette, QColor


class AnimatedButton(QPushButton):
    """Custom animated button with hover effects"""
    def __init__(self, text="", parent=None):
        super().__init__(text, parent)
        self.setMinimumHeight(40)
        self.setCursor(Qt.PointingHandCursor)
        
        # Set up animations
        self._anim_group = QParallelAnimationGroup(self)
        self._x_anim = QPropertyAnimation(self, b"geometry")
        self._y_anim = QPropertyAnimation(self, b"geometry")
        
        self._x_anim.setDuration(100)
        self._x_anim.setEasingCurve(QEasingCurve.InOutQuad)
        self._y_anim.setDuration(100)
        self._y_anim.setEasingCurve(QEasingCurve.InOutQuad)
        
        self._anim_group.addAnimation(self._x_anim)
        self._anim_group.addAnimation(self._y_anim)
    
    def enterEvent(self, event):
        original_geo = self.geometry()
        self._x_anim.setStartValue(original_geo)
        self._x_anim.setEndValue(
            QRect(
                original_geo.x() - 1, 
                original_geo.y(), 
                original_geo.width() + 2, 
                original_geo.height()
            )
        )
        self._y_anim.setStartValue(original_geo)
        self._y_anim.setEndValue(
            QRect(
                original_geo.x(), 
                original_geo.y() - 1, 
                original_geo.width(), 
                original_geo.height() + 2
            )
        )
        self._anim_group.start()
        super().enterEvent(event)
    
    def leaveEvent(self, event):
        original_geo = self.geometry()
        self._x_anim.setStartValue(original_geo)
        self._x_anim.setEndValue(
            QRect(
                original_geo.x() + 1, 
                original_geo.y(), 
                original_geo.width() - 2, 
                original_geo.height()
            )
        )
        self._y_anim.setStartValue(original_geo)
        self._y_anim.setEndValue(
            QRect(
                original_geo.x(), 
                original_geo.y() + 1, 
                original_geo.width(), 
                original_geo.height() - 2
            )
        )
        self._anim_group.start()
        super().leaveEvent(event)


class SettingsScreen(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent_app = parent
        self.setup_ui()
    
    def setup_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(15)
        
        # Title
        title_label = QLabel("Настройки")
        title_font = QFont()
        title_font.setPointSize(18)
        title_font.setBold(True)
        title_label.setFont(title_font)
        title_label.setStyleSheet("color: #E0E0E0; margin-bottom: 10px;")
        title_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(title_label)
        
        # Create tab widget
        self.tab_widget = QTabWidget()
        self.tab_widget.setStyleSheet("""
            QTabWidget::pane {
                border: none;
                background-color: #2D2D30;
                border-radius: 8px;
            }
            QTabBar::tab {
                background-color: #3C3F41;
                color: #E0E0E0;
                padding: 12px 20px;
                margin: 2px;
                border-top-left-radius: 6px;
                border-top-right-radius: 6px;
            }
            QTabBar::tab:selected {
                background-color: #4CAF50;
                color: white;
            }
            QTabBar::tab:hover:!selected {
                background-color: #4A4D4F;
            }
        """)
        
        # Add tabs
        self.create_appearance_tab()
        self.create_account_tab()
        self.create_privacy_tab()
        self.create_messenger_tab()
        
        main_layout.addWidget(self.tab_widget)
    
    def create_appearance_tab(self):
        appearance_widget = QWidget()
        appearance_layout = QVBoxLayout(appearance_widget)
        appearance_layout.setContentsMargins(20, 20, 20, 20)
        
        # Theme selection
        theme_group = QGroupBox("Тема оформления")
        theme_group.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                color: #E0E0E0;
                border: 1px solid #555555;
                border-radius: 8px;
                margin-top: 1ex;
                padding-top: 10px;
            }
            QGroupBox:title {
                subcontrol-origin: margin;
                subcontrol-position: top center;
                padding: 0 5px;
            }
        """)
        theme_layout = QVBoxLayout(theme_group)
        
        theme_label = QLabel("Выберите тему:")
        theme_label.setStyleSheet("color: #E0E0E0; font-weight: normal;")
        theme_layout.addWidget(theme_label)
        
        theme_options = [
            "Серо-зеленая (по умолчанию)",
            "Темная классическая", 
            "Светлая",
            "Глубокий лес",
            "Океанская синева"
        ]
        self.theme_combo = QComboBox()
        self.theme_combo.addItems(theme_options)
        self.theme_combo.setStyleSheet("""
            QComboBox {
                background-color: #3C3C3C;
                border: 1px solid #555555;
                border-radius: 6px;
                padding: 8px;
                color: #E0E0E0;
            }
            QComboBox::drop-down {
                subcontrol-origin: padding;
                subcontrol-position: top right;
                width: 25px;
                border-left: 1px solid #555555;
                border-top-right-radius: 6px;
                border-bottom-right-radius: 6px;
            }
            QComboBox::down-arrow {
                image: url(noimg);
                width: 10px;
                height: 10px;
            }
        """)
        theme_layout.addWidget(self.theme_combo)
        
        appearance_layout.addWidget(theme_group)
        
        # Animation toggle
        anim_group = QGroupBox("Анимации")
        anim_group.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                color: #E0E0E0;
                border: 1px solid #555555;
                border-radius: 8px;
                margin-top: 1ex;
                padding-top: 10px;
            }
            QGroupBox:title {
                subcontrol-origin: margin;
                subcontrol-position: top center;
                padding: 0 5px;
            }
        """)
        anim_layout = QVBoxLayout(anim_group)
        
        self.animation_checkbox = QCheckBox("Включить плавные анимации интерфейса")
        self.animation_checkbox.setChecked(True)
        self.animation_checkbox.setStyleSheet("""
            QCheckBox {
                color: #E0E0E0;
                spacing: 10px;
            }
            QCheckBox::indicator {
                width: 18px;
                height: 18px;
            }
            QCheckBox::indicator:unchecked {
                border: 2px solid #555555;
                background-color: #2D2D30;
                border-radius: 3px;
            }
            QCheckBox::indicator:checked {
                border: 2px solid #4CAF50;
                background-color: #4CAF50;
                border-radius: 3px;
            }
        """)
        anim_layout.addWidget(self.animation_checkbox)
        
        appearance_layout.addWidget(anim_group)
        
        # Font size selection
        font_group = QGroupBox("Размер шрифта")
        font_group.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                color: #E0E0E0;
                border: 1px solid #555555;
                border-radius: 8px;
                margin-top: 1ex;
                padding-top: 10px;
            }
            QGroupBox:title {
                subcontrol-origin: margin;
                subcontrol-position: top center;
                padding: 0 5px;
            }
        """)
        font_layout = QVBoxLayout(font_group)
        
        font_label = QLabel("Размер шрифта интерфейса:")
        font_label.setStyleSheet("color: #E0E0E0; font-weight: normal;")
        font_layout.addWidget(font_label)
        
        font_options = ["Маленький", "Нормальный", "Большой", "Очень большой"]
        self.font_combo = QComboBox()
        self.font_combo.addItems(font_options)
        self.font_combo.setStyleSheet("""
            QComboBox {
                background-color: #3C3C3C;
                border: 1px solid #555555;
                border-radius: 6px;
                padding: 8px;
                color: #E0E0E0;
            }
            QComboBox::drop-down {
                subcontrol-origin: padding;
                subcontrol-position: top right;
                width: 25px;
                border-left: 1px solid #555555;
                border-top-right-radius: 6px;
                border-bottom-right-radius: 6px;
            }
        """)
        font_layout.addWidget(self.font_combo)
        
        appearance_layout.addWidget(font_group)
        
        # Add stretch to push content up
        appearance_layout.addStretch()
        
        # Add save button
        save_btn = AnimatedButton("Сохранить настройки")
        save_btn.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                border-radius: 6px;
                font-weight: bold;
                font-size: 14px;
                padding: 12px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QPushButton:pressed {
                background-color: #3d8b40;
            }
        """)
        save_btn.clicked.connect(self.save_appearance_settings)
        appearance_layout.addWidget(save_btn)
        
        self.tab_widget.addTab(appearance_widget, "Внешний вид")
    
    def create_account_tab(self):
        account_widget = QWidget()
        account_layout = QVBoxLayout(account_widget)
        account_layout.setContentsMargins(20, 20, 20, 20)
        
        # Current user info
        if hasattr(self.parent_app, 'current_user') and self.parent_app.current_user:
            user_info = f"Текущий пользователь: {self.parent_app.current_user['username']}"
            user_label = QLabel(user_info)
            user_label.setStyleSheet("color: #E0E0E0; font-weight: bold; font-size: 16px;")
            user_label.setAlignment(Qt.AlignCenter)
            account_layout.addWidget(user_label)
        
        # Username field
        username_group = QGroupBox("Имя пользователя")
        username_group.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                color: #E0E0E0;
                border: 1px solid #555555;
                border-radius: 8px;
                margin-top: 1ex;
                padding-top: 10px;
            }
            QGroupBox:title {
                subcontrol-origin: margin;
                subcontrol-position: top center;
                padding: 0 5px;
            }
        """)
        username_layout = QVBoxLayout(username_group)
        
        self.username_field = QLineEdit()
        if hasattr(self.parent_app, 'current_user') and self.parent_app.current_user:
            self.username_field.setText(self.parent_app.current_user['username'])
        self.username_field.setStyleSheet("""
            QLineEdit {
                background-color: #3C3C3C;
                border: 1px solid #555555;
                border-radius: 6px;
                padding: 8px;
                color: #E0E0E0;
            }
            QLineEdit:focus {
                border: 2px solid #4CAF50;
            }
        """)
        username_layout.addWidget(self.username_field)
        
        account_layout.addWidget(username_group)
        
        # Email field
        email_group = QGroupBox("Email")
        email_group.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                color: #E0E0E0;
                border: 1px solid #555555;
                border-radius: 8px;
                margin-top: 1ex;
                padding-top: 10px;
            }
            QGroupBox:title {
                subcontrol-origin: margin;
                subcontrol-position: top center;
                padding: 0 5px;
            }
        """)
        email_layout = QVBoxLayout(email_group)
        
        self.email_field = QLineEdit()
        if hasattr(self.parent_app, 'current_user') and self.parent_app.current_user:
            self.email_field.setText(self.parent_app.current_user['email'])
        self.email_field.setStyleSheet("""
            QLineEdit {
                background-color: #3C3C3C;
                border: 1px solid #555555;
                border-radius: 6px;
                padding: 8px;
                color: #E0E0E0;
            }
            QLineEdit:focus {
                border: 2px solid #4CAF50;
            }
        """)
        email_layout.addWidget(self.email_field)
        
        account_layout.addWidget(email_group)
        
        # Password fields
        password_group = QGroupBox("Смена пароля")
        password_group.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                color: #E0E0E0;
                border: 1px solid #555555;
                border-radius: 8px;
                margin-top: 1ex;
                padding-top: 10px;
            }
            QGroupBox:title {
                subcontrol-origin: margin;
                subcontrol-position: top center;
                padding: 0 5px;
            }
        """)
        password_layout = QVBoxLayout(password_group)
        
        self.password_field = QLineEdit()
        self.password_field.setEchoMode(QLineEdit.Password)
        self.password_field.setPlaceholderText("Новый пароль")
        self.password_field.setStyleSheet("""
            QLineEdit {
                background-color: #3C3C3C;
                border: 1px solid #555555;
                border-radius: 6px;
                padding: 8px;
                color: #E0E0E0;
            }
            QLineEdit:focus {
                border: 2px solid #4CAF50;
            }
        """)
        password_layout.addWidget(self.password_field)
        
        self.confirm_password_field = QLineEdit()
        self.confirm_password_field.setEchoMode(QLineEdit.Password)
        self.confirm_password_field.setPlaceholderText("Подтвердите пароль")
        self.confirm_password_field.setStyleSheet("""
            QLineEdit {
                background-color: #3C3C3C;
                border: 1px solid #555555;
                border-radius: 6px;
                padding: 8px;
                color: #E0E0E0;
            }
            QLineEdit:focus {
                border: 2px solid #4CAF50;
            }
        """)
        password_layout.addWidget(self.confirm_password_field)
        
        account_layout.addWidget(password_group)
        
        # Add stretch to push content up
        account_layout.addStretch()
        
        # Save button
        save_btn = AnimatedButton("Сохранить изменения")
        save_btn.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                border-radius: 6px;
                font-weight: bold;
                font-size: 14px;
                padding: 12px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QPushButton:pressed {
                background-color: #3d8b40;
            }
        """)
        save_btn.clicked.connect(self.save_account_changes)
        account_layout.addWidget(save_btn)
        
        self.tab_widget.addTab(account_widget, "Учетная запись")
    
    def create_privacy_tab(self):
        privacy_widget = QWidget()
        privacy_layout = QVBoxLayout(privacy_widget)
        privacy_layout.setContentsMargins(20, 20, 20, 20)
        
        # Data collection
        data_group = QGroupBox("Сбор данных")
        data_group.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                color: #E0E0E0;
                border: 1px solid #555555;
                border-radius: 8px;
                margin-top: 1ex;
                padding-top: 10px;
            }
            QGroupBox:title {
                subcontrol-origin: margin;
                subcontrol-position: top center;
                padding: 0 5px;
            }
        """)
        data_layout = QVBoxLayout(data_group)
        
        self.data_collection_checkbox = QCheckBox("Разрешить анонимную сбору статистики")
        self.data_collection_checkbox.setChecked(True)
        self.data_collection_checkbox.setStyleSheet("""
            QCheckBox {
                color: #E0E0E0;
                spacing: 10px;
            }
            QCheckBox::indicator {
                width: 18px;
                height: 18px;
            }
            QCheckBox::indicator:unchecked {
                border: 2px solid #555555;
                background-color: #2D2D30;
                border-radius: 3px;
            }
            QCheckBox::indicator:checked {
                border: 2px solid #4CAF50;
                background-color: #4CAF50;
                border-radius: 3px;
            }
        """)
        data_layout.addWidget(self.data_collection_checkbox)
        
        self.data_sharing_checkbox = QCheckBox("Разрешить обмен данными с другими пользователями")
        self.data_sharing_checkbox.setChecked(False)
        self.data_sharing_checkbox.setStyleSheet("""
            QCheckBox {
                color: #E0E0E0;
                spacing: 10px;
            }
            QCheckBox::indicator {
                width: 18px;
                height: 18px;
            }
            QCheckBox::indicator:unchecked {
                border: 2px solid #555555;
                background-color: #2D2D30;
                border-radius: 3px;
            }
            QCheckBox::indicator:checked {
                border: 2px solid #4CAF50;
                background-color: #4CAF50;
                border-radius: 3px;
            }
        """)
        data_layout.addWidget(self.data_sharing_checkbox)
        
        privacy_layout.addWidget(data_group)
        
        # Security settings
        security_group = QGroupBox("Безопасность")
        security_group.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                color: #E0E0E0;
                border: 1px solid #555555;
                border-radius: 8px;
                margin-top: 1ex;
                padding-top: 10px;
            }
            QGroupBox:title {
                subcontrol-origin: margin;
                subcontrol-position: top center;
                padding: 0 5px;
            }
        """)
        security_layout = QVBoxLayout(security_group)
        
        self.biometric_checkbox = QCheckBox("Использовать биометрическую аутентификацию")
        self.biometric_checkbox.setChecked(False)
        self.biometric_checkbox.setStyleSheet("""
            QCheckBox {
                color: #E0E0E0;
                spacing: 10px;
            }
            QCheckBox::indicator {
                width: 18px;
                height: 18px;
            }
            QCheckBox::indicator:unchecked {
                border: 2px solid #555555;
                background-color: #2D2D30;
                border-radius: 3px;
            }
            QCheckBox::indicator:checked {
                border: 2px solid #4CAF50;
                background-color: #4CAF50;
                border-radius: 3px;
            }
        """)
        security_layout.addWidget(self.biometric_checkbox)
        
        self.auto_logout_checkbox = QCheckBox("Автоматический выход после бездействия")
        self.auto_logout_checkbox.setChecked(True)
        self.auto_logout_checkbox.setStyleSheet("""
            QCheckBox {
                color: #E0E0E0;
                spacing: 10px;
            }
            QCheckBox::indicator {
                width: 18px;
                height: 18px;
            }
            QCheckBox::indicator:unchecked {
                border: 2px solid #555555;
                background-color: #2D2D30;
                border-radius: 3px;
            }
            QCheckBox::indicator:checked {
                border: 2px solid #4CAF50;
                background-color: #4CAF50;
                border-radius: 3px;
            }
        """)
        security_layout.addWidget(self.auto_logout_checkbox)
        
        privacy_layout.addWidget(security_group)
        
        # Add stretch to push content up
        privacy_layout.addStretch()
        
        # Save button
        save_btn = AnimatedButton("Сохранить настройки")
        save_btn.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                border-radius: 6px;
                font-weight: bold;
                font-size: 14px;
                padding: 12px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QPushButton:pressed {
                background-color: #3d8b40;
            }
        """)
        save_btn.clicked.connect(self.save_privacy_settings)
        privacy_layout.addWidget(save_btn)
        
        self.tab_widget.addTab(privacy_widget, "Конфиденциальность")
    
    def create_messenger_tab(self):
        messenger_widget = QWidget()
        messenger_layout = QVBoxLayout(messenger_widget)
        messenger_layout.setContentsMargins(20, 20, 20, 20)
        
        # Port setting
        port_group = QGroupBox("Настройки соединения")
        port_group.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                color: #E0E0E0;
                border: 1px solid #555555;
                border-radius: 8px;
                margin-top: 1ex;
                padding-top: 10px;
            }
            QGroupBox:title {
                subcontrol-origin: margin;
                subcontrol-position: top center;
                padding: 0 5px;
            }
        """)
        port_layout = QVBoxLayout(port_group)
        
        port_label = QLabel("Порт для мессенджера:")
        port_label.setStyleSheet("color: #E0E0E0; font-weight: normal;")
        port_layout.addWidget(port_label)
        
        self.port_field = QLineEdit("12345")
        self.port_field.setStyleSheet("""
            QLineEdit {
                background-color: #3C3C3C;
                border: 1px solid #555555;
                border-radius: 6px;
                padding: 8px;
                color: #E0E0E0;
            }
            QLineEdit:focus {
                border: 2px solid #4CAF50;
            }
        """)
        port_layout.addWidget(self.port_field)
        
        messenger_layout.addWidget(port_group)
        
        # Nickname setting
        nickname_group = QGroupBox("Отображаемое имя")
        nickname_group.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                color: #E0E0E0;
                border: 1px solid #555555;
                border-radius: 8px;
                margin-top: 1ex;
                padding-top: 10px;
            }
            QGroupBox:title {
                subcontrol-origin: margin;
                subcontrol-position: top center;
                padding: 0 5px;
            }
        """)
        nickname_layout = QVBoxLayout(nickname_group)
        
        nickname_label = QLabel("Никнейм в сети:")
        nickname_label.setStyleSheet("color: #E0E0E0; font-weight: normal;")
        nickname_layout.addWidget(nickname_label)
        
        self.nickname_field = QLineEdit()
        if hasattr(self.parent_app, 'current_user') and self.parent_app.current_user:
            self.nickname_field.setText(self.parent_app.current_user['username'])
        self.nickname_field.setStyleSheet("""
            QLineEdit {
                background-color: #3C3C3C;
                border: 1px solid #555555;
                border-radius: 6px;
                padding: 8px;
                color: #E0E0E0;
            }
            QLineEdit:focus {
                border: 2px solid #4CAF50;
            }
        """)
        nickname_layout.addWidget(self.nickname_field)
        
        messenger_layout.addWidget(nickname_group)
        
        # Notification settings
        notification_group = QGroupBox("Уведомления")
        notification_group.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                color: #E0E0E0;
                border: 1px solid #555555;
                border-radius: 8px;
                margin-top: 1ex;
                padding-top: 10px;
            }
            QGroupBox:title {
                subcontrol-origin: margin;
                subcontrol-position: top center;
                padding: 0 5px;
            }
        """)
        notification_layout = QVBoxLayout(notification_group)
        
        self.sound_checkbox = QCheckBox("Включить звуковые уведомления")
        self.sound_checkbox.setChecked(True)
        self.sound_checkbox.setStyleSheet("""
            QCheckBox {
                color: #E0E0E0;
                spacing: 10px;
            }
            QCheckBox::indicator {
                width: 18px;
                height: 18px;
            }
            QCheckBox::indicator:unchecked {
                border: 2px solid #555555;
                background-color: #2D2D30;
                border-radius: 3px;
            }
            QCheckBox::indicator:checked {
                border: 2px solid #4CAF50;
                background-color: #4CAF50;
                border-radius: 3px;
            }
        """)
        notification_layout.addWidget(self.sound_checkbox)
        
        self.desktop_notifications_checkbox = QCheckBox("Показывать уведомления на рабочем столе")
        self.desktop_notifications_checkbox.setChecked(True)
        self.desktop_notifications_checkbox.setStyleSheet("""
            QCheckBox {
                color: #E0E0E0;
                spacing: 10px;
            }
            QCheckBox::indicator {
                width: 18px;
                height: 18px;
            }
            QCheckBox::indicator:unchecked {
                border: 2px solid #555555;
                background-color: #2D2D30;
                border-radius: 3px;
            }
            QCheckBox::indicator:checked {
                border: 2px solid #4CAF50;
                background-color: #4CAF50;
                border-radius: 3px;
            }
        """)
        notification_layout.addWidget(self.desktop_notifications_checkbox)
        
        messenger_layout.addWidget(notification_group)
        
        # Add stretch to push content up
        messenger_layout.addStretch()
        
        # Save button
        save_btn = AnimatedButton("Сохранить настройки")
        save_btn.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                border-radius: 6px;
                font-weight: bold;
                font-size: 14px;
                padding: 12px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QPushButton:pressed {
                background-color: #3d8b40;
            }
        """)
        save_btn.clicked.connect(self.save_messenger_settings)
        messenger_layout.addWidget(save_btn)
        
        self.tab_widget.addTab(messenger_widget, "Мессенджер")
    
    def save_appearance_settings(self):
        # In a real app, this would save appearance settings to config
        from PySide6.QtWidgets import QMessageBox
        msg = QMessageBox()
        msg.setWindowTitle("Настройки сохранены")
        msg.setText("Настройки внешнего вида успешно сохранены!")
        msg.setIcon(QMessageBox.Information)
        msg.setStyleSheet("""
            QMessageBox {
                background-color: #2D2D30;
                color: #E0E0E0;
            }
            QMessageBox QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                border-radius: 6px;
                padding: 8px 16px;
            }
            QMessageBox QPushButton:hover {
                background-color: #45a049;
            }
        """)
        msg.exec_()
    
    def save_account_changes(self):
        # In a real app, this would save account changes to database
        from PySide6.QtWidgets import QMessageBox
        msg = QMessageBox()
        msg.setWindowTitle("Изменения сохранены")
        msg.setText("Изменения учетной записи успешно сохранены!")
        msg.setIcon(QMessageBox.Information)
        msg.setStyleSheet("""
            QMessageBox {
                background-color: #2D2D30;
                color: #E0E0E0;
            }
            QMessageBox QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                border-radius: 6px;
                padding: 8px 16px;
            }
            QMessageBox QPushButton:hover {
                background-color: #45a049;
            }
        """)
        msg.exec_()
    
    def save_privacy_settings(self):
        # In a real app, this would save privacy settings to config
        from PySide6.QtWidgets import QMessageBox
        msg = QMessageBox()
        msg.setWindowTitle("Настройки сохранены")
        msg.setText("Настройки конфиденциальности успешно сохранены!")
        msg.setIcon(QMessageBox.Information)
        msg.setStyleSheet("""
            QMessageBox {
                background-color: #2D2D30;
                color: #E0E0E0;
            }
            QMessageBox QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                border-radius: 6px;
                padding: 8px 16px;
            }
            QMessageBox QPushButton:hover {
                background-color: #45a049;
            }
        """)
        msg.exec_()
    
    def save_messenger_settings(self):
        # In a real app, this would save messenger settings to config
        from PySide6.QtWidgets import QMessageBox
        msg = QMessageBox()
        msg.setWindowTitle("Настройки сохранены")
        msg.setText("Настройки мессенджера успешно сохранены!")
        msg.setIcon(QMessageBox.Information)
        msg.setStyleSheet("""
            QMessageBox {
                background-color: #2D2D30;
                color: #E0E0E0;
            }
            QMessageBox QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                border-radius: 6px;
                padding: 8px 16px;
            }
            QMessageBox QPushButton:hover {
                background-color: #45a049;
            }
        """)
        msg.exec_()