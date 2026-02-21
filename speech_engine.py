import pyttsx3
from gtts import gTTS
import pygame
import tempfile
import os
import time

# Initialize pyttsx3 engine safely
try:
    engine = pyttsx3.init('sapi5')
    engine.setProperty('rate', 170)
    engine.setProperty('volume', 1.0)
    voices = engine.getProperty('voices')
    if voices:
        engine.setProperty('voice', voices[0].id)
except Exception as e:
    print("pyttsx3 initialization failed:", e)
    engine = None


def speak_offline(text):
    """Try speaking using pyttsx3 (offline)."""
    try:
        if engine:
            engine.say(text)
            engine.runAndWait()
            time.sleep(0.2)  # small delay for smooth playback
            return True
        return False
    except Exception as e:
        print("Offline speech failed:", e)
        return False


def speak_online(text):
    """Fallback to online Google TTS (gTTS) with pygame."""
    try:
        tts = gTTS(text=text, lang='en')
        with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as fp:
            temp_path = fp.name
            tts.save(temp_path)

        pygame.mixer.init()
        pygame.mixer.music.load(temp_path)
        pygame.mixer.music.play()

        # Wait until the audio finishes
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)

        pygame.mixer.quit()
        os.remove(temp_path)
    except Exception as e:
        print("Online speech failed:", e)


def speak(text):
    """Unified speak function with print + fallback."""
    print(f"Assistant: {text}")
    success = speak_offline(text)
    if not success:
        speak_online(text)
