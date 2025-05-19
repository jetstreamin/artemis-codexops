#!/usr/bin/env python3
"""
Conversational Voice Agent for Artemis CodexOps.
- Speak or type a command. Agent will transcribe, process, respond, and speak.
- Optionally integrates with Whisper (ASR), Piper or Google TTS, and GPT for NLU/conversation.
"""
import os, sys
try:
    import speech_recognition as sr
    import pyttsx3
except ImportError:
    print("Please install speech_recognition and pyttsx3 (pip install speechrecognition pyttsx3)")
    sys.exit(1)

def listen():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Say something!")
        audio = r.listen(source)
    try:
        return r.recognize_google(audio)
    except Exception as e:
        print("Sorry, could not recognize.")
        return None

def speak(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

if __name__ == "__main__":
    while True:
        mode = input("Type (t) or Talk (v)? ").strip().lower()
        if mode == 'v':
            cmd = listen()
        else:
            cmd = input("Command: ")
        if not cmd: continue
        print(f"Recognized: {cmd}")
        # Simple demo: respond to commands
        if "mission" in cmd.lower():
            resp = os.popen("python agents/codexagent_nasa_artemis.py").read()
            print(resp)
            speak("Here's the Artemis mission status.")
        elif "exit" in cmd.lower():
            speak("Goodbye!")
            break
        else:
            speak(f"You said: {cmd}")
