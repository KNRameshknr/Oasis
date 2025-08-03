#!/usr/bin/env python3
"""
Text-only demo of Voice Assistant capabilities
This demo shows what the assistant can do without requiring audio hardware
"""

import sys
from pathlib import Path

# Add the project root to Python path
sys.path.insert(0, str(Path(__file__).parent))

def main():
    """Run text-only demo"""
    print("🎤🤖 Voice Assistant - Text Demo")
    print("=" * 50)
    print("This demo shows the voice assistant's capabilities")
    print("without requiring audio hardware.\n")
    
    # Import components
    try:
        from voice_assistant.config import Config
        from voice_assistant.commands import CommandProcessor
        
        # Create a mock TTS function for demo
        def mock_speak(text):
            print(f"🔊 Assistant: {text}")
        
        config = Config()
        processor = CommandProcessor(config, mock_speak)
        
        print("✅ Voice Assistant initialized successfully!\n")
        
    except Exception as e:
        print(f"❌ Error initializing: {e}")
        return
    
    # Demo commands
    demo_commands = [
        ("Greeting", "hello"),
        ("Time Query", "what time is it"),
        ("Date Query", "what's the date today"),
        ("Personal Question", "how are you"),
        ("Identity Question", "what's your name"),
        ("Entertainment", "tell me a joke"),
        ("Random Fun", "flip a coin"),
        ("Web Search", "search for Python programming"),
        ("Weather Query", "what's the weather"),
        ("Reminder", "remind me to buy groceries"),
        ("Help", "help"),
        ("Goodbye", "goodbye")
    ]
    
    print("🚀 Running Demo Commands:")
    print("-" * 30)
    
    for category, command in demo_commands:
        print(f"\n📝 {category}: '{command}'")
        print("👤 User:", command)
        
        try:
            success = processor.process_command(command)
            if not success:
                print("❌ Command not recognized")
        except Exception as e:
            print(f"❌ Error: {e}")
        
        print()  # Empty line for readability
    
    print("=" * 50)
    print("🎉 Demo Complete!")
    print("\nFeatures demonstrated:")
    print("✅ Basic conversation and greetings")
    print("✅ Time and date queries") 
    print("✅ Personal questions and identity")
    print("✅ Entertainment (jokes, coin flips)")
    print("✅ Web search capabilities")
    print("✅ Weather queries (requires API key)")
    print("✅ Reminder system")
    print("✅ Help system")
    print("✅ Graceful exits")
    
    print("\n🔧 To use with voice:")
    print("1. Connect microphone and speakers")
    print("2. Run: python3 main.py")
    print("3. Say 'Hey Aria' to activate")
    print("4. Speak your commands naturally")
    
    print("\n📖 For more information, see README.md")

if __name__ == "__main__":
    main()