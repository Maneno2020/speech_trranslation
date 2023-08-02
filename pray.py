import requests
import sounddevice as sd
import soundfile as sf
import tempfile
import numpy as np

url = "https://sunbird-ai-api-5bq6okiwgq-ew.a.run.app/tasks/stt"
headers = {
    'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJtYW5lbm8yMDIwIiwiZXhwIjo0ODQyMzE2MDYyfQ'
                     '.elEqO4FYZRlfKBYJI8S1ojcwHSzA9GAjLydONqPy8-0'
}

# Define the recording parameters
duration = 10  # Recording duration in seconds
sample_rate = 16000  # Sample rate

# Record audio from the microphone
print("Recording...")
audio = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=1)
sd.wait()  # Wait until recording is finished
print("Recording finished.")

# Convert audio data to 16-bit signed integer
audio = np.squeeze(audio)
audio = (audio * 32767).astype(np.int16)

# Save the recorded audio to a temporary file
with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_file:
    filename = temp_file.name
    sf.write(filename, audio, sample_rate)

# Send the audio file to the API
files = [('audio', ('file.wav', open(filename, 'rb'), 'audio/wav'))]
response = requests.post(url, headers=headers, files=files)

print(response.text)



#
# import requests
# import soundfile as sf
#
# API_URL = "https://api-inference.huggingface.co/models/akera/whisper-small-luganda"
# headers = {"Authorization": f"Bearer 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", "Content-Type": "audio/wav"}
#
# def query(filename):
#     data, samplerate = sf.read(filename)
#     response = requests.post(API_URL, headers=headers, data=data.tobytes())
#     return response.json()
#
#
# output = query("luganda.wav")
# print(output)
# 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