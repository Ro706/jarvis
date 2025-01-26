import speech_recognition as sr
import google.generativeai as genai
from dotenv import load_dotenv
import pyttsx3
import os
load_dotenv()
class RecognizeSpeech:
    def __init__(self):
        self.r = sr.Recognizer()

    def listen(self):
        with sr.Microphone() as source:
            print("Listening...")
            self.r.pause_threshold = 1
            audio = self.r.listen(source)

        # Trying to recognize the speech
        try:
            print("Recognizing...")
            query = self.r.recognize_google(audio, language='en-in')
        except Exception as e:
            print(e)
            print("Say that again please...")
            return "None"
        return query.lower()
class speak:
    def __init__(self):
        self.engine = pyttsx3.init()
    def speak(self,text):
        # self.engine.setProperty('rate', 150)
        self.engine.setProperty('volume', 0.9)
        voices = self.engine.getProperty('voices')
        self.engine.setProperty('voice', voices[0].id)
        self.engine.say(text)
        self.engine.runAndWait()

class bard:
    def __init__(self):
        self.API_KEY = os.getenv("GEMINI_KEY")
        genai.configure(api_key=self.API_KEY)
    def chat(self,query):
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content(query)
        if response and hasattr(response, "text"):
            cleaned_response = response.text.replace("*", "").replace("**", "")
            print(cleaned_response)
            speak().speak(cleaned_response)
        else:
            speak().speak("Sorry, I could not understand that.")
            print("Sorry, I could not understand that.")

if __name__ == "__main__":
    speak().speak("Hello, I am jarvis. How can I help you?")
    while True:
        query = RecognizeSpeech().listen()
        if 'exit' in query:
            speak().speak("Goodbye, Have a nice day!")
            break
        # speak().speak(query)
        bard().chat(query)