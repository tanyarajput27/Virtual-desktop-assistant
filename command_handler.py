from modules.web_tasks import open_website, google_search, play_youtube
from modules.weather import get_weather
from modules.campus_assistant import process_campus_query
from modules.speech_engine import speak
from modules.gemini_ai import ask_gemini
def handle_command(command):
    command = command.lower()
    if "open" in command:
        open_website(command)
    elif "search" in command:
        query = command.replace("search for", "").replace("search", "").strip()
        google_search(query)
    elif "play" in command and "youtube" in command:
        query = command.replace("play on youtube", "").strip()
        play_youtube(query)
    elif "play" in command:
        query = command.replace("play", "").strip()
        play_youtube(query)
    elif "weather" in command:
        city = command.replace("weather in", "").strip() or "Delhi"
        get_weather(city)
    elif any(word in command for word in ["cse", "canteen", "hostel", "department", "campus","basketball","parking","academic","examination","ece","left","right","central","ground","auditorium"]):
        process_campus_query(command)
    elif "exit" in command or "quit" in command:
        speak("Goodbye! Have a great day.")
        return False
    else:
        speak("Let me think...")
        ask_gemini(command)
    return True
