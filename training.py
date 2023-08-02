# import googletrans
# from tkinter import *
# from tkinter import ttk, messagebox
# from googletrans import Translator
#
# root = Tk()
# root.title("LUGANDA-LUO LANGUAGE TRANSLATION")
# root.geometry("1080x400")
# root.resizable(False, False)
# root.configure(background="white")
#
# # choice1 = StringVar()
# # choice2 = StringVar()
# #
# # choices = {'Luganda', 'Luo'}
# # choice1.set('Luganda')
# # choice2.set('Luo')
# #
# # choice1Menu = OptionMenu(root, choice1, *choices)
# # Label(root, text="Choose a Language").grid(row=0, column=1)
# # choice1Menu.grid(row=1, column=1)
#
# # choice2Menu = OptionMenu(root, choice2, *choices)
# # Label(root, text="Translated Language").grid(row=0, column=2)
# # choice2Menu.grid(row=1, column=2)
# #
# # Label(root, text="Enter text").grid(row=2, column=0)
# # var = StringVar()
# # textbox = Entry(root, textvariable=var).grid(row = 2, column=1)
# #
# # Label(root, text="Output").grid(row=2, column=2)
# # var1 = StringVar()
# # textbox = Entry(root, textvariable=var1).grid(row = 2, column=1)
#
#
# def label_change():
#     c = combo1.get()
#     c1 = combo2.get()
#     label1.configure(text=c)
#     label2.configure(text=c1)
#     root.after(1000, label_change)
#
#
# # icon
# # image_icon=PhotoImage(file="google.png")
# # root.iconphoto(False,image_icon)
#
# # arrow
# # arrow_image = PhotoImage(file="arrow.png")
# # image_label =Label(root, image=arrow_image, width=150)
# # image_label.place(x=460, y=50)
#
# # language = googletrans.LANGUAGES
# # languageV = list(language.values())
# # lang1 = language.keys()
#
#
# choice1 = StringVar()
# choice2 = StringVar()
#
# choices = {'Luganda', 'Luo'}
# choice1.set('Luganda')
# choice2.set('Luo')
#
# choice1Menu = OptionMenu(root, choice1, *choices)
# Label(root, text="Choose a Language").grid(row=0, column=1)
# choice1Menu.grid(row=1, column=1)
#
# choice2Menu = OptionMenu(root, choice2, *choices)
# Label(root, text="Translated Language").grid(row=0, column=2)
# choice2Menu.grid(row=1, column=2)
#
#
#
# # first combobox
#
# combo1 = ttk.Combobox(root, values=choices, font="Roboto 14", state="r")
# combo1.place(x=130, y=20)
# combo1.set("ENGLISH")
#
# label1 = Label(root, text="Luganda", font="segoe 30 bold", bg="white", width=18, bd=5, relief=FLAT)
# label1.place(x=10, y=50)
#
# # second combo
# combo2 = ttk.Combobox(root, values=choices, font="Roboto 14", state="r")
# combo2.place(x=730, y=20)
# combo2.set("SELECT LANGUAGE")
#
# label2 = Label(root, text="ENGLISH", font="segoe 30 bold", bg="white", width=18, bd=5, relief=GROOVE)
# label2.place(x=620, y=50)
#
# label_change()
# root.mainloop()


# from nltk import wordpunct_tokenize
# from nltk.corpus import stopwords
#
# def identify_language(text):
#     # Tokenize the text
#     tokens = wordpunct_tokenize(text.lower())
#
#     # Remove stopwords
#     stopwords_list = stopwords.words("english") + stopwords.words("luganda") + stopwords.words("luo")
#     filtered_tokens = [token for token in tokens if token not in stopwords_list]
#
#     # Count the frequency of stopwords for each language
#     english_count = 0
#     luganda_count = 0
#     luo_count = 0
#
#     for token in filtered_tokens:
#         if token in stopwords.words("english"):
#             english_count += 1
#         elif token in stopwords.words("luganda"):
#             luganda_count += 1
#         elif token in stopwords.words("luo"):
#             luo_count += 1
#
#     # Compare the frequencies to determine the language
#     if english_count > luganda_count and english_count > luo_count:
#         return "English"
#     elif luganda_count > english_count and luganda_count > luo_count:
#         return "Luganda"
#     elif luo_count > english_count and luo_count > luganda_count:
#         return "Luo"
#     else:
#         return "Unknown"
#
# # Example usage
# text = "Otim ni mochola okwongorek"
# language = identify_language(text)
# print("Detected Language:", language)



from tkinter import *
from tkinter import ttk
from googletrans import Translator
import pyttsx3
import speech_recognition as sr

root = Tk()
root.title("LUGANDA-LUO LANGUAGE TRANSLATION")
root.geometry("1080x400")
root.resizable(False, False)
root.configure(background="white")

def label_change():
    c = combo1.get()
    c1 = combo2.get()
    label1.configure(text=c)
    label2.configure(text=c1)
    root.after(1000, label_change)

def on_combo1_select(event):
    selected_language = combo1.get()
    label1.configure(text=selected_language)
    if selected_language == "Luganda":
        combo2.set("Luo")
        label2.configure(text="Luo")
    elif selected_language == "Luo":
        combo2.set("Luganda")
        label2.configure(text="Luganda")

def on_combo2_select(event):
    selected_language = combo2.get()
    label2.configure(text=selected_language)
    if selected_language == "Luganda":
        combo1.set("Luo")
        label1.configure(text="Luo")
    elif selected_language == "Luo":
        combo1.set("Luganda")
        label1.configure(text="Luganda")

def translate_now():
    text_ = text1.get(1.0, END)
    t1 = Translator()
    trans_text = t1.translate(text_, src=combo1.get(), dest=combo2.get())
    trans_text = trans_text.text

    text2.delete(1.0, END)
    text2.insert(END, trans_text)

def listen_audio():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source)

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

languages = ["Luganda", "Luo"]

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

# first frame
f = Frame(root, bg="black", bd=5)
f.place(x=10, y=118, width=440, height=210)

text1 = Text(f, font="Roboto 20", bg="white", relief=GROOVE, wrap=WORD)
text1.place(x=0, y=0, width=430, height=200)

scrollbar1 = Scrollbar(f)
scrollbar1.pack(side="right", fill='y')

scrollbar1.configure(command=text1.yview)
text1.configure(yscrollcommand=scrollbar1.set)

# microphone button
microphone_button = Button(f, text="\u23f0", font=("Arial", 15), bd=0, bg="black", fg="white", activebackground="grey", command=listen_audio)
microphone_button.place(x=10, y=165)

# second frame
f1 = Frame(root, bg="black", bd=5)
f1.place(x=620, y=118, width=440, height=210)

text2 = Text(f1, font="Roboto 20", bg="white", relief=GROOVE, wrap=WORD)
text2.place(x=0, y=0, width=430, height=200)

scrollbar2 = Scrollbar(f1)
scrollbar2.pack(side="right", fill='y')

scrollbar2.configure(command=text2.yview)
text2.configure(yscrollcommand=scrollbar2.set)

# speaker button
speaker_button = Button(f1, text="\U0001f508", font=("Arial", 15), bd=0, bg="black", fg="white", activebackground="grey", command=speak_text)
speaker_button.place(x=400, y=165)

# translate button
translate = Button(root, text="Translate", font=("Roboto", 15), activebackground="white", cursor="hand2",
                   bd=1, width=10, height=2, bg="black", fg="white", command=translate_now)
translate.place(x=467, y=250)

label_change()
root.mainloop()
