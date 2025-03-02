# Jarvis
## Voice-Controlled AI Assistant

This project is a voice-controlled AI assistant designed to execute basic terminal commands, manage files and directories, fetch system information, tell jokes, report weather and news, send emails, and even open websites or play games. The assistant is built with Python and uses speech recognition, text-to-speech, and AI models to interact with the user.

## Features

- **Voice Recognition:** Uses Google’s speech recognition for user input.
- **Text-to-Speech:** Provides spoken feedback using `pyttsx3`.
- **AI-Powered Responses:** Uses Gemini AI for answering general queries.
- **File Management:** Create, read, append, delete files and directories.
- **System Information:** Fetches RAM and CPU details.
- **Web Browsing:** Opens popular websites like YouTube, Google, GitHub, etc.
- **Entertainment:** Tells jokes and plays games.
- **Weather and News:** Provides current weather reports and news updates.
- **Email Integration:** Sends emails directly via voice commands.

## Setup

1. Clone the repository.
2. Install required dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Create a `.env` file and add your Gemini API key:
   ```env
   GEMINI_KEY=your_api_key_here
   ```
4. Run the assistant:
   ```bash
   python main.py
   ```

## Usage

Once running, the assistant will listen for voice commands. Examples include:

- "Open YouTube"
- "Create file example.txt with content Hello World"
- "Read file example.txt"
- "What’s the weather today?"
- "Tell me a joke"
- "Play music"
- "Send mail"
- "Play a game"

## File Structure

- `core/` – System utilities (RAM info, CPU info, weather, news, email, greetings)
- `game/` – Games directory
- `main.py` – Entry point of the application

## Dependencies

- `pyttsx3`
- `speech_recognition`
- `pyjokes`
- `google-generativeai`
- `dotenv`
- `webbrowser`
- `os`, `signal`

## Exit

To exit the assistant, simply say:

```
Goodbye
Exit
```

Enjoy your smart and helpful AI assistant!

