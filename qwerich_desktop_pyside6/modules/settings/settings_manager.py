"""
Settings Manager for Qwerich Desktop Application
Handles application settings, themes, and user preferences
"""

import json
import os


class SettingsManager:
    def __init__(self, settings_file="settings.json"):
        self.settings_file = settings_file
        self.default_settings = {
            "theme": "deep_forest",
            "animations_enabled": True,
            "font_size": 16,
            "account": {
                "username": "",
                "email": ""
            },
            "messenger": {
                "nickname": "",
                "port": 12345,
                "sound_notifications": True
            },
            "privacy": {
                "collect_anonymous_data": False
            }
        }
        self.settings = self.load_settings()
    
    def load_settings(self):
        """Load settings from file or create default ones"""
        try:
            with open(self.settings_file, 'r', encoding='utf-8') as f:
                loaded_settings = json.load(f)
                # Merge with defaults to ensure all keys exist
                return self.merge_settings(self.default_settings, loaded_settings)
        except FileNotFoundError:
            # Create settings file with defaults
            self.save_settings(self.default_settings)
            return self.default_settings
    
    def merge_settings(self, default, override):
        """Merge default settings with overrides recursively"""
        result = default.copy()
        for key, value in override.items():
            if isinstance(value, dict) and key in result and isinstance(result[key], dict):
                result[key] = self.merge_settings(result[key], value)
            else:
                result[key] = value
        return result
    
    def save_settings(self, settings=None):
        """Save settings to file"""
        if settings is None:
            settings = self.settings
        
        with open(self.settings_file, 'w', encoding='utf-8') as f:
            json.dump(settings, f, ensure_ascii=False, indent=2)
    
    def get_setting(self, key_path):
        """Get a setting value using dot notation (e.g., 'theme' or 'account.username')"""
        keys = key_path.split('.')
        value = self.settings
        
        for key in keys:
            if isinstance(value, dict) and key in value:
                value = value[key]
            else:
                return None
        
        return value
    
    def set_setting(self, key_path, value):
        """Set a setting value using dot notation"""
        keys = key_path.split('.')
        current = self.settings
        
        # Navigate to the parent of the target key
        for key in keys[:-1]:
            if key not in current or not isinstance(current[key], dict):
                current[key] = {}
            current = current[key]
        
        # Set the final value
        current[keys[-1]] = value
        
        # Save to file
        self.save_settings()
    
    def get_available_themes(self):
        """Return list of available color themes"""
        return [
            "deep_forest",
            "ocean_blue", 
            "dark_amethyst",
            "light_breeze",
            "true_black"
        ]
    
    def apply_theme(self, theme_name):
        """Apply a specific theme"""
        if theme_name in self.get_available_themes():
            self.set_setting('theme', theme_name)
            return True
        return False
    
    def toggle_animations(self):
        """Toggle animation settings"""
        current = self.get_setting('animations_enabled')
        self.set_setting('animations_enabled', not current)
    
    def get_user_account_info(self):
        """Get user account information"""
        return {
            'username': self.get_setting('account.username'),
            'email': self.get_setting('account.email')
        }
    
    def update_account_info(self, username=None, email=None, password=None):
        """Update user account information"""
        if username is not None:
            self.set_setting('account.username', username)
        if email is not None:
            self.set_setting('account.email', email)
        # Password would be handled separately due to security considerations
    
    def get_messenger_settings(self):
        """Get messenger-specific settings"""
        return {
            'nickname': self.get_setting('messenger.nickname'),
            'port': self.get_setting('messenger.port'),
            'sound_notifications': self.get_setting('messenger.sound_notifications')
        }
    
    def update_messenger_settings(self, **kwargs):
        """Update messenger settings"""
        for key, value in kwargs.items():
            if key in ['nickname', 'port', 'sound_notifications']:
                self.set_setting(f'messenger.{key}', value)
    
    def reset_to_defaults(self):
        """Reset all settings to default values"""
        self.settings = self.default_settings.copy()
        self.save_settings()


# Theme definitions
THEME_DEFINITIONS = {
    "deep_forest": {
        "primary_palette": "Green",
        "primary_hue": "700",
        "primary_light": "#1a4d1a",
        "primary_dark": "#0a2f0a",
        "accent_palette": "Green",
        "accent_hue": "A200",
        "background_color": "#0a2f0a",
        "text_color": "#ffffff",
        "secondary_text_color": "#cccccc"
    },
    "ocean_blue": {
        "primary_palette": "Blue",
        "primary_hue": "800",
        "primary_light": "#48cae4",
        "primary_dark": "#0d1b2a",
        "accent_palette": "Cyan",
        "accent_hue": "A200",
        "background_color": "#0d1b2a",
        "text_color": "#ffffff",
        "secondary_text_color": "#cccccc"
    },
    "dark_amethyst": {
        "primary_palette": "Purple",
        "primary_hue": "800",
        "primary_light": "#9d4edd",
        "primary_dark": "#1a1a2e",
        "accent_palette": "DeepPurple",
        "accent_hue": "A200",
        "background_color": "#1a1a2e",
        "text_color": "#ffffff",
        "secondary_text_color": "#cccccc"
    },
    "light_breeze": {
        "primary_palette": "Gray",
        "primary_hue": "100",
        "primary_light": "#e9ecef",
        "primary_dark": "#f8f9fa",
        "accent_palette": "Green",
        "accent_hue": "700",
        "background_color": "#ffffff",
        "text_color": "#000000",
        "secondary_text_color": "#666666"
    },
    "true_black": {
        "primary_palette": "Gray",
        "primary_hue": "900",
        "primary_light": "#00ff00",
        "primary_dark": "#000000",
        "accent_palette": "Green",
        "accent_hue": "A400",
        "background_color": "#000000",
        "text_color": "#00ff00",
        "secondary_text_color": "#00cc00"
    }
}


def get_theme_definition(theme_name):
    """Get the definition for a specific theme"""
    return THEME_DEFINITIONS.get(theme_name, THEME_DEFINITIONS["deep_forest"])


# Example usage
if __name__ == "__main__":
    settings = SettingsManager()
    
    print("Current theme:", settings.get_setting('theme'))
    print("Animations enabled:", settings.get_setting('animations_enabled'))
    print("Available themes:", settings.get_available_themes())
    
    # Change theme
    settings.apply_theme('ocean_blue')
    print("Changed theme to:", settings.get_setting('theme'))
    
    # Update account info
    settings.update_account_info(username='testuser', email='test@example.com')
    print("Account info:", settings.get_user_account_info())