"""
Speech Recognition and Text-to-Speech functionality
"""

import speech_recognition as sr
import pyttsx3
import threading
import queue
import logging
from typing import Optional, Callable, Dict, Any
from .config import Config

class SpeechRecognizer:
    """Handles speech recognition functionality"""
    
    def __init__(self, config: Config):
        self.config = config
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        self.is_listening = False
        self.wake_word = config.get('voice_assistant.wake_word', 'hey aria').lower()
        
        # Configure recognizer settings
        self._configure_recognizer()
        
        # Set up logging
        self.logger = logging.getLogger(__name__)
        
    def _configure_recognizer(self):
        """Configure the speech recognizer with settings from config"""
        self.recognizer.energy_threshold = self.config.get(
            'voice_assistant.speech_recognition.energy_threshold', 300
        )
        self.recognizer.dynamic_energy_threshold = self.config.get(
            'voice_assistant.speech_recognition.dynamic_energy_threshold', True
        )
        self.recognizer.pause_threshold = 0.8
        self.recognizer.phrase_threshold = 0.3
        
    def calibrate_microphone(self):
        """Calibrate microphone for ambient noise"""
        print("Calibrating microphone for ambient noise...")
        with self.microphone as source:
            self.recognizer.adjust_for_ambient_noise(source, duration=2)
        print("Microphone calibrated!")
        
    def listen_for_wake_word(self, callback: Callable[[str], None]) -> bool:
        """Listen continuously for the wake word"""
        try:
            with self.microphone as source:
                print(f"Listening for wake word: '{self.wake_word}'...")
                audio = self.recognizer.listen(
                    source, 
                    timeout=self.config.get('voice_assistant.speech_recognition.timeout', 5),
                    phrase_time_limit=self.config.get('voice_assistant.speech_recognition.phrase_time_limit', 10)
                )
                
            text = self._recognize_speech(audio)
            if text and self.wake_word in text.lower():
                callback(text)
                return True
                
        except sr.WaitTimeoutError:
            pass
        except sr.UnknownValueError:
            pass
        except sr.RequestError as e:
            self.logger.error(f"Speech recognition error: {e}")
            
        return False
        
    def listen_for_command(self) -> Optional[str]:
        """Listen for a voice command after wake word detection"""
        try:
            with self.microphone as source:
                print("Listening for command...")
                audio = self.recognizer.listen(
                    source,
                    timeout=self.config.get('voice_assistant.speech_recognition.timeout', 5),
                    phrase_time_limit=self.config.get('voice_assistant.speech_recognition.phrase_time_limit', 10)
                )
                
            return self._recognize_speech(audio)
            
        except sr.WaitTimeoutError:
            print("No command heard within timeout period")
            return None
        except sr.UnknownValueError:
            print("Could not understand the command")
            return None
        except sr.RequestError as e:
            self.logger.error(f"Speech recognition error: {e}")
            return None
            
    def _recognize_speech(self, audio) -> Optional[str]:
        """Recognize speech from audio using configured engine"""
        engine = self.config.get('voice_assistant.speech_recognition.engine', 'google')
        language = self.config.get('voice_assistant.language', 'en-US')
        
        try:
            if engine == 'google':
                return self.recognizer.recognize_google(audio, language=language)
            elif engine == 'sphinx':
                return self.recognizer.recognize_sphinx(audio)
            elif engine == 'wit':
                wit_key = self.config.get_api_key('wit')
                if wit_key:
                    return self.recognizer.recognize_wit(audio, key=wit_key)
            elif engine == 'bing':
                bing_key = self.config.get_api_key('bing')
                if bing_key:
                    return self.recognizer.recognize_bing(audio, key=bing_key)
            else:
                return self.recognizer.recognize_google(audio, language=language)
                
        except sr.UnknownValueError:
            return None
        except sr.RequestError as e:
            self.logger.error(f"Recognition service error: {e}")
            return None

class TextToSpeech:
    """Handles text-to-speech functionality"""
    
    def __init__(self, config: Config):
        self.config = config
        self.engine = pyttsx3.init()
        self.speech_queue = queue.Queue()
        self.is_speaking = False
        self._configure_engine()
        
        # Start speech thread
        self.speech_thread = threading.Thread(target=self._speech_worker, daemon=True)
        self.speech_thread.start()
        
    def _configure_engine(self):
        """Configure the TTS engine with settings from config"""
        # Set speech rate
        rate = self.config.get('voice_assistant.text_to_speech.rate', 200)
        self.engine.setProperty('rate', rate)
        
        # Set volume
        volume = self.config.get('voice_assistant.text_to_speech.volume', 0.9)
        self.engine.setProperty('volume', volume)
        
        # Set voice
        voice_preference = self.config.get('voice_assistant.text_to_speech.voice', 'default')
        voices = self.engine.getProperty('voices')
        
        if voice_preference == 'female' and len(voices) > 1:
            self.engine.setProperty('voice', voices[1].id)
        elif voice_preference == 'male' and len(voices) > 0:
            self.engine.setProperty('voice', voices[0].id)
        # 'default' uses system default
        
    def speak(self, text: str, priority: bool = False):
        """Add text to speech queue"""
        if priority:
            # Clear queue and add high priority message
            while not self.speech_queue.empty():
                try:
                    self.speech_queue.get_nowait()
                except queue.Empty:
                    break
                    
        self.speech_queue.put(text)
        
    def speak_immediately(self, text: str):
        """Speak text immediately, interrupting current speech"""
        self.stop_speaking()
        self.engine.say(text)
        self.engine.runAndWait()
        
    def _speech_worker(self):
        """Worker thread for processing speech queue"""
        while True:
            try:
                text = self.speech_queue.get(timeout=1)
                if text:
                    self.is_speaking = True
                    self.engine.say(text)
                    self.engine.runAndWait()
                    self.is_speaking = False
                    self.speech_queue.task_done()
            except queue.Empty:
                continue
            except Exception as e:
                logging.error(f"TTS error: {e}")
                self.is_speaking = False
                
    def stop_speaking(self):
        """Stop current speech"""
        if self.is_speaking:
            self.engine.stop()
            self.is_speaking = False
            
    def is_busy(self) -> bool:
        """Check if currently speaking"""
        return self.is_speaking or not self.speech_queue.empty()
        
    def get_available_voices(self) -> list:
        """Get list of available voices"""
        voices = self.engine.getProperty('voices')
        return [{'id': voice.id, 'name': voice.name, 'gender': getattr(voice, 'gender', 'unknown')} 
                for voice in voices] if voices else []
                
    def set_voice(self, voice_id: str):
        """Set voice by ID"""
        try:
            self.engine.setProperty('voice', voice_id)
            return True
        except Exception as e:
            logging.error(f"Failed to set voice {voice_id}: {e}")
            return False