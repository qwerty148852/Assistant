"""
Documentation Screen for Qwerich Desktop Application
GUI component for the documentation functionality
"""

import tkinter as tk
from tkinter import ttk
import ttkbootstrap as ttkb
from ttkbootstrap.constants import *


class DocsScreen(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.setup_ui()
    
    def setup_ui(self):
        # Clear existing widgets
        for widget in self.winfo_children():
            widget.destroy()
        
        # Main frame
        main_frame = ttk.Frame(self)
        main_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        title_label = ttk.Label(
            main_frame,
            text="Документация",
            font=("Arial", 16, "bold")
        )
        title_label.pack(pady=(0, 10))
        
        # Create notebook for different documentation sections
        notebook = ttk.Notebook(main_frame)
        notebook.pack(fill='both', expand=True)
        
        # About Qwerich tab
        self.create_about_tab(notebook)
        
        # Getting Started tab
        self.create_getting_started_tab(notebook)
        
        # Messenger tab
        self.create_messenger_tab(notebook)
        
        # System Monitor tab
        self.create_system_monitor_tab(notebook)
        
        # Settings tab
        self.create_settings_tab(notebook)
    
    def create_about_tab(self, notebook):
        about_frame = ttk.Frame(notebook)
        notebook.add(about_frame, text="О Qwerich")
        
        about_text = tk.Text(
            about_frame,
            wrap=tk.WORD,
            state='normal',
            font=("Arial", 11)
        )
        about_text.pack(fill='both', expand=True, padx=10, pady=10)
        
        about_content = """
Добро пожаловать в Qwerich!

Qwerich - это кроссплатформенное десктоп-приложение с графическим интерфейсом, 
разработанное для предоставления пользователю различных функций, включая 
виртуального ассистента, системный монитор, LAN-мессенджер и многое другое.

Философия проекта:
- Простота использования
- Кроссплатформенность
- Богатый функционал
- Интуитивный интерфейс

Версия: 2.0
        """
        
        about_text.insert(tk.END, about_content)
        about_text.config(state='disabled')
    
    def create_getting_started_tab(self, notebook):
        getting_started_frame = ttk.Frame(notebook)
        notebook.add(getting_started_frame, text="Начало работы")
        
        getting_started_text = tk.Text(
            getting_started_frame,
            wrap=tk.WORD,
            state='normal',
            font=("Arial", 11)
        )
        getting_started_text.pack(fill='both', expand=True, padx=10, pady=10)
        
        getting_started_content = """
Начало работы с Qwerich

1. Регистрация:
   - Нажмите "Зарегистрироваться" на главном экране
   - Введите имя пользователя, email и пароль
   - Подтвердите, что вы не робот
   - Нажмите "Создать аккаунт"

2. Вход в систему:
   - Введите свои учетные данные
   - Подтвердите, что вы не робот
   - Нажмите "Войти"

3. Использование чата:
   - Перейдите в раздел "Чат с Qwerich"
   - Введите сообщение в поле ввода
   - Нажмите "Отправить" или Enter

4. Мониторинг системы:
   - Перейдите в раздел "Системная информация"
   - Просмотрите информацию о CPU, памяти, дисках и сети

5. LAN-мессенджер:
   - Перейдите в раздел "LAN Мессенджер"
   - Общайтесь с другими пользователями в локальной сети
        """
        
        getting_started_text.insert(tk.END, getting_started_content)
        getting_started_text.config(state='disabled')
    
    def create_messenger_tab(self, notebook):
        messenger_frame = ttk.Frame(notebook)
        notebook.add(messenger_frame, text="Мессенджер")
        
        messenger_text = tk.Text(
            messenger_frame,
            wrap=tk.WORD,
            state='normal',
            font=("Arial", 11)
        )
        messenger_text.pack(fill='both', expand=True, padx=10, pady=10)
        
        messenger_content = """
LAN-мессенджер

Функции мессенджера:
- Общение с другими пользователями в локальной сети
- Отправка текстовых сообщений
- Отображение статуса "Печатает..."
- Уведомления о новых сообщениях

Как работает:
- Приложение отправляет широковещательные пакеты в локальную сеть
- Обнаруживает другие экземпляры Qwerich
- Устанавливает прямые TCP-соединения для обмена сообщениями

Устранение неполадок:
- Убедитесь, что все устройства находятся в одной локальной сети
- Проверьте настройки брандмауэра
- Убедитесь, что порты не заблокированы
        """
        
        messenger_text.insert(tk.END, messenger_content)
        messenger_text.config(state='disabled')
    
    def create_system_monitor_tab(self, notebook):
        sys_monitor_frame = ttk.Frame(notebook)
        notebook.add(sys_monitor_frame, text="Системный монитор")
        
        sys_monitor_text = tk.Text(
            sys_monitor_frame,
            wrap=tk.WORD,
            state='normal',
            font=("Arial", 11)
        )
        sys_monitor_text.pack(fill='both', expand=True, padx=10, pady=10)
        
        sys_monitor_content = """
Системный монитор

Монитор отображает следующую информацию:

CPU:
- Загрузка каждого ядра в процентах
- Температура процессора (если поддерживается)
- Частота процессора

Память (RAM):
- Общий объем памяти
- Используемая память
- Свободная память
- Процент использования

Диски:
- Информация о каждом разделе
- Тип файловой системы
- Общий объем
- Используемое пространство
- Свободное пространство

Сеть:
- IP-адреса
- Скорость передачи данных
- Скорость приема данных
- Статистика пакетов
        """
        
        sys_monitor_text.insert(tk.END, sys_monitor_content)
        sys_monitor_text.config(state='disabled')
    
    def create_settings_tab(self, notebook):
        settings_frame = ttk.Frame(notebook)
        notebook.add(settings_frame, text="Настройки")
        
        settings_text = tk.Text(
            settings_frame,
            wrap=tk.WORD,
            state='normal',
            font=("Arial", 11)
        )
        settings_text.pack(fill='both', expand=True, padx=10, pady=10)
        
        settings_content = """
Настройки приложения

Вкладка "Внешний вид":
- Выбор одной из 5 цветовых тем
- Настройка размера шрифта
- Переключатель анимаций

Вкладка "Учетная запись":
- Изменение имени пользователя
- Изменение email
- Смена пароля

Вкладка "Конфиденциальность":
- Управление сбором анонимной статистики
- Настройки обмена данными

Вкладка "Мессенджер":
- Настройка порта для мессенджера
- Установка никнейма в сети
- Управление звуковыми уведомлениями
        """
        
        settings_text.insert(tk.END, settings_content)
        settings_text.config(state='disabled')