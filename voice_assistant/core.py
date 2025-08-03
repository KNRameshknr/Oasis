"""
Core Voice Assistant class that orchestrates all components
"""

import logging
import threading
import time
from typing import Optional

from .config import Config
from .speech import SpeechRecognizer, TextToSpeech
from .commands import CommandProcessor

class VoiceAssistant:
    """Main Voice Assistant class"""
    
    def __init__(self, config_file: str = "config.yaml"):
        # Initialize configuration
        self.config = Config(config_file)
        
        # Set up logging
        self._setup_logging()
        self.logger = logging.getLogger(__name__)
        
        # Initialize components
        self.speech_recognizer = None
        self.text_to_speech = None
        self.command_processor = None
        
        # Control flags
        self.is_running = False
        self.is_listening = False
        
        # Initialize components
        self._initialize_components()
        
    def _setup_logging(self):
        """Set up logging configuration"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('voice_assistant.log'),
                logging.StreamHandler()
            ]
        )
        
    def _initialize_components(self):
        """Initialize all voice assistant components"""
        try:
            # Initialize text-to-speech first
            self.text_to_speech = TextToSpeech(self.config)
            
            # Initialize speech recognizer
            self.speech_recognizer = SpeechRecognizer(self.config)
            
            # Initialize command processor with TTS callback
            self.command_processor = CommandProcessor(
                self.config, 
                self.text_to_speech.speak
            )
            
            self.logger.info("Voice Assistant components initialized successfully")
            
        except Exception as e:
            self.logger.error(f"Failed to initialize components: {e}")
            raise
    
    def start(self):
        """Start the voice assistant"""
        if self.is_running:
            self.logger.warning("Voice Assistant is already running")
            return
            
        self.is_running = True
        self.logger.info("Starting Voice Assistant...")
        
        # Greet the user
        assistant_name = self.config.get('voice_assistant.name', 'Aria')
        self.text_to_speech.speak(f"Hello! I'm {assistant_name}, your voice assistant. I'm ready to help!")
        
        # Calibrate microphone
        try:
            self.speech_recognizer.calibrate_microphone()
        except Exception as e:
            self.logger.error(f"Microphone calibration failed: {e}")
            self.text_to_speech.speak("Warning: Microphone calibration failed. Voice recognition may not work optimally.")
        
        # Start main listening loop
        self._start_listening_loop()
    
    def stop(self):
        """Stop the voice assistant"""
        if not self.is_running:
            return
            
        self.is_running = False
        self.is_listening = False
        
        self.text_to_speech.speak("Voice Assistant shutting down. Goodbye!")
        self.logger.info("Voice Assistant stopped")
    
    def _start_listening_loop(self):
        """Main listening loop for wake word detection and command processing"""
        wake_word = self.config.get('voice_assistant.wake_word', 'hey aria')
        
        self.text_to_speech.speak(f"Say '{wake_word}' to get my attention, or say 'help' to see what I can do.")
        
        while self.is_running:
            try:
                # Listen for wake word
                if self.speech_recognizer.listen_for_wake_word(self._on_wake_word_detected):
                    # Wake word detected, now listen for command
                    self._process_voice_command()
                    
            except KeyboardInterrupt:
                self.logger.info("Received keyboard interrupt")
                break
            except Exception as e:
                self.logger.error(f"Error in listening loop: {e}")
                time.sleep(1)  # Brief pause before retrying
        
        self.stop()
    
    def _on_wake_word_detected(self, text: str):
        """Callback when wake word is detected"""
        self.logger.info(f"Wake word detected: {text}")
        self.text_to_speech.speak("Yes? How can I help you?", priority=True)
    
    def _process_voice_command(self):
        """Process a voice command after wake word detection"""
        try:
            # Listen for the actual command
            command = self.speech_recognizer.listen_for_command()
            
            if command:
                self.logger.info(f"Command received: {command}")
                
                # Process the command
                success = self.command_processor.process_command(command)
                
                if not success:
                    self.text_to_speech.speak("I'm sorry, I didn't understand that command.")
                    
                # Check if it was an exit command
                if any(word in command.lower() for word in ['stop', 'exit', 'quit', 'goodbye']):
                    self.is_running = False
                    
            else:
                self.text_to_speech.speak("I didn't catch that. Could you please repeat?")
                
        except Exception as e:
            self.logger.error(f"Error processing voice command: {e}")
            self.text_to_speech.speak("Sorry, I encountered an error while processing your command.")
    
    def process_text_command(self, command: str) -> bool:
        """Process a text command directly (useful for testing)"""
        if not command:
            return False
            
        self.logger.info(f"Processing text command: {command}")
        return self.command_processor.process_command(command)
    
    def get_status(self) -> dict:
        """Get current status of the voice assistant"""
        return {
            'is_running': self.is_running,
            'is_listening': self.is_listening,
            'is_speaking': self.text_to_speech.is_busy() if self.text_to_speech else False,
            'assistant_name': self.config.get('voice_assistant.name', 'Aria'),
            'wake_word': self.config.get('voice_assistant.wake_word', 'hey aria'),
            'features_enabled': {
                'basic_commands': self.config.is_feature_enabled('basic_commands'),
                'web_search': self.config.is_feature_enabled('web_search'),
                'weather': self.config.is_feature_enabled('weather'),
                'email': self.config.is_feature_enabled('email'),
                'reminders': self.config.is_feature_enabled('reminders'),
                'smart_home': self.config.is_feature_enabled('smart_home'),
                'advanced_nlp': self.config.is_feature_enabled('advanced_nlp'),
            }
        }
    
    def update_config(self, key: str, value):
        """Update configuration value"""
        self.config.set(key, value)
        self.config.save()
        self.logger.info(f"Configuration updated: {key} = {value}")
    
    def get_available_voices(self):
        """Get available TTS voices"""
        if self.text_to_speech:
            return self.text_to_speech.get_available_voices()
        return []
    
    def set_voice(self, voice_id: str):
        """Set TTS voice"""
        if self.text_to_speech:
            return self.text_to_speech.set_voice(voice_id)
        return False