#!/usr/bin/env python3
import speech_recognition as sr
import pyttsx3
import os

def speak(text):
    print("SAYING:", text)
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

def listen():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        audio = r.listen(source)
    try:
        command = r.recognize_google(audio)
        print("You said:", command)
        return command
    except Exception:
        speak("Sorry, I didn't catch that.")
        return None

if __name__ == "__main__":
    while True:
        command = listen()
        if not command:
            continue
        command = command.lower()
        if "stop" in command:
            speak("Stopping.")
            break
        elif "artemis" in command:
            os.system("python agents/codexagent_nasa_artemis.py")
            speak("Artemis mission status executed.")
        else:
            speak(f"You said: {command}")
