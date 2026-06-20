import speech_recognition as sr
import pyttsx3
import threading

def init_engine():
    """Initialize pyttsx3 engine."""
    engine = pyttsx3.init()
    engine.setProperty('rate', 150)
    return engine

def text_to_speech(text):
    """
    Reads the given text aloud using pyttsx3.
    Runs in a separate thread to prevent blocking the Streamlit app.
    """
    def speak():
        engine = init_engine()
        engine.say(text)
        engine.runAndWait()

    thread = threading.Thread(target=speak)
    thread.start()

def speech_to_text():
    """
    Listens to the microphone and returns the recognized text.
    Returns:
        text (str) or None if not recognized.
    """
    recognizer = sr.Recognizer()
    try:
        with sr.Microphone() as source:
            # Adjust for ambient noise
            recognizer.adjust_for_ambient_noise(source, duration=0.5)
            # Listen for up to 5 seconds, wait up to 5 sec for phrase
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=5)
            
            # Google Speech Recognition (free, no key needed)
            text = recognizer.recognize_google(audio)
            return text
    except sr.WaitTimeoutError:
        return "Timeout: No speech detected."
    except sr.UnknownValueError:
        return "Could not understand audio."
    except sr.RequestError as e:
        return f"Could not request results; {e}"
    except Exception as e:
        return f"Microphone error: {e}"
