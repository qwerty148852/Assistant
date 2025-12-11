"""
Database module for Qwerich Desktop Application
Handles SQLite database operations for users, chat history, and settings
"""

import sqlite3
import hashlib
import os
from datetime import datetime


class Database:
    def __init__(self, db_path="qwerich.db"):
        self.db_path = db_path
        self.init_db()
    
    def init_db(self):
        """Initialize the database with required tables"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Create users table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                email TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Create chat_history table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS chat_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                message TEXT NOT NULL,
                response TEXT NOT NULL,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        ''')
        
        # Create settings table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS settings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                theme TEXT DEFAULT 'deep_forest',
                animations_enabled BOOLEAN DEFAULT 1,
                font_size INTEGER DEFAULT 16,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def hash_password(self, password):
        """Hash password using SHA-256"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def register_user(self, username, email, password):
        """Register a new user"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            password_hash = self.hash_password(password)
            cursor.execute(
                "INSERT INTO users (username, email, password_hash) VALUES (?, ?, ?)",
                (username, email, password_hash)
            )
            
            # Get the user ID to create default settings
            user_id = cursor.lastrowid
            
            # Create default settings for the user
            cursor.execute(
                "INSERT INTO settings (user_id, theme, animations_enabled) VALUES (?, ?, ?)",
                (user_id, 'deep_forest', 1)
            )
            
            conn.commit()
            conn.close()
            return True
        except sqlite3.IntegrityError:
            # Username or email already exists
            return False
    
    def authenticate_user(self, username_or_email, password):
        """Authenticate user credentials"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        password_hash = self.hash_password(password)
        
        cursor.execute('''
            SELECT id, username, email 
            FROM users 
            WHERE (username = ? OR email = ?) AND password_hash = ?
        ''', (username_or_email, username_or_email, password_hash))
        
        result = cursor.fetchone()
        conn.close()
        
        if result:
            return {'id': result[0], 'username': result[1], 'email': result[2]}
        return None
    
    def get_user_settings(self, user_id):
        """Get user settings from database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("SELECT theme, animations_enabled, font_size FROM settings WHERE user_id = ?", (user_id,))
        result = cursor.fetchone()
        conn.close()
        
        if result:
            return {
                'theme': result[0],
                'animations_enabled': bool(result[1]),
                'font_size': result[2]
            }
        return None
    
    def update_user_settings(self, user_id, **settings):
        """Update user settings in database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Build dynamic update query
        set_clause = []
        values = []
        for key, value in settings.items():
            set_clause.append(f"{key} = ?")
            values.append(value)
        
        values.append(user_id)
        query = f"UPDATE settings SET {', '.join(set_clause)} WHERE user_id = ?"
        
        cursor.execute(query, values)
        conn.commit()
        conn.close()
    
    def save_chat_message(self, user_id, message, response):
        """Save chat message to history"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute(
            "INSERT INTO chat_history (user_id, message, response) VALUES (?, ?, ?)",
            (user_id, message, response)
        )
        
        conn.commit()
        conn.close()
    
    def get_chat_history(self, user_id):
        """Retrieve chat history for a user"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute(
            "SELECT message, response, timestamp FROM chat_history WHERE user_id = ? ORDER BY timestamp ASC",
            (user_id,)
        )
        
        results = cursor.fetchall()
        conn.close()
        
        return [{'message': r[0], 'response': r[1], 'timestamp': r[2]} for r in results]