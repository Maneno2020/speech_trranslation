from tkinter import *
from tkinter import ttk
from googletrans import Translator
import pyttsx3
import speech_recognition as sr

root = Tk()
root.title("English-French Language Translation")
root.geometry("1080x400")
root.resizable(False, False)
root.configure(background="white")

# Placeholder text
placeholder_text = "Type a sentence or press the microphone to record audio"


def label_change():
    c = combo1.get()
    c1 = combo2.get()
    label1.configure(text=c)
    label2.configure(text=c1)
    root.after(1000, label_change)


def on_combo1_select(event):
    selected_language = combo1.get()
    label1.configure(text=selected_language)
    if selected_language == "English":
        combo2.set("French")
        label2.configure(text="French")
    elif selected_language == "French":
        combo2.set("English")
        label2.configure(text="English")


def on_combo2_select(event):
    selected_language = combo2.get()
    label2.configure(text=selected_language)
    if selected_language == "English":
        combo1.set("French")
        label1.configure(text="French")
    elif selected_language == "French":
        combo1.set("English")
        label1.configure(text="English")


def translate_now():
    text_ = text1.get(1.0, END)
    if text_.strip() == placeholder_text:
        print("Text field is empty")
        return

    t1 = Translator()
    trans_text = t1.translate(text_, src=combo1.get(), dest=combo2.get())
    trans_text = trans_text.text

    text2.delete(1.0, END)
    text2.insert(END, trans_text)

    # Speak the translated text
    speak_text()


def listen_audio():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source)

    # Clear text field before listening
    text1.delete(1.0, END)

    try:
        text = r.recognize_google(audio)
        text1.insert(END, text)
    except sr.UnknownValueError:
        print("Speech recognition could not understand audio")
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))


def speak_text():
    engine = pyttsx3.init()
    text = text2.get(1.0, END)
    engine.say(text)
    engine.runAndWait()


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


languages = ["English", "French"]

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

text2 = Text(f1, font="Roboto 20", bg="white", relief=GROOVE, wrap=WORD)
text2.place(x=0, y=0, width=430, height=200)

scrollbar2 = Scrollbar(f1)
scrollbar2.pack(side="right", fill='y')

scrollbar2.configure(command=text2.yview)
text2.configure(yscrollcommand=scrollbar2.set)

# Speaker button
speaker_button = Button(f1, text="\U0001f508", font=("Arial", 15), bd=0, bg="black", fg="white",
                        activebackground="grey", command=speak_text)
speaker_button.place(x=400, y=165)

# Translate button
translate = Button(root, text="Translate", font=("Roboto", 15), activebackground="white", cursor="hand2",
                   bd=1, width=10, height=2, bg="black", fg="white", command=translate_now)
translate.place(x=467, y=250)

label_change()
root.mainloop()
