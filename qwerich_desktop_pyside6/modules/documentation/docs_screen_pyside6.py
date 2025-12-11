"""
Enhanced Documentation Screen for Qwerich Desktop Application (PySide6 Version)
Beautiful GUI with animations and gray-green theme
"""

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, 
    QTextEdit, QLineEdit, QFrame, QScrollArea, QListWidget,
    QListWidgetItem, QTreeWidget, QTreeWidgetItem, QTabWidget
)
from PySide6.QtCore import Qt, QEasingCurve, QPropertyAnimation, QRect, QUrl
from PySide6.QtGui import QFont, QDesktopServices


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


class DocumentationScreen(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
    
    def setup_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(15)
        
        # Title
        title_label = QLabel("Документация")
        title_font = QFont()
        title_font.setPointSize(18)
        title_font.setBold(True)
        title_label.setFont(title_font)
        title_label.setStyleSheet("color: #E0E0E0; margin-bottom: 10px;")
        title_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(title_label)
        
        # Create tab widget for different documentation sections
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
        
        # Add documentation tabs
        self.create_general_docs_tab()
        self.create_features_tab()
        self.create_api_docs_tab()
        self.create_troubleshooting_tab()
        
        main_layout.addWidget(self.tab_widget)
    
    def create_general_docs_tab(self):
        general_widget = QWidget()
        general_layout = QVBoxLayout(general_widget)
        general_layout.setContentsMargins(20, 20, 20, 20)
        
        # Documentation content
        docs_content = QTextEdit()
        docs_content.setReadOnly(True)
        docs_content.setStyleSheet("""
            QTextEdit {
                background-color: #1E1E1E;
                border: 1px solid #555555;
                border-radius: 8px;
                padding: 20px;
                color: #CCCCCC;
                font-size: 14px;
                line-height: 1.6;
            }
        """)
        
        # Add sample documentation content
        docs_html = """
        <h2 style="color: #4CAF50; text-align: center;">Добро пожаловать в документацию Qwerich</h2>
        
        <h3 style="color: #E0E0E0; margin-top: 20px;">Общее описание</h3>
        <p>Qwerich - это многофункциональное приложение для управления системой и общения. 
        Приложение предоставляет широкий спектр возможностей для работы с системой и взаимодействия с другими пользователями.</p>
        
        <h3 style="color: #E0E0E0; margin-top: 20px;">Основные функции</h3>
        <ul style="color: #CCCCCC; margin-left: 20px;">
            <li>Интерактивный чат с виртуальным ассистентом</li>
            <li>Мониторинг системных ресурсов</li>
            <li>LAN мессенджер для общения в локальной сети</li>
            <li>Настройка персональных параметров</li>
            <li>Документация и справочная информация</li>
        </ul>
        
        <h3 style="color: #E0E0E0; margin-top: 20px;">Начало работы</h3>
        <p>Для начала работы с приложением:</p>
        <ol style="color: #CCCCCC; margin-left: 20px;">
            <li>Создайте учетную запись или войдите в существующую</li>
            <li>Ознакомьтесь с основными разделами приложения</li>
            <li>Настройте персональные параметры в разделе "Настройки"</li>
            <li>Используйте чат для получения помощи от ассистента</li>
        </ol>
        
        <h3 style="color: #E0E0E0; margin-top: 20px;">Поддержка</h3>
        <p>Если у вас возникли вопросы или проблемы, обратитесь в службу поддержки 
        через раздел "Обратная связь" или воспользуйтесь встроенным чатом с ассистентом.</p>
        """
        
        docs_content.setHtml(docs_html)
        general_layout.addWidget(docs_content)
        
        self.tab_widget.addTab(general_widget, "Общая информация")
    
    def create_features_tab(self):
        features_widget = QWidget()
        features_layout = QVBoxLayout(features_widget)
        features_layout.setContentsMargins(20, 20, 20, 20)
        
        # Features content
        features_content = QTextEdit()
        features_content.setReadOnly(True)
        features_content.setStyleSheet("""
            QTextEdit {
                background-color: #1E1E1E;
                border: 1px solid #555555;
                border-radius: 8px;
                padding: 20px;
                color: #CCCCCC;
                font-size: 14px;
                line-height: 1.6;
            }
        """)
        
        features_html = """
        <h2 style="color: #4CAF50; text-align: center;">Функции приложения</h2>
        
        <h3 style="color: #E0E0E0; margin-top: 20px;">1. Чат с ассистентом</h3>
        <p>Интерактивный чат позволяет получить помощь от виртуального ассистента Qwerich. 
        Ассистент может ответить на вопросы, помочь с настройками и предоставить информацию о системе.</p>
        
        <h3 style="color: #E0E0E0; margin-top: 20px;">2. Мониторинг системы</h3>
        <p>В разделе "Системная информация" вы можете отслеживать состояние системных ресурсов:</p>
        <ul style="color: #CCCCCC; margin-left: 20px;">
            <li>Загрузка процессора</li>
            <li>Использование оперативной памяти</li>
            <li>Состояние дисков</li>
            <li>Сетевая активность</li>
            <li>Температура компонентов</li>
        </ul>
        
        <h3 style="color: #E0E0E0; margin-top: 20px;">3. LAN Мессенджер</h3>
        <p>Встроенный мессенджер позволяет общаться с другими пользователями в локальной сети. 
        Функции мессенджера включают:</p>
        <ul style="color: #CCCCCC; margin-left: 20px;">
            <li>Обмен текстовыми сообщениями</li>
            <li>Отображение статуса собеседников</li>
            <li>Уведомления о новых сообщениях</li>
            <li>История переписки</li>
        </ul>
        
        <h3 style="color: #E0E0E0; margin-top: 20px;">4. Настройки</h3>
        <p>Персонализируйте приложение под свои предпочтения:</p>
        <ul style="color: #CCCCCC; margin-left: 20px;">
            <li>Выбор темы оформления</li>
            <li>Настройка анимаций</li>
            <li>Управление уведомлениями</li>
            <li>Параметры безопасности</li>
        </ul>
        
        <h3 style="color: #E0E0E0; margin-top: 20px;">5. Документация</h3>
        <p>Полная документация доступна в нескольких разделах для удобного поиска информации.</p>
        """
        
        features_content.setHtml(features_html)
        features_layout.addWidget(features_content)
        
        self.tab_widget.addTab(features_widget, "Функции")
    
    def create_api_docs_tab(self):
        api_widget = QWidget()
        api_layout = QVBoxLayout(api_widget)
        api_layout.setContentsMargins(20, 20, 20, 20)
        
        # API documentation content
        api_content = QTextEdit()
        api_content.setReadOnly(True)
        api_content.setStyleSheet("""
            QTextEdit {
                background-color: #1E1E1E;
                border: 1px solid #555555;
                border-radius: 8px;
                padding: 20px;
                color: #CCCCCC;
                font-size: 14px;
                line-height: 1.6;
            }
        """)
        
        api_html = """
        <h2 style="color: #4CAF50; text-align: center;">API Документация</h2>
        
        <h3 style="color: #E0E0E0; margin-top: 20px;">Обзор API</h3>
        <p>Qwerich предоставляет API для интеграции с внешними системами и автоматизации задач.</p>
        
        <h3 style="color: #E0E0E0; margin-top: 20px;">Аутентификация</h3>
        <p>Для доступа к API требуется токен аутентификации, который можно получить в настройках приложения.</p>
        
        <h3 style="color: #E0E0E0; margin-top: 20px;">Доступные методы</h3>
        <ul style="color: #CCCCCC; margin-left: 20px;">
            <li><strong>GET /api/system/info</strong> - Получение информации о системе</li>
            <li><strong>GET /api/chat/messages</strong> - Получение истории сообщений</li>
            <li><strong>POST /api/chat/send</strong> - Отправка сообщения</li>
            <li><strong>GET /api/settings</strong> - Получение настроек пользователя</li>
            <li><strong>PUT /api/settings</strong> - Обновление настроек пользователя</li>
        </ul>
        
        <h3 style="color: #E0E0E0; margin-top: 20px;">Пример запроса</h3>
        <pre style="background-color: #3C3C3C; padding: 15px; border-radius: 5px; color: #E0E0E0;">
        curl -X GET "https://localhost:8080/api/system/info" 
             -H "Authorization: Bearer YOUR_TOKEN"
        </pre>
        
        <h3 style="color: #E0E0E0; margin-top: 20px;">Пример ответа</h3>
        <pre style="background-color: #3C3C3C; padding: 15px; border-radius: 5px; color: #E0E0E0;">
        {
            "cpu_usage": 15.2,
            "memory_usage": 42.7,
            "disk_usage": 68.3,
            "network_status": "connected"
        }
        </pre>
        """
        
        api_content.setHtml(api_html)
        api_layout.addWidget(api_content)
        
        self.tab_widget.addTab(api_widget, "API")
    
    def create_troubleshooting_tab(self):
        troubleshoot_widget = QWidget()
        troubleshoot_layout = QVBoxLayout(troubleshoot_widget)
        troubleshoot_layout.setContentsMargins(20, 20, 20, 20)
        
        # Troubleshooting content
        troubleshoot_content = QTextEdit()
        troubleshoot_content.setReadOnly(True)
        troubleshoot_content.setStyleSheet("""
            QTextEdit {
                background-color: #1E1E1E;
                border: 1px solid #555555;
                border-radius: 8px;
                padding: 20px;
                color: #CCCCCC;
                font-size: 14px;
                line-height: 1.6;
            }
        """)
        
        troubleshoot_html = """
        <h2 style="color: #4CAF50; text-align: center;">Устранение неполадок</h2>
        
        <h3 style="color: #E0E0E0; margin-top: 20px;">Частые проблемы</h3>
        
        <h4 style="color: #E0E0E0; margin-top: 15px;">Проблема: Приложение не запускается</h4>
        <p><strong>Решение:</strong> Проверьте, установлены ли все необходимые зависимости. 
        Убедитесь, что версия Python не ниже 3.8.</p>
        
        <h4 style="color: #E0E0E0; margin-top: 15px;">Проблема: Медленная работа приложения</h4>
        <p><strong>Решение:</strong> Закройте другие приложения, чтобы освободить системные ресурсы. 
        Проверьте использование памяти в разделе "Системная информация".</p>
        
        <h4 style="color: #E0E0E0; margin-top: 15px;">Проблема: Не удается подключиться к мессенджеру</h4>
        <p><strong>Решение:</strong> Убедитесь, что все пользователи находятся в одной локальной сети. 
        Проверьте настройки брандмауэра и порты подключения.</p>
        
        <h4 style="color: #E0E0E0; margin-top: 15px;">Проблема: Ассистент не отвечает</h4>
        <p><strong>Решение:</strong> Проверьте подключение к интернету. 
        Попробуйте перезапустить чат или перезапустить приложение.</p>
        
        <h3 style="color: #E0E0E0; margin-top: 20px;">Поддержка</h3>
        <p>Если вы не можете решить проблему самостоятельно, обратитесь в службу поддержки:</p>
        <ul style="color: #CCCCCC; margin-left: 20px;">
            <li>Email: support@qwerich.local</li>
            <li>Форум: https://forum.qwerich.local</li>
            <li>Чат поддержки: встроен в приложение</li>
        </ul>
        
        <h3 style="color: #E0E0E0; margin-top: 20px;">Диагностика</h3>
        <p>Для более точной диагностики проблем, используйте встроенные инструменты диагностики 
        в разделе "Системная информация".</p>
        """
        
        troubleshoot_content.setHtml(troubleshoot_html)
        troubleshoot_layout.addWidget(troubleshoot_content)
        
        self.tab_widget.addTab(troubleshoot_widget, "Устранение неполадок")


class ModernDocumentationScreen(QWidget):
    """Modern documentation screen with enhanced features"""
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
        
        header_title = QLabel("Документация")
        header_title_font = QFont()
        header_title_font.setPointSize(18)
        header_title_font.setBold(True)
        header_title.setFont(header_title_font)
        header_title.setStyleSheet("color: #E0E0E0;")
        header_layout.addWidget(header_title)
        
        # Search bar
        search_input = QLineEdit()
        search_input.setPlaceholderText("Поиск по документации...")
        search_input.setStyleSheet("""
            QLineEdit {
                background-color: #3C3C3C;
                border: 1px solid #555555;
                border-radius: 15px;
                padding: 8px 15px;
                color: #E0E0E0;
                width: 250px;
            }
            QLineEdit:focus {
                border: 2px solid #4CAF50;
            }
        """)
        header_layout.addWidget(search_input)
        
        header_layout.addStretch()
        
        main_layout.addWidget(header)
        
        # Main content area
        content_frame = QFrame()
        content_frame.setStyleSheet("""
            QFrame {
                background-color: #1E1E1E;
            }
        """)
        
        content_layout = QHBoxLayout(content_frame)
        content_layout.setContentsMargins(0, 0, 0, 0)
        
        # Sidebar with navigation
        sidebar = QFrame()
        sidebar.setFixedWidth(250)
        sidebar.setStyleSheet("""
            QFrame {
                background-color: #252526;
                border-right: 1px solid #444444;
            }
        """)
        
        sidebar_layout = QVBoxLayout(sidebar)
        sidebar_layout.setContentsMargins(10, 10, 10, 10)
        
        sidebar_title = QLabel("Разделы")
        sidebar_title.setStyleSheet("color: #E0E0E0; font-weight: bold; font-size: 16px; margin-bottom: 10px;")
        sidebar_layout.addWidget(sidebar_title)
        
        # Navigation tree
        nav_tree = QTreeWidget()
        nav_tree.setHeaderHidden(True)
        nav_tree.setStyleSheet("""
            QTreeWidget {
                background-color: #252526;
                border: none;
                color: #E0E0E0;
            }
            QTreeWidget::item {
                padding: 8px;
                border-bottom: 1px solid #3C3C3C;
            }
            QTreeWidget::item:selected {
                background-color: #3C3C3C;
            }
            QTreeWidget::branch {
                background-color: #252526;
            }
        """)
        
        # Add navigation items
        root_items = [
            "Общая информация",
            "Функции приложения", 
            "API Документация",
            "Устранение неполадок",
            "FAQ",
            "Контакты поддержки"
        ]
        
        for item_text in root_items:
            item = QTreeWidgetItem(nav_tree)
            item.setText(0, item_text)
            item.setFont(0, QFont("Arial", 11))
        
        sidebar_layout.addWidget(nav_tree)
        
        content_layout.addWidget(sidebar)
        
        # Documentation content area
        content_area = QScrollArea()
        content_area.setStyleSheet("""
            QScrollArea {
                border: none;
                background-color: #1E1E1E;
            }
        """)
        content_area.setWidgetResizable(True)
        
        content_widget = QWidget()
        content_widget.setStyleSheet("background-color: #1E1E1E;")
        
        content_widget_layout = QVBoxLayout(content_widget)
        content_widget_layout.setContentsMargins(30, 30, 30, 30)
        
        # Documentation title
        doc_title = QLabel("Добро пожаловать в документацию Qwerich")
        doc_title_font = QFont()
        doc_title_font.setPointSize(24)
        doc_title_font.setBold(True)
        doc_title.setFont(doc_title_font)
        doc_title.setStyleSheet("color: #E0E0E0; margin-bottom: 20px;")
        content_widget_layout.addWidget(doc_title)
        
        # Documentation content
        content_text = QTextEdit()
        content_text.setReadOnly(True)
        content_text.setStyleSheet("""
            QTextEdit {
                background-color: #2D2D30;
                border: 1px solid #555555;
                border-radius: 8px;
                padding: 25px;
                color: #CCCCCC;
                font-size: 15px;
                line-height: 1.7;
            }
        """)
        
        # Rich documentation content
        doc_html = """
        <h2 style="color: #4CAF50; margin-top: 0;">Введение</h2>
        <p>Qwerich - это современное многофункциональное приложение, разработанное для упрощения 
        управления системными ресурсами и обеспечения эффективного взаимодействия пользователей. 
        Приложение объединяет в себе возможности системного мониторинга, коммуникации и автоматизации.</p>
        
        <h3 style="color: #4CAF50; margin-top: 25px;">Основные возможности</h3>
        <div style="display: flex; flex-wrap: wrap; gap: 20px; margin-top: 15px;">
            <div style="flex: 1; min-width: 300px; background-color: #2D2D30; padding: 20px; border-radius: 8px; border-left: 4px solid #4CAF50;">
                <h4 style="color: #E0E0E0; margin-top: 0;">Интеллектуальный ассистент</h4>
                <p style="color: #CCCCCC;">Встроенный ассистент готов помочь с любыми вопросами, 
                предоставить информацию о системе и помочь в решении задач.</p>
            </div>
            <div style="flex: 1; min-width: 300px; background-color: #2D2D30; padding: 20px; border-radius: 8px; border-left: 4px solid #2196F3;">
                <h4 style="color: #E0E0E0; margin-top: 0;">Мониторинг системы</h4>
                <p style="color: #CCCCCC;">Отслеживайте состояние процессора, памяти, дисков и 
                сетевой активности в реальном времени.</p>
            </div>
            <div style="flex: 1; min-width: 300px; background-color: #2D2D30; padding: 20px; border-radius: 8px; border-left: 4px solid #FF9800;">
                <h4 style="color: #E0E0E0; margin-top: 0;">LAN коммуникации</h4>
                <p style="color: #CCCCCC;">Общайтесь с коллегами в локальной сети через 
                встроенный мессенджер с поддержкой уведомлений.</p>
            </div>
        </div>
        
        <h3 style="color: #4CAF50; margin-top: 30px;">Начало работы</h3>
        <p>Чтобы начать работу с Qwerich, следуйте этим простым шагам:</p>
        <ol style="color: #CCCCCC; margin-left: 20px; margin-top: 15px;">
            <li style="margin-bottom: 10px;"><strong>Регистрация:</strong> Создайте учетную запись 
            или войдите, если она уже существует</li>
            <li style="margin-bottom: 10px;"><strong>Исследование:</strong> Ознакомьтесь с 
            основными разделами приложения</li>
            <li style="margin-bottom: 10px;"><strong>Настройка:</strong> Персонализируйте 
            приложение в разделе "Настройки"</li>
            <li style="margin-bottom: 10px;"><strong>Использование:</strong> Начните 
            использовать функции приложения по назначению</li>
        </ol>
        
        <h3 style="color: #4CAF50; margin-top: 30px;">Поддержка и обратная связь</h3>
        <p>Мы стремимся сделать Qwerich максимально удобным и функциональным. Если у вас есть 
        вопросы, предложения или вы столкнулись с проблемой, не стесняйтесь обращаться к нам:</p>
        <ul style="color: #CCCCCC; margin-left: 20px; margin-top: 15px;">
            <li style="margin-bottom: 8px;">Служба поддержки: <a style="color: #4CAF50;" href="mailto:support@qwerich.local">support@qwerich.local</a></li>
            <li style="margin-bottom: 8px;">Официальный форум: <a style="color: #4CAF50;" href="#" onclick="QDesktopServices.openUrl('https://forum.qwerich.local')">https://forum.qwerich.local</a></li>
            <li style="margin-bottom: 8px;">Встроенный чат с ассистентом</li>
            <li style="margin-bottom: 8px;">Центр помощи в приложении</li>
        </ul>
        
        <div style="margin-top: 30px; padding: 20px; background-color: #2D2D30; border-radius: 8px; border-left: 4px solid #9C27B0;">
            <h4 style="color: #E0E0E0; margin-top: 0;">Совет дня</h4>
            <p style="color: #CCCCCC; margin-bottom: 0;">Используйте сочетания клавиш для быстрого 
            доступа к функциям приложения. Например, Ctrl+D открывает раздел документации, 
            Ctrl+S - настройки, а Ctrl+Q - выход из приложения.</p>
        </div>
        """
        
        content_text.setHtml(doc_html)
        content_widget_layout.addWidget(content_text)
        
        content_area.setWidget(content_widget)
        content_layout.addWidget(content_area)
        
        main_layout.addWidget(content_frame)