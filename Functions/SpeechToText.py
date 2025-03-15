import speech_recognition as sr

class SpeechRecognizer:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()

    def listen_continuously(self):
        """Continuously listens and returns recognized speech as text."""
        with self.microphone as source:
            self.recognizer.adjust_for_ambient_noise(source, duration=1)
            self.recognizer.pause_threshold=1.5
            print("🎙️ Listening continuously... Speak now!")

            while True:
                try:
                    print("\n🎙️ Listening...")
                    audio = self.recognizer.listen(source, timeout=5)  # Listen for 10 sec max

                    # Convert speech to text
                    command = self.recognizer.recognize_google(audio).lower()

                    print(f"✅ Recognized: {command}")
                    return command  # ✅ Returns the recognized text

                except sr.UnknownValueError:
                    print("🤷 Could not understand. Try speaking clearly.")
                except sr.RequestError:
                    print("⚠️ Error: Unable to connect to Google Speech API.")
                except Exception as e:
                    print(f"⚠️ Unexpected Error: {e}")

