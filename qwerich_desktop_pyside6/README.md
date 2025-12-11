# Qwerich Desktop Application (Enhanced PySide6 Version)

This is a beautiful, modern desktop application built with PySide6. It features a sleek gray-green theme with animations and intuitive user interface.

## Features

- Beautiful gray-green themed GUI using PySide6 with animations
- User authentication system (login/register)
- System information monitoring
- Interactive chat with virtual assistant
- LAN messenger for local network communication
- Comprehensive documentation system
- Settings panel with multiple tabs
- Modular architecture
- Responsive design

## Enhancements in this Version

- **Animated UI Elements**: Smooth animations on hover and click events
- **Enhanced Chat Screen**: Modern chat interface with message bubbles and typing indicators
- **Improved Messenger**: Styled contact list with status indicators and message history
- **Modern Settings**: Tabbed interface with appearance, account, privacy, and messenger settings
- **Rich Documentation**: Well-organized documentation with search and navigation
- **Animated Navigation**: Hover animations on sidebar buttons
- **Gradient Backgrounds**: Modern gradient styling in navigation areas
- **Enhanced Styling**: Improved color scheme and visual consistency

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
- Animated buttons with QPropertyAnimation

## Screens

1. **Login Screen** - Secure user authentication
2. **Registration Screen** - User account creation
3. **Main Application Screen** - Features navigation sidebar and content area with:
   - Home dashboard
   - System information
   - Interactive chat with Qwerich assistant
   - LAN Messenger with contacts and messaging
   - Documentation with search and navigation
   - Settings with multiple tabs

## Design Highlights

- **Modern Gray-Green Theme**: Sleek interface with carefully chosen colors
- **Animations**: Smooth hover and transition effects
- **Responsive Layout**: Adapts to different screen sizes
- **Intuitive Navigation**: Clear sidebar navigation system with icons
- **Consistent Styling**: Uniform look and feel across all components
- **Accessibility**: Proper contrast and readable fonts
- **Modern UI Components**: Enhanced message bubbles, contact lists, and input fields

## Modules

- **Authentication**: Secure login and registration system
- **System Monitor**: Real-time system information display
- **Database**: SQLite-based user management
- **Settings**: Application configuration management with multiple tabs
- **Chat Engine**: Intelligent response generation for assistant
- **Messenger**: Local network communication system
- **Documentation**: Comprehensive help system

## License

This project is licensed under the MIT License - see the LICENSE file for details.