"""
Command processing and handling for the Voice Assistant
"""

import re
import datetime
import webbrowser
import requests
import json
import smtplib
import schedule
import time
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Dict, Any, Optional, List, Callable
from googlesearch import search
import logging

from .config import Config

class CommandProcessor:
    """Processes and executes voice commands"""
    
    def __init__(self, config: Config, tts_callback: Callable[[str], None]):
        self.config = config
        self.speak = tts_callback
        self.logger = logging.getLogger(__name__)
        
        # Command patterns and handlers
        self.command_patterns = {
            # Basic commands
            r'hello|hi|hey': self._handle_greeting,
            r'what.*time|time.*is': self._handle_time,
            r'what.*date|date.*is|today': self._handle_date,
            r'how.*are.*you|how.*doing': self._handle_how_are_you,
            r'what.*your.*name|who.*are.*you': self._handle_name,
            
            # Web search
            r'search.*for (.*)|look.*up (.*)|find (.*)|google (.*)': self._handle_web_search,
            
            # Weather
            r'weather.*in (.*)|weather.*for (.*)|.*weather.*': self._handle_weather,
            
            # Email
            r'send.*email.*to (.*)|email (.*)': self._handle_email,
            
            # Reminders
            r'remind.*me.*to (.*)|set.*reminder.*for (.*)': self._handle_reminder,
            
            # System commands
            r'stop|exit|quit|goodbye': self._handle_exit,
            r'help|what.*can.*you.*do': self._handle_help,
            
            # Fun commands
            r'tell.*joke|joke': self._handle_joke,
            r'flip.*coin|coin.*flip': self._handle_coin_flip,
        }
        
        # Initialize reminders list
        self.reminders = []
        
    def process_command(self, command: str) -> bool:
        """Process a voice command and execute appropriate action"""
        if not command:
            return False
            
        command = command.lower().strip()
        self.logger.info(f"Processing command: {command}")
        
        # Try to match command patterns
        for pattern, handler in self.command_patterns.items():
            match = re.search(pattern, command)
            if match:
                try:
                    return handler(command, match)
                except Exception as e:
                    self.logger.error(f"Error executing command '{command}': {e}")
                    self.speak("Sorry, I encountered an error while processing that command.")
                    return False
        
        # If no pattern matches, try advanced NLP if enabled
        if self.config.is_feature_enabled('advanced_nlp'):
            return self._handle_advanced_nlp(command)
        else:
            self.speak("I'm not sure how to help with that. Try saying 'help' to see what I can do.")
            return False
    
    def _handle_greeting(self, command: str, match) -> bool:
        """Handle greeting commands"""
        greetings = [
            "Hello! How can I help you today?",
            "Hi there! What can I do for you?",
            "Hey! I'm here to assist you.",
            "Hello! Ready to help with whatever you need."
        ]
        import random
        self.speak(random.choice(greetings))
        return True
    
    def _handle_time(self, command: str, match) -> bool:
        """Handle time-related commands"""
        now = datetime.datetime.now()
        time_str = now.strftime("%I:%M %p")
        self.speak(f"The current time is {time_str}")
        return True
    
    def _handle_date(self, command: str, match) -> bool:
        """Handle date-related commands"""
        now = datetime.datetime.now()
        date_str = now.strftime("%A, %B %d, %Y")
        self.speak(f"Today is {date_str}")
        return True
    
    def _handle_how_are_you(self, command: str, match) -> bool:
        """Handle how are you questions"""
        responses = [
            "I'm doing great, thank you for asking!",
            "I'm functioning perfectly and ready to help!",
            "I'm excellent! How are you doing?",
            "All systems are running smoothly, thanks!"
        ]
        import random
        self.speak(random.choice(responses))
        return True
    
    def _handle_name(self, command: str, match) -> bool:
        """Handle name/identity questions"""
        name = self.config.get('voice_assistant.name', 'Aria')
        self.speak(f"I'm {name}, your voice assistant. I'm here to help you with various tasks!")
        return True
    
    def _handle_web_search(self, command: str, match) -> bool:
        """Handle web search commands"""
        if not self.config.is_feature_enabled('web_search'):
            self.speak("Web search is currently disabled.")
            return False
            
        # Extract search query from the match groups
        query = None
        for group in match.groups():
            if group:
                query = group.strip()
                break
                
        if not query:
            self.speak("What would you like me to search for?")
            return False
        
        try:
            self.speak(f"Searching for {query}")
            
            # Perform Google search
            search_results = list(search(query))
            
            if search_results:
                self.speak(f"I found some results for {query}. Here are the top results:")
                for i, url in enumerate(search_results[:2], 1):
                    self.speak(f"Result {i}: Opening in browser")
                    webbrowser.open(url)
                    time.sleep(1)  # Brief pause between opening tabs
            else:
                self.speak(f"I couldn't find any results for {query}")
                
        except Exception as e:
            self.logger.error(f"Web search error: {e}")
            self.speak("Sorry, I encountered an error while searching the web.")
            
        return True
    
    def _handle_weather(self, command: str, match) -> bool:
        """Handle weather-related commands"""
        if not self.config.is_feature_enabled('weather'):
            self.speak("Weather updates are currently disabled.")
            return False
            
        api_key = self.config.get_api_key('openweather')
        if not api_key:
            self.speak("Weather API key is not configured.")
            return False
        
        # Extract location from command or use default
        location = "current location"
        location_match = re.search(r'in (.*)|for (.*)', command)
        if location_match:
            for group in location_match.groups():
                if group:
                    location = group.strip()
                    break
        
        try:
            # For demo purposes, we'll use a default location
            if location == "current location":
                location = "New York"
                
            url = f"http://api.openweathermap.org/data/2.5/weather?q={location}&appid={api_key}&units=metric"
            response = requests.get(url, timeout=5)
            
            if response.status_code == 200:
                data = response.json()
                temp = data['main']['temp']
                description = data['weather'][0]['description']
                self.speak(f"The weather in {location} is {description} with a temperature of {temp} degrees Celsius")
            else:
                self.speak(f"Sorry, I couldn't get weather information for {location}")
                
        except Exception as e:
            self.logger.error(f"Weather API error: {e}")
            self.speak("Sorry, I couldn't retrieve weather information right now.")
            
        return True
    
    def _handle_email(self, command: str, match) -> bool:
        """Handle email sending commands"""
        if not self.config.is_feature_enabled('email'):
            self.speak("Email functionality is currently disabled.")
            return False
            
        self.speak("Email functionality requires additional setup. Please configure your email settings in the configuration file.")
        return True
    
    def _handle_reminder(self, command: str, match) -> bool:
        """Handle reminder commands"""
        if not self.config.is_feature_enabled('reminders'):
            self.speak("Reminders are currently disabled.")
            return False
            
        # Extract reminder text
        reminder_text = None
        for group in match.groups():
            if group:
                reminder_text = group.strip()
                break
                
        if reminder_text:
            # For demo, we'll just acknowledge the reminder
            self.speak(f"I'll remind you to {reminder_text}. Note: Advanced scheduling requires additional setup.")
            self.reminders.append({
                'text': reminder_text,
                'created': datetime.datetime.now(),
                'status': 'active'
            })
        else:
            self.speak("What would you like me to remind you about?")
            
        return True
    
    def _handle_exit(self, command: str, match) -> bool:
        """Handle exit commands"""
        goodbyes = [
            "Goodbye! Have a great day!",
            "See you later! Take care!",
            "Bye! Feel free to call me anytime!",
            "Farewell! It was nice talking with you!"
        ]
        import random
        self.speak(random.choice(goodbyes))
        return True
    
    def _handle_help(self, command: str, match) -> bool:
        """Handle help commands"""
        help_text = """Here's what I can help you with:
        - Basic greetings and conversation
        - Tell you the current time and date
        - Search the web for information
        - Provide weather updates
        - Set reminders
        - Tell jokes and flip coins
        - And much more! Just ask me naturally."""
        
        self.speak(help_text)
        return True
    
    def _handle_joke(self, command: str, match) -> bool:
        """Handle joke requests"""
        jokes = [
            "Why don't scientists trust atoms? Because they make up everything!",
            "Why did the scarecrow win an award? He was outstanding in his field!",
            "Why don't eggs tell jokes? They'd crack each other up!",
            "What do you call a fake noodle? An impasta!",
            "Why did the math book look so sad? Because it was full of problems!"
        ]
        import random
        self.speak(random.choice(jokes))
        return True
    
    def _handle_coin_flip(self, command: str, match) -> bool:
        """Handle coin flip requests"""
        import random
        result = "heads" if random.random() < 0.5 else "tails"
        self.speak(f"I flipped a coin and got {result}!")
        return True
    
    def _handle_advanced_nlp(self, command: str) -> bool:
        """Handle commands using advanced NLP (placeholder for OpenAI integration)"""
        # This would integrate with OpenAI or other NLP services
        self.speak("I'm still learning to understand that. Could you try rephrasing your request?")
        return False