from datetime import time
import pyjokes
import speech_recognition as sr
import google.generativeai as genai
from dotenv import load_dotenv
from core.PhotoCaptureApp import create_gui
from core.ram_info import RamInfo
from core.cpu_info import cpu_info
from core.weather import tellmeTodaysWeather
from core.news import news_report
from core.wishme import wish_me
from core.mail import send_mail
from game.game1 import game
import webbrowser
import pyttsx3
import os
import signal
load_dotenv()

def handler(sig, frame):
    print("Goodbye, Have a nice day!")
    exit(0)

signal.signal(signal.SIGINT, handler)

class FileManager:
    def __init__(self, base_path="."):
        self.base_path = os.path.abspath(base_path)

    def create_file(self, filename, content=""):
        path = os.path.join(self.base_path, filename)
        with open(path, "w") as file:
            file.write(content)
        return f"File created: {path}"

    def read_file(self, filename):
        path = os.path.join(self.base_path, filename)
        if os.path.exists(path):
            with open(path, "r") as file:
                return file.read()
        else:
            return f"File not found: {path}"

    def append_to_file(self, filename, content):
        path = os.path.join(self.base_path, filename)
        if os.path.exists(path):
            with open(path, "a") as file:
                file.write(content)
            return f"Content appended to: {path}"
        else:
            return f"File not found: {path}"

    def delete_file(self, filename):
        path = os.path.join(self.base_path, filename)
        if os.path.exists(path):
            os.remove(path)
            return f"File deleted: {path}"
        else:
            return f"File not found: {path}"

    def create_directory(self, dirname):
        path = os.path.join(self.base_path, dirname)
        os.makedirs(path, exist_ok=True)
        return f"Directory created: {path}"

    def delete_directory(self, dirname):
        path = os.path.join(self.base_path, dirname)
        if os.path.exists(path) and os.path.isdir(path):
            try:
                os.rmdir(path)
                return f"Directory deleted: {path}"
            except OSError as e:
                return f"Error: Could not delete {path}. The directory might not be empty."
        else:
            return f"Directory not found: {path}"

    def add_folder(self, foldername):
        path = os.path.join(self.base_path, foldername)
        os.makedirs(path, exist_ok=True)
        return f"Folder added: {path}"

    def delete_folder(self, foldername):
        path = os.path.join(self.base_path, foldername)
        if os.path.exists(path) and os.path.isdir(path):
            try:
                os.rmdir(path)
                return f"Folder deleted: {path}"
            except OSError as e:
                return f"Error: Could not delete {path}. The folder might not be empty."
        else:
            return f"Folder not found: {path}"

    def search_file(self, filename, start_path="."):
        start_path = os.path.abspath(start_path)
        for root, dirs, files in os.walk(start_path):
            if filename in files:
                return f"File found: {os.path.join(root, filename)}"
        return f"File not found: {filename}"

    def list_directory(self, dirname="."):
        path = os.path.join(self.base_path, dirname)
        if os.path.exists(path) and os.path.isdir(path):
            files = os.listdir(path)
            if files:
                return f"Contents of {path}:\n" + "\n".join(files)
            else:
                return f"Directory {path} is empty"
        else:
            return f"Directory not found: {path}"

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
            print(f"User said: {query}")
        except Exception as e:
            print(e)
            print("Say that again please...")
            return "None"
        return query.lower()

class Speak:
    def __init__(self):
        self.engine = pyttsx3.init()
        self.engine.setProperty('volume', 0.9)
        voices = self.engine.getProperty('voices')
        self.engine.setProperty('voice', voices[0].id)
        
    def speak(self, text):
        print(f"Jarvis: {text}")
        self.engine.say(text)
        self.engine.runAndWait()

class Bard:
    def __init__(self):
        genai.configure(api_key=os.getenv("GEMINI_KEY"))
        self.model = genai.GenerativeModel('gemini-1.5-flash')
        
    def chat(self, query):
        try:
            query = f"Your name is Jarvis, our intelligent and reliable personal assistant try if possible give each reponce under 2 to 3 line only. {query}"
            response = self.model.generate_content(query)
            
            if response and hasattr(response, "text"):
                cleaned_response = response.text.replace("*", "").replace("**", "")
                return cleaned_response
            else:
                return "Sorry, I could not understand that."
        except Exception as e:
            print(f"Error with Gemini API: {e}")
            return "Sorry, I encountered an error while processing your request."

def extract_command_parts(query):
    parts = query.split(' ', 1)
    command = parts[0]
    content = parts[1] if len(parts) > 1 else ""
    return command, content

def parse_file_command(query):
    # Parse more complex file commands
    parts = query.split()
    
    if len(parts) < 2:
        return None, None, None
    
    command = parts[0]
    filename = parts[-1]  # Assume the last word is the filename
    
    # For commands that need content, extract it
    content = ""
    if command == "create" or command == "append":
        # Find position of "with content" or similar phrase
        content_marker = query.find("with content")
        name_marker = query.find(filename)
        
        if content_marker != -1 and name_marker != -1:
            content = query[content_marker + len("with content"):name_marker].strip()
    
    return command, filename, content

def get_user_input(speaker, speech_recognizer, prompt):
    speaker.speak(prompt)
    user_input = speech_recognizer.listen()
    
    # Try again if recognition failed
    if user_input == "none":
        speaker.speak("I didn't catch that. Please try again.")
        user_input = speech_recognizer.listen()
    
    return user_input



'''
MAIN PROGRAM STARTS HERE
'''


if __name__ == "__main__":
    speaker = Speak()
    speech_recognizer = RecognizeSpeech()
    file_manager = FileManager()
    user_name = input("What's your name? ")
    wish_me(user_name)
    
    while True:
        query = speech_recognizer.listen()
        if query == "none":
            continue
            
        if 'exit' in query or 'goodbye' in query:
            speaker.speak("Goodbye, Have a nice day!")
            break
        elif 'open youtube' in query:
            speaker.speak("Opening Youtube")
            webbrowser.open("youtube.com")
        elif 'open google' in query:
            speaker.speak("Opening Google")
            query = query.replace("open google and search for", "")
            webbrowser.open(f"https://www.google.com/search?q={query}")
        elif 'open stackoverflow' in query:
            speaker.speak("Opening Stackoverflow")
            webbrowser.open("stackoverflow.com")
        elif 'open github' in query:
            speaker.speak("Opening Github")
            webbrowser.open("github.com")
        elif 'open facebook' in query:
            speaker.speak("Opening Facebook")
            webbrowser.open("facebook.com")
        elif 'open instagram' in query:
            speaker.speak("Opening Instagram")
            webbrowser.open("instagram.com")
        elif 'ram' in query:
            speaker.speak("Here are the RAM details:")
            ram_info = RamInfo().info()
            speaker.speak(ram_info)
        elif "play music" in query:
            os.system("spotify")   
        elif 'cpu' in query:
            cpu_details = cpu_info()
            speaker.speak("Here are the CPU details:")
            speaker.speak(cpu_details)
            
        elif 'weather' in query:
            speaker.speak("Here is the weather in Nagpur:")
            tellmeTodaysWeather()
        elif "joke" in query:
            # Jokes section: telling jokes
            joke = pyjokes.get_joke()
            print(joke)
            speaker.speak(joke)
        elif 'time' in query:
            speaker.speak("The current time is:")
            speaker.speak(time.ctime())
        # Interactive file management commands
        elif 'create file' in query or 'make file' in query:
                file_name = input("Please Enter file name : ")
                # subprocess.call(['echo. >', file_name])
                os.system(f"echo. > {file_name}")
                print("File created successfully")
                
        elif 'read file' in query:
            # Ask for file name if not provided
            if len(query.split("file")[-1].strip()) < 2:
                filename =input("Please Enter file name : ")
            else:
                filename = query.split("file")[-1].strip()
                
            if filename != "none":
                content = file_manager.read_file(filename)
                speaker.speak(f"Content of {filename}:")
                speaker.speak(content)
            else:
                speaker.speak("Sorry, I couldn't read the file without a name.")
            
        elif 'append to file' in query or 'add to file' in query:
            # Ask for file name if not provided
            if 'append to file' in query:
                parts = query.split("append to file")[-1].strip()
            else:
                parts = query.split("add to file")[-1].strip()
                
            if len(parts) < 2:
                filename = input("Which file would you like to append to?")
            else:
                filename = parts
                
            # Ask for content
            content = get_user_input(speaker, speech_recognizer, "What content should I append to the file?")
            
            if filename != "none" and content != "none":
                try:
                    result = file_manager.append_to_file(filename, content)
                    speaker.speak(result)
                except Exception as e:
                    speaker.speak(f"Error appending to file: {e}")
            else:
                speaker.speak("Sorry, I couldn't append to the file due to missing information.")
                
        elif 'delete file' in query or 'remove file' in query:
            # Ask for file name if not provided
            if len(query.split("file")[-1].strip()) < 2:
                filename = input("Enter file name : ")
            else:
                filename = query.split("file")[-1].strip()
                
            if filename != "none":
                # Confirm deletion
                confirmation = input(f"Are you sure you want to delete {filename}? Say yes to confirm.")
                if confirmation == "yes":
                    result = file_manager.delete_file(filename)
                    speaker.speak(result)
                else:
                    speaker.speak("File deletion cancelled.")
            else:
                speaker.speak("Sorry, I couldn't delete the file without a name.")
            
        elif 'create directory' in query or 'create folder' in query or 'add folder' in query:
            # Extract the directory name if provided
            if "directory" in query:
                dirname = query.split("directory")[-1].strip()
            else:
                dirname = query.split("folder")[-1].strip()
                
            # Ask for directory name if not provided
            if len(dirname) < 2:
                dirname = input( "What should I name the directory or folder?")
                
            if dirname != "none":
                result = file_manager.create_directory(dirname)
                # speaker.speak(result)
                print("Directory created: ", result)
            else:
                speaker.speak("Sorry, I couldn't create the directory without a name.")
            
        elif 'delete directory' in query or 'delete folder' in query or 'remove folder' in query:
            # Extract the directory name if provided
            if "directory" in query:
                dirname = query.split("directory")[-1].strip()
            else:
                dirname = query.split("folder")[-1].strip()
                
            # Ask for directory name if not provided
            if len(dirname) < 2:
                dirname = input("Which directory or folder would you like me to delete?")
                
            if dirname != "none":
                # Confirm deletion
                confirmation = input(f"Are you sure you want to delete the directory {dirname}? Say yes to confirm.")
                if confirmation == "yes":
                    result = file_manager.delete_directory(dirname)
                    speaker.speak(result)
                else:
                    speaker.speak("Directory deletion cancelled.")
            else:
                speaker.speak("Sorry, I couldn't delete the directory without a name.")
            
        elif 'list directory' in query or 'list folder' in query:
            # Extract the directory name if provided
            if "list directory" in query:
                dirname = query.split("list directory")[-1].strip()
            else:
                dirname = query.split("list folder")[-1].strip()
                
            # Ask for directory name if not provided or use current directory
            if len(dirname) < 2:
                dirname = input("Which directory or folder would you like me to list? Say current for the current directory.")
                if dirname == "current":
                    dirname = "."
                
            if dirname != "none":
                result = file_manager.list_directory(dirname)
                speaker.speak(result)
            else:
                speaker.speak("Listing current directory:")
                result = file_manager.list_directory(".")
                speaker.speak(result)
            
        elif 'search file' in query or 'find file' in query:
            # Extract the file name if provided
            filename = query.split("file")[-1].strip()
                
            # Ask for file name if not provided
            if len(filename) < 2:
                filename = get_user_input(speaker, speech_recognizer, "What file would you like me to search for?")
                
            if filename != "none":
                speaker.speak(f"Searching for file {filename}...")
                result = file_manager.search_file(filename)
                speaker.speak(result)
            else:
                speaker.speak("Sorry, I couldn't search without a file name.")
        elif "news report" in query:
            news_report()
        elif "mail" in query:
            send_mail()
        elif "game" in query:
            speaker.speak("Opening a game for you!")
            game()
        elif "selfie" in query:
            speaker.speak("Taking a selfie for you!")
            create_gui()
        else:
            # Use Gemini for other queries
            response = Bard().chat(query)
            speaker.speak(response)