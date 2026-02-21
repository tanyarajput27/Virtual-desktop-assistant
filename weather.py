import requests
from modules.speech_engine import speak

API_KEY = "76f16eb8b60749a4aa9133427251411"
BASE_URL = "http://api.weatherapi.com/v1/current.json"

def get_weather(location="Delhi"):
    try:
        if not location or location.strip() == "":
            location = "Delhi"

        params = {
            "key": API_KEY,
            "q": location,
            "aqi": "yes"
        }

        response = requests.get(BASE_URL, params=params)

        # Invalid city or API error
        if response.status_code != 200:
            speak(f"Sorry, I couldn't find weather information for {location}.")
            print("❌ API Error:", response.text)
            return

        data = response.json()

        # Extract all details
        city = data['location']['name']
        country = data['location']['country']
        temp = data['current']['temp_c']
        condition = data['current']['condition']['text']
        humidity = data['current']['humidity']
        wind = data['current']['wind_kph']

        # Final weather report
        weather_report = (
            f"The weather in {city}, {country} is {condition}. "
            f"The temperature is {temp} degree Celsius. "
            f"Humidity is {humidity} percent, "
            f"and the wind speed is {wind} kilometers per hour."
        )

        # Speak and print it
        speak(weather_report)
        print(weather_report)

    except Exception as e:
        speak("I couldn't fetch the weather. Please check your internet connection.")
        print("❌ Network Error:", e)


