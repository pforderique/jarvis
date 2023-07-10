"""
jarvis.py

This file contains the JARVIS class, which allows the user to start and stop
listening for speech, and stores the history of what was said.
"""
import speech_recognition as sr


class JARVIS:
    def __init__(self):
        self.history = []
        self._recognizer = sr.Recognizer()
        self._mic = sr.Microphone()
        self._is_listening = False
        self._terminate = None
        print("Hello Sir. I am JARVIS.")

    def start_listening(self):
        if self._is_listening:
            print("JARVIS is already listening.")

        self._is_listening = True
        with self._mic as source:
            self._recognizer.adjust_for_ambient_noise(source)

        self._terminate = self._recognizer.listen_in_background(self._mic, self._speech_callback)
        print("JARVIS is listening...")

    def stop_listening(self):
        if self._terminate:
            self._terminate(wait_for_stop=False)
        print("JARVIS is no longer listening.")

    def _speech_callback(self, recognizer, audio):
        try:
            transcription = recognizer.recognize_google(audio).lower()
            self.history.append(transcription)
            print("Transcription received: " + transcription)

            if transcription == "quit":
                print("Quitting...", end="")
                self._terminate(wait_for_stop=False)
                print("done.")

        except sr.UnknownValueError:
            print("JARVIS could not understand audio")
        except sr.RequestError as e:
            print("Could not request results from Google Speech Recognition service; {0}".format(e))