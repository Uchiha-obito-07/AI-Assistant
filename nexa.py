import speech_recognition as sr
import webbrowser
import pyttsx3
import musicLibrary
import requests

engine = pyttsx3.init()
newsapi = "178e663584444bbda1b4538cbe52a315"

def speak(text):
    engine.say(text)
    engine.runAndWait()

def processCommand(c):
    if "open google" in c.lower():
        speak("opening google")
        r = sr.Recognizer()
        webbrowser.open("https://google.com")

    elif "open instagram" in c.lower():
        webbrowser.open("https://instagram.com")

    elif "open youtube" in c.lower():
        webbrowser.open("https://youtube.com")

    elif "open AI" in c.lower():
        webbrowser.open("https://chatgpt.com/")

    elif "open whatsapp" in c.lower():
        webbrowser.open("https://web.whatsapp.com/")
    elif "open wikipidia" in c.lower():
        webbrowser.open("https://wikipidia.com")
    elif "play games" in c.lower():
        webbrowser.open("https://poki.com/")
    elif c.lower().startswith("play"):
        song = c.lower().split(" ")[1]
        link = musicLibrary.music.get(song)

        if link:
            webbrowser.open(link)
        else:
            speak(f"I couldn’t find the song {song}")

    elif "news" in c.lower():
        r = requests.get(
            f"https://newsapi.org/v2/top-headlines?country=in&apiKey={newsapi}"
        )

        if r.status_code == 200:
            data = r.json()
            articles = data.get('articles', [])

            for article in articles[:5]:
                speak(article['title'])


if __name__ == "__main__":
    speak("Initializing. Say Nexa to wake me up")

    r = sr.Recognizer()

    while True:
        try:
            with sr.Microphone() as source:
                r.adjust_for_ambient_noise(source, duration=0.5)

                print("Listening for wake word 'Nexa'...")

                audio = r.listen(
                    source,
                    timeout=5,
                    phrase_time_limit=3
                )

                word = r.recognize_google(audio)

                print("Heard:", word)

                if "Nexa" in word.lower():
                    print("Wake word detected!")

                    speak("Yes, how can I help?")

                    with sr.Microphone() as source:
                        r.adjust_for_ambient_noise(source, duration=0.5)

                        print("Listening for command...")

                        audio = r.listen(
                            source,
                            timeout=5,
                            phrase_time_limit=5
                        )

                        command = r.recognize_google(audio)

                        print("Command:", command)

                        processCommand(command)

        except sr.WaitTimeoutError:
            continue

        except Exception as e:
            print("Error:", e)