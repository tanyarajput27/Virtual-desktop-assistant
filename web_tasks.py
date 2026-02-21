import webbrowser
from modules.speech_engine import speak

def open_website(command):
    sites = {
        "google": "https://www.google.com",
        "youtube": "https://www.youtube.com",
        "linkedin": "https://www.linkedin.com",
        "github": "https://github.com",
        "igdtuw": "https://www.igdtuw.ac.in/"
    }

    for site in sites:
        if site in command:
            speak(f"Opening {site}...")
            webbrowser.open(sites[site])
            return
    speak("Sorry, I don't know that site yet.")

def google_search(query):
    speak(f"Searching Google for {query}...")
    webbrowser.open(f"https://www.google.com/search?q={query}")

def play_youtube(query):
    speak(f"Playing {query} on YouTube...")
    webbrowser.open(f"https://www.youtube.com/results?search_query={query}")
