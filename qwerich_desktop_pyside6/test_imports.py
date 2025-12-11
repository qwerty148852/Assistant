#!/usr/bin/env python3
"""
Test script to verify PySide6 application imports work correctly
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_imports():
    """Test that all modules can be imported without errors"""
    print("Testing PySide6 Qwerich Desktop Application imports...")
    
    try:
        # Test main application
        from main import MainApp
        print("✓ MainApp imported successfully")
        
        # Test PySide6 imports
        from PySide6.QtWidgets import QApplication, QMainWindow
        print("✓ PySide6 imports work correctly")
        
        # Test auth modules
        from modules.auth.login_screen import LoginScreen
        from modules.auth.registration_screen import RegistrationScreen
        print("✓ Authentication modules imported successfully")
        
        # Test main app screen
        from modules.main_app_screen import MainAppScreen
        print("✓ Main application screen imported successfully")
        
        # Test database
        from database import Database
        print("✓ Database module imported successfully")
        
        # Test system info
        from modules.system_info.monitor import SystemMonitor
        print("✓ System monitor module imported successfully")
        
        # Test other modules
        from modules.assistant_chat.chat_screen import ChatScreen
        from modules.documentation.docs_screen import DocsScreen
        from modules.settings.settings_screen import SettingsScreen
        print("✓ All additional modules imported successfully")
        
        print("\n🎉 All imports successful! PySide6 application is ready!")
        print("To run the application, use: python main.py")
        
    except ImportError as e:
        print(f"✗ Import error: {e}")
        return False
    except Exception as e:
        print(f"✗ Error: {e}")
        return False
    
    return True

if __name__ == "__main__":
    success = test_imports()
    if success:
        sys.exit(0)
    else:
        sys.exit(1)