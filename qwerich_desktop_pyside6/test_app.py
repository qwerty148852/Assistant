#!/usr/bin/env python3
"""
Test script to verify that the enhanced Qwerich Desktop Application works correctly
"""

import sys
import os

# Add project root to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_imports():
    """Test that all modules can be imported without errors"""
    print("Testing module imports...")
    
    try:
        from modules.main_app_screen import MainAppScreen
        print("✓ MainAppScreen imported successfully")
    except Exception as e:
        print(f"✗ Error importing MainAppScreen: {e}")
        return False
    
    try:
        from modules.assistant_chat.chat_screen_pyside6 import ModernChatScreen
        print("✓ ModernChatScreen imported successfully")
    except Exception as e:
        print(f"✗ Error importing ModernChatScreen: {e}")
        return False
    
    try:
        from modules.messenger.messenger_screen_pyside6 import ModernMessengerScreen
        print("✓ ModernMessengerScreen imported successfully")
    except Exception as e:
        print(f"✗ Error importing ModernMessengerScreen: {e}")
        return False
    
    try:
        from modules.documentation.docs_screen_pyside6 import ModernDocumentationScreen
        print("✓ ModernDocumentationScreen imported successfully")
    except Exception as e:
        print(f"✗ Error importing ModernDocumentationScreen: {e}")
        return False
    
    try:
        from modules.settings.settings_screen_pyside6 import SettingsScreen
        print("✓ SettingsScreen imported successfully")
    except Exception as e:
        print(f"✗ Error importing SettingsScreen: {e}")
        return False
    
    print("All imports successful!")
    return True

def test_chat_functionality():
    """Test the chat engine functionality"""
    print("\nTesting chat engine functionality...")
    
    try:
        from modules.assistant_chat.chat_engine import ChatEngine
        engine = ChatEngine()
        
        # Test a few sample messages
        test_messages = [
            "Привет",
            "Как дела?",
            "Спасибо",
            "Пока"
        ]
        
        for msg in test_messages:
            response = engine.generate_response(msg)  # Use generate_response method
            print(f"Input: '{msg}' -> Response: '{response}'")
        
        print("✓ Chat engine functionality works!")
        return True
    except Exception as e:
        print(f"✗ Error testing chat engine: {e}")
        return False

def main():
    print("Testing Qwerich Desktop Application (Enhanced Version)")
    print("=" * 50)
    
    # Test imports
    if not test_imports():
        print("\nImport tests failed. Please check the error messages above.")
        return False
    
    # Test functionality
    if not test_chat_functionality():
        print("\nFunctionality tests failed. Please check the error messages above.")
        return False
    
    print("\n" + "=" * 50)
    print("All tests passed! The enhanced application is ready to run.")
    print("You can start the application with: python main.py")
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)