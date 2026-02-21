import speech_recognition as sr
from modules.speech_engine import speak
from modules.command_handler import handle_command

def listen_command():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("\nListening...")
        recognizer.pause_threshold = 1
        audio = recognizer.listen(source)
    try:
        print("Recognizing...")
        query = recognizer.recognize_google(audio, language='en-in')
        print(f"You said: {query}\n")
    except Exception:
        speak("Sorry, could you please repeat?")
        return ""
    return query.lower()

if __name__ == "__main__":
    speak("Hello, I am " \
    "your virtual Desktop assistant.")
    while True:
        command = listen_command()
        if not command:
            continue
        if not handle_command(command):
            break
