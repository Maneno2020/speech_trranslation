import sounddevice as sd
import soundfile as sf
import requests
import tempfile

API_URL = "https://api-inference.huggingface.co/models/indonesian-nlp/wav2vec2-luganda"
headers = {"Authorization": "Bearer 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"}


def query(filename):
    with open(filename, "rb") as f:
        data = f.read()
    response = requests.post(API_URL, headers=headers, data=data)
    return response.json()


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
output = query(filename)
print(output)
