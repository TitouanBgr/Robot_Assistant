import speech_recognition as sr
from src.utils import ask_to_gpt
from gpiozero import Motor
from time import sleep
import requests

class TextRecognition:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.commands = {
            "avance": self.move_forward,
            "recule": self.move_backward,
            "gauche": self.move_left,
            "droite": self.move_right,
            "écoute": self.listen_more
        }
        self.api_url = "http://10.38.161.78:5000"  

    def move_forward(self, text):
        print("Action: Avancer")
        requests.post(f"{self.api_url}/avancer")

    def move_backward(self, text):
        print("Action: Reculer")
        requests.post(f"{self.api_url}/reculer")

    def move_left(self, text):
        print("Action: Tourner à gauche")
        requests.post(f"{self.api_url}/gauche")

    def move_right(self, text):
        print("Action: Tourner à droite")
        requests.post(f"{self.api_url}/droite")

    def listen_more(self, text):
        return ask_to_gpt(text)


    def run_from_microphone(self):
        with sr.Microphone() as source:
            self.recognizer.adjust_for_ambient_noise(source)
            print("Ajustement au bruit ambiant effectué. Parlez maintenant...")
            while True:
                try:
                    audio = self.recognizer.listen(source)
                    text = self.recognizer.recognize_google(audio, language='fr-FR').lower()
                    print("Vous:", text)
                    self.execute_command(text)
                except sr.UnknownValueError:
                    print("Google Speech Recognition n'a pas pu comprendre l'audio.")
                except sr.RequestError as e:
                    print(f"Impossible d'obtenir les résultats depuis Google Speech Recognition service; {e}")

    def _transcribe_audio_from_file(self, file_path):
        """Transcrit le contenu audio d'un fichier en utilisant Google Speech Recognition."""
        with sr.AudioFile(file_path) as source:
            audio_data = self.recognizer.record(source)
            try:
                return self.recognizer.recognize_google(audio_data, language='fr-FR').lower()
            except (sr.UnknownValueError, sr.RequestError) as e:
                return str(e)

    def run_from_file(self, filename):
        text = self._transcribe_audio_from_file(filename)
        if isinstance(text, str) and text:
            print("Fichier audio dit:", text)
            self.execute_command(text)
        else:
            print("Erreur de transcription ou fichier vide:", text)


    def execute_command(self, text):
        for command, action in self.commands.items():
            if command in text:
                action(text)
                return 