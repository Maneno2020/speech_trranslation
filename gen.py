import requests
from tkinter import *
from tkinter import ttk
import pyttsx3
import speech_recognition as sr
from deep_translator import GoogleTranslator
import base64
import pygame
import tempfile
import os
import time

url = 'https://sunbird-ai-api-5bq6okiwgq-ew.a.run.app'
API_URL = "https://api-inference.huggingface.co/models/indonesian-nlp/wav2vec2-luganda"
api_headers = {"Authorization": "Bearer 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"}

headers = {
    'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJtYW5lbm8yMDIwIiwiZXhwIjo0ODQyMzE2MDYyfQ'
                     '.elEqO4FYZRlfKBYJI8S1ojcwHSzA9GAjLydONqPy8-0',
    "Content-Type": "application/json"
}

root = Tk()
root.title("Luganda-English Language Translation")
root.geometry("1080x400")
root.resizable(False, False)
root.configure(background="white")


# Placeholder text
placeholder_text = "Type a sentence or press the microphone to record audio"


# Define functions
def speak_text(text):
    if combo2.get() == "Luganda":
        payload = {
            "text": text
        }
        response = requests.post(f"{url}/tasks/tts", headers=headers, json=payload)

        if response.status_code == 200:
            base64_string = response.json()["base64_string"]
            audio_data = base64.b64decode(base64_string)
            play_audio(audio_data)
        else:
            print("Error:", response.status_code, response.text)
    else:
        engine = pyttsx3.init()
        engine.setProperty("rate", 150)  # Adjust the speech rate (optional)
        engine.setProperty("volume", 1.0)  # Adjust the volume (optional)
        engine.say(text)
        engine.runAndWait()


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


def recognize_speech(audio_file_path, is_luganda):
    if is_luganda:
        api_url = API_URL
        headers = api_headers
    else:
        api_url = f"{url}/tasks/tts"
        headers = api_headers

    with open(audio_file_path, "rb") as f:
        data = f.read()

    max_retries = 5  # Adjust the maximum number of retries as needed
    retries = 0

    while retries < max_retries:
        response = requests.post(api_url, headers=headers, data=data)
        result = response.json()

        if "error" not in result:
            return result

        if result["error"] == "Model indonesian-nlp/wav2vec2-luganda is currently loading":
            print("Model is currently loading. Retrying...")
            retries += 1
            time.sleep(5)  # Adjust the retry interval as needed
        else:
            print("Error occurred during recognition.")
            return None

    print("Max retries exceeded. Unable to process request.")
    return None


def save_microphone_audio(timeout=10):
    recognizer = sr.Recognizer()

    # Delete the previous temporary audio file if it exists
    temp_audio_file = "temp.wav"
    if os.path.exists(temp_audio_file):
        os.remove(temp_audio_file)

    with sr.Microphone() as source:
        try:
            # Adjust the timeout value to capture audio for the desired duration
            audio = recognizer.listen(source, timeout=timeout)
        except sr.WaitTimeoutError:
            return None

    # Save the captured audio to a new temporary WAV file.
    with open(temp_audio_file, "wb") as f:
        f.write(audio.get_wav_data())

    return temp_audio_file


def listen_audio():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source)

    # Clear text field before listening
    text1.delete(1.0, END)

    temp_audio_file = "temp.wav"
    with open(temp_audio_file, "wb") as f:
        f.write(audio.get_wav_data())

    if combo1.get() == "Luganda":
        is_luganda = True
        output = recognize_speech(temp_audio_file, is_luganda)
        if output:
            recognized_text = output["text"]  # Assuming the API response contains the recognized text
            text1.delete(1.0, END)
            text1.insert(END, recognized_text)
    try:
        if combo1.get() == "Luganda":
            is_luganda = True
            output = recognize_speech(audio, is_luganda)
        else:

            output = r.recognize_google(audio )

        if "text" in output:
            recognized_text = output["text"]
            text1.insert(END, recognized_text)
        else:
            text = r.recognize_google(audio)
            text1.insert(END, text)
            # print("No 'text' key found in the API response.")
    except sr.UnknownValueError:
        print("Speech recognition could not understand audio")
    except sr.RequestError as e:
        print("Could not request results from the recognition service; {0}".format(e))


def play_audio(audio_data):
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_file:
        temp_filename = temp_file.name
        temp_file.write(audio_data)

    pygame.mixer.init()
    pygame.mixer.music.load(temp_filename)
    pygame.mixer.music.play()

    # Wait for the audio playback to finish
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)  # Adjust the tick value as needed

    # Stop and close the audio playback
    pygame.mixer.music.stop()
    pygame.mixer.quit()

    # Delete the temporary file after playing
    os.remove(temp_filename)


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


# Define GUI components

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

# Microphone button
microphone_button = Button(f, text="\u23f0", font=("Arial", 15), bd=0, bg="black", fg="white",
                           activebackground="grey", command=listen_audio)
microphone_button.place(x=10, y=165)

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

# Translate button
translate = Button(root, text="Translate", font=("Roboto", 15), activebackground="white", cursor="hand2",
                   bd=1, width=10, height=2, bg="black", fg="white", command=translate_now)
translate.place(x=467, y=250)

root.mainloop()

# Step 1: Record audio from the microphone and save it as a temporary file
recording_duration = 10  # Adjust the recording duration (in seconds) as needed
temp_audio_file = save_microphone_audio(timeout=recording_duration)

if temp_audio_file:
    # Step 2: Use the pre-recorded audio file for transcription
    output = recognize_speech(temp_audio_file)

    if output:
        print(output)

    # Step 3: Clean up - delete the temporary audio file
    if os.path.exists(temp_audio_file):
        os.remove(temp_audio_file)

else:
    print("No sound detected.")
