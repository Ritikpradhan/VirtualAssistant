import speech_recognition as sr
import pyttsx3
import requests
import json
from datetime import datetime

# Initialize text-to-speech engine
engine = pyttsx3.init()

# Function to convert text to speech
def speak(text):
    engine.say(text)
    engine.runAndWait()

# Function to get weather updates
def get_weather(city):
    api_key = "YOUR_OPENWEATHERMAP_API_KEY"  # Replace with your actual API key
    base_url = "http://api.openweathermap.org/data/2.5/weather"
    params = {"q": city, "appid": api_key}

    response = requests.get(base_url, params=params)
    data = response.json()

    if data["cod"] != "404":
        weather_description = data["weather"][0]["description"]
        temperature = data["main"]["temp"] - 273.15  # Convert to Celsius
        return f"The weather in {city} is {weather_description} with a temperature of {temperature:.2f} degrees Celsius."
    else:
        return f"Sorry, I couldn't retrieve the weather information for {city}."

# Initialize the speech recognition engine
recognizer = sr.Recognizer()

# Main loop for interaction
while True:
    try:
        with sr.Microphone() as source:
            print("Listening...")
            recognizer.adjust_for_ambient_noise(source, duration=1)
            audio = recognizer.listen(source, timeout=5)

        print("Recognizing...")

        # Use Google Web Speech API for speech recognition
        query = recognizer.recognize_google(audio).lower()

        print("You said:", query)

        # Perform actions based on user input
        if "weather" in query:
            speak("Sure, which city would you like the weather for?")
            city = recognizer.recognize_google(recognizer.listen(source)).lower()
            weather_response = get_weather(city)
            speak(weather_response)
        elif "exit" in query:
            speak("Goodbye!")
            break
        else:
            speak("Sorry, I didn't understand that. Can you please repeat?")

    except sr.UnknownValueError:
        print("Sorry, I didn't catch that. Could you please repeat?")
    except sr.RequestError as e:
        print(f"Could not request results from Google Speech Recognition service; {e}")

