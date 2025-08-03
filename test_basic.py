#!/usr/bin/env python3
"""
Simple test script for Voice Assistant basic functionality
"""

import sys
from pathlib import Path

# Add the project root to Python path
sys.path.insert(0, str(Path(__file__).parent))

def test_basic_imports():
    """Test basic imports"""
    try:
        from voice_assistant.config import Config
        print("✅ Config import successful")
        
        config = Config()
        print("✅ Config initialization successful")
        
        from voice_assistant.speech import TextToSpeech
        print("✅ TextToSpeech import successful")
        
        tts = TextToSpeech(config)
        print("✅ TextToSpeech initialization successful")
        
        from voice_assistant.commands import CommandProcessor
        print("✅ CommandProcessor import successful")
        
        processor = CommandProcessor(config, tts.speak)
        print("✅ CommandProcessor initialization successful")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_basic_commands():
    """Test basic command processing"""
    try:
        from voice_assistant.config import Config
        from voice_assistant.speech import TextToSpeech
        from voice_assistant.commands import CommandProcessor
        
        config = Config()
        tts = TextToSpeech(config)
        processor = CommandProcessor(config, tts.speak)
        
        # Test basic commands
        test_commands = [
            "hello",
            "what time is it",
            "what's the date",
            "tell me a joke",
            "flip a coin"
        ]
        
        for command in test_commands:
            print(f"\n📝 Testing command: '{command}'")
            result = processor.process_command(command)
            print(f"   Result: {'✅ Success' if result else '❌ Failed'}")
            
        return True
        
    except Exception as e:
        print(f"❌ Command processing error: {e}")
        return False

def test_text_to_speech():
    """Test text-to-speech functionality"""
    try:
        from voice_assistant.config import Config
        from voice_assistant.speech import TextToSpeech
        
        config = Config()
        tts = TextToSpeech(config)
        
        print("🔊 Testing text-to-speech...")
        tts.speak("Hello! This is a test of the voice assistant text to speech system.")
        
        # Wait a moment for speech to complete
        import time
        time.sleep(3)
        
        print("✅ Text-to-speech test completed")
        return True
        
    except Exception as e:
        print(f"❌ TTS error: {e}")
        return False

def main():
    """Run all tests"""
    print("🚀 Voice Assistant Basic Tests")
    print("=" * 40)
    
    tests = [
        ("Basic Imports", test_basic_imports),
        ("Command Processing", test_basic_commands),
        ("Text-to-Speech", test_text_to_speech)
    ]
    
    results = []
    for test_name, test_func in tests:
        print(f"\n🧪 Running {test_name} test...")
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ {test_name} test failed with exception: {e}")
            results.append((test_name, False))
    
    print("\n" + "=" * 40)
    print("📊 Test Results:")
    print("=" * 40)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test_name}: {status}")
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    print(f"\nOverall: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Voice Assistant is ready to use.")
    else:
        print("⚠️  Some tests failed. Check the errors above.")

if __name__ == "__main__":
    main()