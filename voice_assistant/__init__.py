"""
Voice Assistant - A comprehensive voice-controlled assistant
"""

__version__ = "1.0.0"
__author__ = "Voice Assistant Team"

from .core import VoiceAssistant
from .speech import SpeechRecognizer, TextToSpeech
from .commands import CommandProcessor
from .config import Config

__all__ = [
    "VoiceAssistant",
    "SpeechRecognizer", 
    "TextToSpeech",
    "CommandProcessor",
    "Config"
]