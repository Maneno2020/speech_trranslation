# import speech_recognition as sr
#
# def recognize_luganda_speech():
#     recognizer = sr.Recognizer()
#     with sr.Microphone() as source:
#         print("Say something...")
#         audio = recognizer.listen(source)
#
#     try:
#         # Recognize speech using Google Web Speech API
#         recognized_text = recognizer.recognize_google(audio, language="lg-UG")
#         print("You said:", recognized_text)
#     except sr.UnknownValueError:
#         print("Google Web Speech API could not understand the audio.")
#     except sr.RequestError as e:
#         print("Could not request results from Google Web Speech API; {0}".format(e))
#
#
# if __name__ == "__main__":
#     recognize_luganda_speech()
#
# import speech_recognition as sr
#
# # Create a recognizer instance
# recognizer = sr.Recognizer()
#
# # Set the default microphone as the audio source
# microphone = sr.Microphone()
#
# # Adjust for ambient noise levels
# with microphone as source:
#     recognizer.adjust_for_ambient_noise(source)
#
# # Capture speech from the microphone
# with microphone as source:
#     print("Speak something in Luganda...")
#     audio = recognizer.listen(source)
#
# # Recognize Luganda speech using Google Speech Recognition
# try:
#     print("Transcribing...")
#     text = recognizer.recognize_google(audio, language="lg")
#     print("Transcription:", text)
# except sr.UnknownValueError:
#     print("Could not understand the audio.")
# except sr.RequestError:
#     print("Could not connect to Google Speech Recognition service.")

# import requests
#
# API_URL = "https://api-inference.huggingface.co/models/akera/whisper-small-luganda"
# headers = {"Authorization": f"Bearer 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"}
#
# def query(filename):
#     with open(filename, "rb") as f:
#         data = f.read()
#     response = requests.post(API_URL, headers=headers, data=data)
#     return response.json()
#
#
# output = query("luganda.wav")
# print(output)

import requests

url = "https://sunbird-ai-api-5bq6okiwgq-ew.a.run.app/tasks/stt"

payload = {}
files = [
    ('audio', ('luganda.wav', open('luganda.wav', 'rb'), 'audio/wav'))
]
headers = {
    'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJtYW5lbm8yMDIwIiwiZXhwIjo0ODQyMzE2MDYyfQ'
                     '.elEqO4FYZRlfKBYJI8S1ojcwHSzA9GAjLydONqPy8-0'
}

response = requests.request("POST", url, headers=headers, data=payload, files=files)

print(response.text)
