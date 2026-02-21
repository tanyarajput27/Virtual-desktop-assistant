import google.generativeai as genai
from modules.speech_engine import speak

# Your Gemini API Key
genai.configure(api_key="AIzaSyDI1K44dsdRrkCZ0UJvC3WlH--iiXiyjkg")

# Initialize model
model = genai.GenerativeModel("gemini-2.5-pro")

def ask_gemini(prompt):
    try:
        response = model.generate_content(prompt)
        reply = response.text
        print("Gemini Response:", reply)
        speak(reply)
        return reply
    except Exception as e:
        print("Error:", e)
        speak("Sorry, I could not process that request using AI.")
        return None
