#!/usr/bin/env python3
"""
Voice Assistant - Main Entry Point

A comprehensive voice assistant with both beginner and advanced features.
Supports speech recognition, text-to-speech, web search, weather updates,
reminders, and more.
"""

import sys
import argparse
import signal
from pathlib import Path

# Add the project root to Python path
sys.path.insert(0, str(Path(__file__).parent))

from voice_assistant import VoiceAssistant

def signal_handler(signum, frame):
    """Handle Ctrl+C gracefully"""
    print("\nShutting down voice assistant...")
    sys.exit(0)

def main():
    """Main function to run the voice assistant"""
    parser = argparse.ArgumentParser(description="Voice Assistant - Your AI-powered voice companion")
    parser.add_argument(
        "--config", 
        default="config.yaml",
        help="Path to configuration file (default: config.yaml)"
    )
    parser.add_argument(
        "--test-command",
        help="Test a specific command without voice input"
    )
    parser.add_argument(
        "--demo",
        action="store_true",
        help="Run in demo mode with sample commands"
    )
    parser.add_argument(
        "--list-voices",
        action="store_true",
        help="List available TTS voices and exit"
    )
    
    args = parser.parse_args()
    
    # Set up signal handler for graceful shutdown
    signal.signal(signal.SIGINT, signal_handler)
    
    try:
        # Initialize voice assistant
        print("Initializing Voice Assistant...")
        assistant = VoiceAssistant(args.config)
        
        # List voices if requested
        if args.list_voices:
            voices = assistant.get_available_voices()
            print("\nAvailable TTS Voices:")
            print("-" * 40)
            for voice in voices:
                print(f"ID: {voice['id']}")
                print(f"Name: {voice['name']}")
                print(f"Gender: {voice.get('gender', 'Unknown')}")
                print("-" * 40)
            return
        
        # Test command mode
        if args.test_command:
            print(f"Testing command: {args.test_command}")
            success = assistant.process_text_command(args.test_command)
            print(f"Command processed: {'Successfully' if success else 'Failed'}")
            return
        
        # Demo mode
        if args.demo:
            print("Running in demo mode...")
            demo_commands = [
                "hello",
                "what time is it",
                "what's the date today",
                "tell me a joke",
                "flip a coin",
                "help"
            ]
            
            for command in demo_commands:
                print(f"\nDemo command: {command}")
                assistant.process_text_command(command)
                input("Press Enter to continue...")
            
            return
        
        # Normal operation - start voice assistant
        print("Voice Assistant initialized successfully!")
        print("Starting voice recognition...")
        print("Press Ctrl+C to exit")
        
        assistant.start()
        
    except KeyboardInterrupt:
        print("\nShutting down voice assistant...")
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()