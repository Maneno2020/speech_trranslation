import requests
import speech_recognition as sr
import os
import time

API_URL = "https://api-inference.huggingface.co/models/indonesian-nlp/wav2vec2-luganda"
headers = {"Authorization": "Bearer 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"}


def recognize_luganda_speech(audio_file_path):
    with open(audio_file_path, "rb") as f:
        data = f.read()
    response = requests.post(API_URL, headers=headers, data=data)
    return response.json()


def save_microphone_audio(timeout=10):
    recognizer = sr.Recognizer()

    # Delete the previous temporary audio file if it exists
    temp_audio_file = "temp.wav"
    if os.path.exists(temp_audio_file):
        os.remove(temp_audio_file)

    with sr.Microphone() as source:
        print(f"Say something... (recording for {timeout} seconds)")
        try:
            # Adjust the timeout value to capture audio for the desired duration
            audio = recognizer.listen(source, timeout=timeout)
        except sr.WaitTimeoutError:
            return None

    # Save the captured audio to a new temporary WAV file.
    with open(temp_audio_file, "wb") as f:
        f.write(audio.get_wav_data())

    return temp_audio_file


if __name__ == "__main__":
    # Step 1: Record audio from the microphone and save it as a temporary file
    recording_duration = 5  # Adjust the recording duration (in seconds) as needed
    temp_audio_file = save_microphone_audio(timeout=recording_duration)

    if temp_audio_file:
        # Step 2: Use the pre-recorded audio file for transcription
        output = recognize_luganda_speech(temp_audio_file)

        if output:
            print(output)
        else:
            print("Error occurred during recognition.")

        # Step 3: Clean up - delete the temporary audio file
        if os.path.exists(temp_audio_file):
            os.remove(temp_audio_file)

    else:
        print("No sound detected.")
