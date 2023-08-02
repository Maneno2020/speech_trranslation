# Required Libraries: deep_translator, tkinter

# Install required libraries:
# pip install deep_translator
# pip install tk

from tkinter import *
from tkinter import ttk
from deep_translator import GoogleTranslator

root = Tk()
root.title("English to Luganda Translation")
root.geometry("500x300")
root.configure(background="white")


# Function to translate the text
def translate_text():
    text = text_entry.get(1.0, END).strip()
    if not text:
        return

    translation = GoogleTranslator(source='en', target='lg').translate(text)
    translation_output.delete(1.0, END)
    translation_output.insert(END, translation)


# Text Entry
text_entry = Text(root, font=("Helvetica", 12), wrap=WORD, height=5, padx=5, pady=5)
text_entry.pack(pady=10)

# Translate Button
translate_button = Button(root, text="Translate", font=("Helvetica", 14), command=translate_text)
translate_button.pack(pady=5)

# Translation Output
translation_output = Text(root, font=("Helvetica", 12), wrap=WORD, height=5, padx=5, pady=5)
translation_output.pack(pady=10)

root.mainloop()
