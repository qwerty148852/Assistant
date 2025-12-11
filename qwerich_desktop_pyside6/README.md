# Qwerich Desktop Application (PySide6 Version)

This is a beautiful, modern desktop application built with PySide6. It features a sleek dark theme and intuitive user interface.

## Features

- Beautiful dark-themed GUI using PySide6
- User authentication system (login/register)
- System information monitoring
- Modular architecture
- Responsive design

## Requirements

- Python 3.8+
- PySide6
- psutil
- bcrypt
- pillow

## Installation

1. Clone the repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the application:
   ```bash
   python main.py
   ```

## Architecture

The application follows a modern PySide6 architecture with:

- QMainWindow as main window
- QStackedWidget for navigation between screens
- QSplitter for main layout with navigation sidebar
- Custom styling with QSS (Qt Style Sheets)
- Responsive layouts using QVBoxLayout, QHBoxLayout, and QFormLayout

## Screens

1. **Login Screen** - Secure user authentication
2. **Registration Screen** - User account creation
3. **Main Application Screen** - Features navigation sidebar and content area with:
   - Home dashboard
   - System information
   - Chat interface
   - Documentation
   - Settings
   - LAN Messenger

## Design Highlights

- **Modern Dark Theme**: Sleek dark interface with carefully chosen colors
- **Responsive Layout**: Adapts to different screen sizes
- **Intuitive Navigation**: Clear sidebar navigation system
- **Consistent Styling**: Uniform look and feel across all components
- **Accessibility**: Proper contrast and readable fonts

## Modules

- **Authentication**: Secure login and registration system
- **System Monitor**: Real-time system information display
- **Database**: SQLite-based user management
- **Settings**: Application configuration management

## License

This project is licensed under the MIT License - see the LICENSE file for details.