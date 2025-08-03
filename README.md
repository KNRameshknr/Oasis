# Voice Assistant 🎤🤖

A comprehensive voice-controlled assistant built in Python that can perform various tasks through natural language voice commands. This project includes both beginner-friendly basic features and advanced capabilities for more complex interactions.

## Features

### 🌟 Beginner Features
- **Voice Recognition**: Responds to wake word and voice commands
- **Basic Conversations**: Greetings, time, date, and casual interactions
- **Text-to-Speech**: Natural voice responses
- **Web Search**: Search the internet and open results
- **Entertainment**: Tell jokes, flip coins, and more

### 🚀 Advanced Features
- **Weather Updates**: Get current weather information
- **Email Integration**: Send emails via voice commands
- **Reminders System**: Set and manage voice reminders
- **Smart Home Control**: Control smart devices (configurable)
- **Natural Language Processing**: Advanced command understanding
- **Customizable Commands**: Add your own voice commands
- **Multiple TTS Voices**: Choose from available system voices

## Installation

### Prerequisites
- Python 3.7 or higher
- Microphone and speakers/headphones
- Internet connection for web features

### Setup Instructions

1. **Clone or download the project**
   ```bash
   git clone <repository-url>
   cd voice-assistant
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Install system dependencies** (Linux/Ubuntu)
   ```bash
   sudo apt-get install portaudio19-dev python3-pyaudio
   sudo apt-get install espeak espeak-data libespeak1 libespeak-dev
   ```

4. **Configure API keys** (optional, for advanced features)
   ```bash
   cp .env.example .env
   # Edit .env with your API keys
   ```

5. **Test the installation**
   ```bash
   python main.py --demo
   ```

## Usage

### Basic Usage

**Start the voice assistant:**
```bash
python main.py
```

**Test specific commands:**
```bash
python main.py --test-command "hello"
python main.py --test-command "what time is it"
```

**Run demo mode:**
```bash
python main.py --demo
```

**List available voices:**
```bash
python main.py --list-voices
```

### Voice Commands

#### Basic Commands
- **"Hey Aria"** - Wake word to activate the assistant
- **"Hello"** / **"Hi"** - Greet the assistant
- **"What time is it?"** - Get current time
- **"What's the date?"** - Get current date
- **"How are you?"** - Casual conversation
- **"What's your name?"** - Learn about the assistant

#### Search and Information
- **"Search for [topic]"** - Search the web
- **"Google [query]"** - Perform Google search
- **"Look up [information]"** - Find information online
- **"What's the weather?"** - Get weather updates (requires API key)

#### Entertainment
- **"Tell me a joke"** - Hear a random joke
- **"Flip a coin"** - Get heads or tails
- **"Help"** - List available commands

#### System Commands
- **"Stop"** / **"Exit"** / **"Goodbye"** - Shut down the assistant

### Configuration

The voice assistant can be customized through the `config.yaml` file:

```yaml
voice_assistant:
  name: "Aria"                    # Assistant's name
  wake_word: "hey aria"           # Wake word phrase
  language: "en-US"               # Recognition language
  
  # Enable/disable features
  features:
    basic_commands: true
    web_search: true
    weather: true
    email: false
    reminders: true
    smart_home: false
    advanced_nlp: true
```

### API Keys Setup

For advanced features, you'll need API keys:

1. **OpenWeather API** (for weather):
   - Sign up at [OpenWeatherMap](https://openweathermap.org/api)
   - Add your API key to `.env`: `OPENWEATHER_API_KEY=your_key_here`

2. **OpenAI API** (for advanced NLP):
   - Get API key from [OpenAI](https://platform.openai.com/)
   - Add to `.env`: `OPENAI_API_KEY=your_key_here`

3. **Gmail** (for email features):
   - Enable 2-factor authentication
   - Generate app password
   - Add to `.env`: `GMAIL_EMAIL=your_email@gmail.com` and `GMAIL_APP_PASSWORD=your_app_password`

## Project Structure

```
voice-assistant/
├── voice_assistant/          # Main package
│   ├── __init__.py          # Package initialization
│   ├── core.py              # Main VoiceAssistant class
│   ├── speech.py            # Speech recognition & TTS
│   ├── commands.py          # Command processing
│   └── config.py            # Configuration management
├── main.py                  # Entry point
├── config.yaml              # Configuration file
├── requirements.txt         # Python dependencies
├── .env.example            # Environment variables template
└── README.md               # This file
```

## Development

### Adding Custom Commands

To add new voice commands, edit `voice_assistant/commands.py`:

```python
# Add to command_patterns dictionary
r'your.*pattern.*here': self._handle_your_command,

# Add handler method
def _handle_your_command(self, command: str, match) -> bool:
    """Handle your custom command"""
    self.speak("Your custom response here")
    return True
```

### Testing

Run tests with different commands:
```bash
python main.py --test-command "your test command here"
```

### Logging

Logs are saved to `voice_assistant.log` and displayed in the console.

## Troubleshooting

### Common Issues

1. **Microphone not working**
   - Check microphone permissions
   - Test with: `python -c "import speech_recognition as sr; print(sr.Microphone.list_microphone_names())"`

2. **TTS not working**
   - Install system TTS engines: `sudo apt-get install espeak`
   - Check available voices: `python main.py --list-voices`

3. **Dependencies issues**
   - Try: `pip install --upgrade pip`
   - Install system packages: `sudo apt-get install python3-dev`

4. **PyAudio installation fails**
   - Linux: `sudo apt-get install portaudio19-dev`
   - macOS: `brew install portaudio`
   - Windows: Download PyAudio wheel from [here](https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyaudio)

### Performance Tips

- Run in a quiet environment for better recognition
- Speak clearly and at moderate pace
- Calibrate microphone when prompted
- Use a good quality microphone for best results

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Built with Python's `speech_recognition` library
- Uses `pyttsx3` for text-to-speech
- Integrates with various APIs for extended functionality
- Inspired by modern voice assistants like Alexa and Google Assistant

---

**Happy voice commanding! 🎤✨**
