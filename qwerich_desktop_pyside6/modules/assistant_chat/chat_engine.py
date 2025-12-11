"""
Chat Engine for Qwerich Desktop Application
Handles natural language processing and response generation
"""

import difflib
import json
import random
from datetime import datetime


class ChatEngine:
    def __init__(self, responses_file="modules/assistant_chat/responses.json"):
        self.responses_file = responses_file
        self.responses = self.load_responses()
        self.command_patterns = self.create_command_patterns()
    
    def load_responses(self):
        """Load responses from JSON file or create default ones"""
        try:
            with open(self.responses_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            # Create default responses
            default_responses = {
                "greetings": {
                    "patterns": ["привет", "хай", "здравствуй", "добрый день", "hello", "hi"],
                    "responses": [
                        "Привет! Рад вас видеть!",
                        "Здравствуйте! Как я могу вам помочь?",
                        "Привет! У меня всё отлично, я готов помочь!",
                        "Хай! Что нового?"
                    ]
                },
                "weather": {
                    "patterns": ["погода", "какая погода", "что на улице", "температура"],
                    "responses": [
                        "Запрос к погодному сервису настроен не до конца",
                        "К сожалению, я не могу предоставить точную информацию о погоде",
                        "Сегодня хорошая погода для работы за компьютером!"
                    ]
                },
                "how_are_you": {
                    "patterns": ["как дела", "как жизнь", "что нового", "как настроение"],
                    "responses": [
                        "У меня всё отлично! Спасибо, что спросили!",
                        "Я чувствую себя великолепно! Готов помочь вам!",
                        "Всё в порядке! А как у вас дела?",
                        "Я всегда в отличном настроении, когда помогаю людям!"
                    ]
                },
                "abilities": {
                    "patterns": ["что ты умеешь", "расскажи о себе", "функции", "возможности"],
                    "responses": [
                        "Я могу общаться с вами, помогать в работе, показывать информацию о системе и многое другое!",
                        "Я - ваш виртуальный помощник Qwerich. Могу отвечать на вопросы, помогать с задачами и т.д.",
                        "Я умею общаться, предоставлять информацию, работать с системными данными и даже чатиться с другими пользователями!"
                    ]
                },
                "system_info": {
                    "patterns": ["система", "устройство", "информация о системе", "мои данные"],
                    "responses": [
                        "Для просмотра информации о системе перейдите в раздел 'Система' в главном меню",
                        "Вы можете увидеть всю информацию о вашем устройстве во вкладке 'Система'",
                        "Чтобы посмотреть системную информацию, откройте раздел 'Система'"
                    ]
                },
                "goodbye": {
                    "patterns": ["пока", "до встречи", "увидимся", "bye", "goodbye"],
                    "responses": [
                        "До встречи! Возвращайтесь скорее!",
                        "Пока! Надеюсь, я смог вам помочь!",
                        "Удачи! Заходите, когда понадобится помощь!",
                        "До скорой встречи!"
                    ]
                },
                "thank_you": {
                    "patterns": ["спасибо", "благодарю", "thanks", "thx"],
                    "responses": [
                        "Пожалуйста! Всегда рад помочь!",
                        "Не за что! Рад быть полезным!",
                        "Спасибо вам тоже! Всегда к вашим услугам!",
                        "Обращайтесь, если что-нибудь понадобится!"
                    ]
                }
            }
            
            # Save default responses to file
            with open(self.responses_file, 'w', encoding='utf-8') as f:
                json.dump(default_responses, f, ensure_ascii=False, indent=2)
            
            return default_responses
    
    def create_command_patterns(self):
        """Create a dictionary mapping patterns to their categories"""
        patterns = {}
        for category, data in self.responses.items():
            for pattern in data['patterns']:
                patterns[pattern.lower()] = category
        return patterns
    
    def find_best_match(self, user_input):
        """Find the best matching command category for user input"""
        user_input_lower = user_input.lower()
        
        # Direct match
        for pattern, category in self.command_patterns.items():
            if pattern in user_input_lower:
                return category
        
        # Fuzzy matching
        all_patterns = list(self.command_patterns.keys())
        matches = difflib.get_close_matches(user_input_lower, all_patterns, n=1, cutoff=0.6)
        
        if matches:
            return self.command_patterns[matches[0]]
        
        # Check for partial matches in the input
        for pattern, category in self.command_patterns.items():
            if pattern in user_input_lower:
                return category
        
        # No match found
        return None
    
    def generate_response(self, user_input):
        """Generate a response based on user input"""
        category = self.find_best_match(user_input)
        
        if category and category in self.responses:
            responses = self.responses[category]['responses']
            return random.choice(responses)
        else:
            # Generic response for unknown inputs
            generic_responses = [
                "Интересный вопрос! Могу ли я чем-то еще помочь?",
                "Я пока не знаю, как на это ответить. Но я учусь!",
                "Попробуйте переформулировать ваш запрос",
                "Могу ли я помочь вам с чем-то еще?",
                "Это интересно! Расскажите больше."
            ]
            return random.choice(generic_responses)
    
    def process_command(self, user_input, user_id=None):
        """Process user command and return response"""
        response = self.generate_response(user_input)
        
        # Optionally save to chat history if user_id is provided
        if user_id:
            import sys
            import os
            sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
            from database import Database  # Import here to avoid circular dependency
            db = Database()
            db.save_chat_message(user_id, user_input, response)
        
        return {
            'input': user_input,
            'response': response,
            'timestamp': datetime.now().isoformat(),
            'category': self.find_best_match(user_input) or 'unknown'
        }


# Example usage
if __name__ == "__main__":
    engine = ChatEngine()
    
    # Test some inputs
    test_inputs = [
        "Привет, как дела?",
        "Какая погода сегодня?",
        "Расскажи о себе",
        "Что ты умеешь?",
        "Пока!"
    ]
    
    for inp in test_inputs:
        result = engine.process_command(inp)
        print(f"Input: {inp}")
        print(f"Response: {result['response']}")
        print(f"Category: {result['category']}")
        print("-" * 40)