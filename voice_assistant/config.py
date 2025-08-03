"""
Configuration management for the Voice Assistant
"""

import os
import yaml
from pathlib import Path
from dotenv import load_dotenv
from typing import Dict, Any, Optional

class Config:
    """Configuration manager for the voice assistant"""
    
    def __init__(self, config_file: str = "config.yaml"):
        self.config_file = config_file
        self.config_data = {}
        self._load_config()
        self._load_env_variables()
    
    def _load_config(self):
        """Load configuration from YAML file"""
        config_path = Path(self.config_file)
        if config_path.exists():
            with open(config_path, 'r') as file:
                self.config_data = yaml.safe_load(file)
        else:
            # Default configuration if file doesn't exist
            self.config_data = self._get_default_config()
    
    def _load_env_variables(self):
        """Load environment variables from .env file"""
        load_dotenv()
        
        # Update API keys from environment variables
        if 'voice_assistant' in self.config_data:
            api_keys = self.config_data['voice_assistant'].get('api_keys', {})
            api_keys['openweather'] = os.getenv('OPENWEATHER_API_KEY', '')
            api_keys['openai'] = os.getenv('OPENAI_API_KEY', '')
            api_keys['wolfram_alpha'] = os.getenv('WOLFRAM_ALPHA_API_KEY', '')
            api_keys['gmail_app_password'] = os.getenv('GMAIL_APP_PASSWORD', '')
    
    def _get_default_config(self) -> Dict[str, Any]:
        """Return default configuration"""
        return {
            'voice_assistant': {
                'name': 'Aria',
                'wake_word': 'hey aria',
                'language': 'en-US',
                'speech_recognition': {
                    'engine': 'google',
                    'timeout': 5,
                    'phrase_time_limit': 10,
                    'energy_threshold': 300,
                    'dynamic_energy_threshold': True
                },
                'text_to_speech': {
                    'engine': 'pyttsx3',
                    'voice': 'default',
                    'rate': 200,
                    'volume': 0.9
                },
                'features': {
                    'basic_commands': True,
                    'web_search': True,
                    'weather': True,
                    'email': True,
                    'reminders': True,
                    'smart_home': False,
                    'advanced_nlp': True
                },
                'api_keys': {},
                'privacy': {
                    'save_conversations': False,
                    'log_commands': True,
                    'encrypt_data': True
                }
            }
        }
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value using dot notation"""
        keys = key.split('.')
        value = self.config_data
        
        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default
        
        return value
    
    def set(self, key: str, value: Any):
        """Set configuration value using dot notation"""
        keys = key.split('.')
        config = self.config_data
        
        for k in keys[:-1]:
            if k not in config:
                config[k] = {}
            config = config[k]
        
        config[keys[-1]] = value
    
    def save(self):
        """Save configuration to file"""
        with open(self.config_file, 'w') as file:
            yaml.dump(self.config_data, file, default_flow_style=False)
    
    def is_feature_enabled(self, feature: str) -> bool:
        """Check if a feature is enabled"""
        return self.get(f'voice_assistant.features.{feature}', False)
    
    def get_api_key(self, service: str) -> Optional[str]:
        """Get API key for a service"""
        key = self.get(f'voice_assistant.api_keys.{service}')
        return key if key else None