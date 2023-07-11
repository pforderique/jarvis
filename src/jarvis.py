"""
jarvis.py

This file contains the JARVIS class, which allows the user to start and stop
listening for speech, and stores the history of what was said.
"""
from .constants import TMP_FOLDER

from gtts import gTTS
import playsound
import speech_recognition as sr

import os
from random import randint
# TODO: add commands = open chrome, navigate to x, tab, tab, tab, hit enter.
# in preprosser.py, we can have a list of commands


class JARVIS:
    SAVED_AUDIOS_PATH = './data/audio/'

    def __init__(self):
        self.history = []
        self._recognizer = sr.Recognizer()
        self._mic = sr.Microphone()
        self._is_listening = False
        self._terminate = None
        self._say("./data/audio/jarvis_startup.mp3", is_file=True)

        os.makedirs(TMP_FOLDER, exist_ok=True)

    def start_listening(self):
        if self._is_listening:
            self._say("I am already listening Sir.")

        self._is_listening = True
        with self._mic as source:
            self._recognizer.adjust_for_ambient_noise(source)

        self._terminate = self._recognizer.listen_in_background(self._mic, self._speech_callback)
        self._say("At your command Sir...")

    def stop_listening(self):
        if self._terminate:
            self._terminate(wait_for_stop=False)
        self._say("Goodbye, Sir.")

    def _say(self, content, is_file=False):
        if is_file:
            return playsound.playsound(content, block=False)

        content_hash = f'{hash(content) + randint(0, 100)}.mp3'
        save_location = os.path.join(TMP_FOLDER, content_hash)

        tts = gTTS(text=content, lang='en')
        tts.save(save_location)
        playsound.playsound(save_location, block=False)
        os.remove(save_location)
        print(content)

    def _speech_callback(self, recognizer, audio):
        try:
            transcription = recognizer.recognize_google(audio).lower()
            self.history.append(transcription)
            print("Transcription received: " + transcription)

            if transcription in ["quit", "stop", "stop listening"]:
                print("Quitting...", end="")
                self._say("Goodbye, Sir.")
                self._terminate(wait_for_stop=False)
                print("done.")

        except sr.UnknownValueError:
            self._say("I'm sorry sir, I could not understand that.")
        except sr.RequestError as e:
            print("Could not request results from Google Speech Recognition service; {0}".format(e))