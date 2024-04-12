import unittest
from src.recognition import TextRecognition
from src.utils import ask_to_gpt
import nltk
from nltk import word_tokenize

class TestCommandsTranscription(unittest.TestCase):
    threshold = 0.5

    def setUp(self):
            """Initialise TextRecognition"""
            self.recognition = TextRecognition()
            try:
                nltk.data.find('tokenizers/punkt')
            except LookupError:
                nltk.download('punkt')

    def score_transcription(self, expected, actual):
        """Transcription des scores basée sur des mots tokenisés."""
        expected_tokens = set(word_tokenize(expected.lower()))
        actual_tokens = set(word_tokenize(actual.lower()))
        common_elements = expected_tokens.intersection(actual_tokens)
        if len(expected_tokens) == 0: 
            return 0.0
        return len(common_elements) / len(expected_tokens)


    def test_avance(self):
        """Test if the 'avance' audio file contains the correct word and scores its relevance."""
        expected_phrase = "avance"
        transcribed_text = self.recognition._transcribe_audio_from_file('./static/Avance-1.wav')
        score = self.score_transcription(expected_phrase, transcribed_text)
        self.assertIn("avance", transcribed_text)
        self.assertGreaterEqual(score, self.threshold)
        print(f"Test 'avance' - Score: {score}")

    def test_recule(self):
        """Teste si le fichier audio pour 'recule' contient le mot correct et score la pertinence."""
        expected_phrase = "recule"
        transcribed_text = self.recognition._transcribe_audio_from_file('./static/recule.wav')
        score = self.score_transcription(expected_phrase, transcribed_text)
        self.assertIn("recule", transcribed_text)
        self.assertGreaterEqual(score, self.threshold)
        print(f"Test 'recule' - Score: {score}")


    def test_tourne(self):
        """Teste si le fichier audio pour 'tourner à droite' contient le mot correct et score la pertinence."""
        expected_phrase = "tourne à droite"
        transcribed_text = self.recognition._transcribe_audio_from_file('./static/tourne-a-droite.wav')
        score = self.score_transcription(expected_phrase, transcribed_text)
        self.assertIn("tourne", transcribed_text)
        self.assertGreaterEqual(score, self.threshold)
        print(f"Test 'tourne' - Score: {score}")



class TestGPTIntegration(unittest.TestCase):
    threshold = 0.5

    def setUp(self):
        """Initialise TextRecognition"""
        self.recognition = TextRecognition()
        try:
            nltk.data.find('tokenizers/punkt')
        except LookupError:
            nltk.download('punkt', quiet=True)

    def score_transcription(self, expected_phrases, actual):
        """Transcription des scores basée des mots tokenisés."""
        actual_tokens = set(word_tokenize(actual.lower()))
        score = sum(1 for phrase in expected_phrases if any(token in actual_tokens for token in word_tokenize(phrase.lower())))
        max_score = len(expected_phrases)
        return score / max_score if max_score > 0 else 0.0

    def test_transcription_and_summary(self):
        """Test si GPT résume correctement les douleurs de dos mentionné par le patient"""
        expected_phrases = ['mal au dos', 'douleur au dos', 'bloqué le dos']  
        recognizer = self.recognition
        transcribed_text = recognizer._transcribe_audio_from_file('./static/Je-me-suis-bloque-le-dos.wav')
        summary = ask_to_gpt(transcribed_text)

        score = self.score_transcription(expected_phrases, summary)

        print(f"Test 'Summary' - Score: {score:.2f}")
        print(f"Summary: {summary}")

if __name__ == '__main__':
    unittest.main()
