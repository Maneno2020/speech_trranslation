import base64
import requests
from tkinter import *
from tkinter import ttk
import pyttsx3
import speech_recognition as sr
from deep_translator import GoogleTranslator
import pygame
import tempfile
import os
import sounddevice as sd
import soundfile as sf

# API URLs and headers
ASR_API_URL = "https://api-inference.huggingface.co/models/indonesian-nlp/wav2vec2-luganda"
ASR_HEADERS = {"Authorization": "Bearer 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"}

TRANSLATION_API_URL = "https://sunbird-ai-api-5bq6okiwgq-ew.a.run.app"
TRANSLATION_HEADERS = {
    'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJtYW5lbm8yMDIwIiwiZXhwIjo0ODQyMzE2MDYyfQ'
                     '.elEqO4FYZRlfKBYJI8S1ojcwHSzA9GAjLydONqPy8-0',
    "Content-Type": "application/json"
}

# Disable Pygame video initialization
os.environ["SDL_VIDEODRIVER"] = "dummy"

# Initialize Pygame audio
pygame.mixer.init()

root = Tk()
root.title("Luganda-English Language Translation")
root.geometry("1080x400")
root.resizable(False, False)
root.configure(background="white")

# Placeholder text
placeholder_text = "Type a sentence or press the microphone to record audio"


def query_asr(audio_data, sample_rate):
    response = requests.post(ASR_API_URL, headers=ASR_HEADERS, data=audio_data, params={"sample_rate": sample_rate})
    return response.json()


def query_translation(text):
    payload = {
        "text": text
    }
    response = requests.post(f"{TRANSLATION_API_URL}/tasks/tts", headers=TRANSLATION_HEADERS, json=payload)

    if response.status_code == 200:
        base64_string = response.json()["base64_string"]
        audio_data = base64.b64decode(base64_string)
        play_audio(audio_data)
    else:
        print("Error:", response.status_code, response.text)


def speak_text(text):
    if combo2.get() == "Luganda":
        query_translation(text)
    else:
        engine = pyttsx3.init()
        engine.setProperty("rate", 150)  # Adjust the speech rate (optional)
        engine.setProperty("volume", 1.0)  # Adjust the volume (optional)
        engine.say(text)
        engine.runAndWait()


def play_audio(audio_data):
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_file:
        temp_filename = temp_file.name
        temp_file.write(audio_data)

    pygame.mixer.music.load(temp_filename)
    pygame.mixer.music.play()

    while pygame.mixer.music.get_busy():
        continue

    # Delete the temporary file after playing
    os.remove(temp_filename)


def on_combo1_select(event):
    selected_language = combo1.get()
    label1.configure(text=selected_language)
    if selected_language == "Luganda":
        combo2.set("English")
        label2.configure(text="English")
    elif selected_language == "English":
        combo2.set("Luganda")
        label2.configure(text="Luganda")


def on_combo2_select(event):
    selected_language = combo2.get()
    label2.configure(text=selected_language)
    if selected_language == "Luganda":
        combo1.set("English")
        label1.configure(text="English")
    elif selected_language == "English":
        combo1.set("Luganda")
        label1.configure(text="Luganda")


def translate_now():
    text_ = text1.get(1.0, END)
    if text_.strip() == placeholder_text:
        print("Text field is empty")
        return

    source_lang = combo1.get()
    target_lang = combo2.get()

    translation = GoogleTranslator(source=source_lang.lower(), target=target_lang.lower()).translate(text_)
    text2.config(state=NORMAL)  # Enable text2
    text2.delete(1.0, END)
    text2.insert(END, translation)
    text2.config(state=DISABLED)  # Disable text2 again

    # Speak the translated text
    speak_text(translation)


def listen_audio():
    r = sr.Recognizer()

    selected_language = combo1.get()
    if selected_language == "Luganda":
        r.recognize_google = query_asr

    # Define the recording parameters
    duration = 20  # Recording duration in seconds
    sample_rate = 16000  # Sample rate

    # Record audio from the microphone
    print("Recording...")
    audio = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=1)
    sd.wait()  # Wait until recording is finished
    print("Recording finished.")

    # Save the recorded audio to a temporary WAV file
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_file:
        filename = temp_file.name
        sf.write(filename, audio, sample_rate)

    # Perform speech recognition on the recorded audio
    with open(filename, "rb") as f:
        audio_data = f.read()
        text = r.recognize_google(audio_data, sample_rate=sample_rate)

    # Insert the recognized text into the text1 field
    text1.delete(1.0, END)
    text1.insert(END, text)

    # Delete the temporary audio file
    os.remove(filename)


def clear_placeholder(event):
    current_text = text1.get(1.0, END)
    if current_text.strip() == placeholder_text:
        text1.delete(1.0, END)
        text1.configure(foreground="black")  # Change text color to black


def restore_placeholder(event):
    current_text = text1.get(1.0, END)
    if current_text.strip() == "":
        text1.insert(END, placeholder_text)
        text1.configure(foreground="gray")  # Change text color to gray


def enable_typing(event):
    current_text = text1.get(1.0, END)
    if current_text.strip() == placeholder_text:
        text1.delete(1.0, END)
        text1.configure(foreground="black")  # Change text color to black


languages = ["Luganda", "English"]

combo1 = ttk.Combobox(root, values=languages, font="Roboto 14", state="readonly")
combo1.place(x=130, y=20)
combo1.set(languages[0])
combo1.bind("<<ComboboxSelected>>", on_combo1_select)

label1 = Label(root, text=languages[0], font="segoe 30 bold", bg="white", width=18, bd=5, relief=GROOVE)
label1.place(x=10, y=50)

combo2 = ttk.Combobox(root, values=languages, font="Roboto 14", state="readonly")
combo2.place(x=730, y=20)
combo2.set(languages[1])
combo2.bind("<<ComboboxSelected>>", on_combo2_select)

label2 = Label(root, text=languages[1], font="segoe 30 bold", bg="white", width=18, bd=5, relief=GROOVE)
label2.place(x=620, y=50)

# First frame
f = Frame(root, bg="black", bd=5)
f.place(x=10, y=118, width=440, height=210)

text1 = Text(f, font="Roboto 20", bg="white", relief=GROOVE, wrap=WORD)
text1.place(x=0, y=0, width=430, height=200)
text1.bind("<Button-1>", clear_placeholder)  # Bind clear_placeholder function to MouseClick event
text1.bind("<<FocusOut>>", restore_placeholder)  # Bind restore_placeholder function to FocusOut event
text1.bind("<Button-1>", enable_typing)  # Bind enable_typing function to MouseClick event

# Insert placeholder text
text1.insert(END, placeholder_text)
text1.configure(foreground="gray")  # Set initial text color to gray

scrollbar1 = Scrollbar(f)
scrollbar1.pack(side="right", fill='y')

scrollbar1.configure(command=text1.yview)
text1.configure(yscrollcommand=scrollbar1.set)

# Second frame
f1 = Frame(root, bg="black", bd=5)
f1.place(x=620, y=118, width=440, height=210)

text2 = Text(f1, font="Roboto 20", bg="white", relief=GROOVE, wrap=WORD, state=DISABLED)
text2.place(x=0, y=0, width=430, height=200)

scrollbar2 = Scrollbar(f1)
scrollbar2.pack(side="right", fill='y')

scrollbar2.configure(command=text2.yview)
text2.configure(yscrollcommand=scrollbar2.set)

# Speaker button
speaker_button = Button(f1, text="\U0001f508", font=("Arial", 15), bd=0, bg="black", fg="white",
                        activebackground="grey", command=lambda: speak_text(text2.get(1.0, END)))
speaker_button.place(x=400, y=165)

# Microphone button
microphone_button = Button(f, text="\u23f0", font=("Arial", 15), bd=0, bg="black", fg="white",
                           activebackground="grey", command=listen_audio)
microphone_button.place(x=10, y=165)

# Translate button
translate = Button(root, text="Translate", font=("Roboto", 15), activebackground="white", cursor="hand2",
                   bd=1, width=10, height=2, bg="black", fg="white", command=translate_now)
translate.place(x=467, y=250)

root.mainloop()
