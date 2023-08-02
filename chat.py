# import requests
#
# API_URL = "https://api-inference.huggingface.co/models/indonesian-nlp/wav2vec2-luganda"
# headers = {"Authorization": "Bearer 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"}
#
#
# def query(filename):
#     with open(filename, "rb") as f:
#         data = f.read()
#     response = requests.post(API_URL, headers=headers, data=data)
#     return response.json()
#
#
# output = query("whatsApp.wav")
# print(output)
#
# import requests
# import speech_recognition as sr
#
# API_URL = "https://api-inference.huggingface.co/models/indonesian-nlp/wav2vec2-luganda"
# headers = {"Authorization": "Bearer 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"}
#
#
# def recognize_luganda_speech_from_microphone():
#     recognizer = sr.Recognizer()
#     with sr.Microphone() as source:
#         print("Say something...")
#         audio = recognizer.listen(source)
#
#     # Save the captured audio to a temporary WAV file (optional).
#     with open("temp_audio.wav", "wb") as f:
#         f.write(audio.get_wav_data())
#
#     response = query("temp_audio.wav")
#     print(response)
#
#
# def query(filename):
#     with open(filename, "rb") as f:
#         data = f.read()
#     response = requests.post(API_URL, headers=headers, data=data)
#     return response.json()
#
#
# if __name__ == "__main__":
#     recognize_luganda_speech_from_microphone()


import requests
import speech_recognition as sr
import os

API_URL = "https://api-inference.huggingface.co/models/indonesian-nlp/wav2vec2-luganda"
headers = {"Authorization": "Bearer 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"}


def recognize_luganda_speech(audio_file_path):
    with open(audio_file_path, "rb") as f:
        data = f.read()
    response = requests.post(API_URL, headers=headers, data=data)
    return response.json()


def save_microphone_audio():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Say something...")
        audio = recognizer.listen(source)

    # Save the captured audio to a temporary WAV file.
    temp_audio_file = "temp_audio.wav"
    with open(temp_audio_file, "wb") as f:
        f.write(audio.get_wav_data())

    return temp_audio_file


if __name__ == "__main__":
    # Step 1: Record audio from the microphone and save it as a temporary file
    temp_audio_file = save_microphone_audio()

    # Step 2: Use the pre-recorded audio file for transcription
    output = recognize_luganda_speech(temp_audio_file)
    print(output)

    # Step 3: Clean up - delete the temporary audio file
    if os.path.exists(temp_audio_file):
        os.remove(temp_audio_file)
