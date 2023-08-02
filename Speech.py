import io
from google.cloud import speech_v1p1beta1 as speech


def transcribe_luganda_speech(file_path):
    # Set up the client
    client = speech.SpeechClient()

    # Read the audio file
    with io.open(file_path, "rb") as audio_file:
        content = audio_file.read()

    # Configure the audio request
    audio = speech.RecognitionAudio(content=content)
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000,
        language_code="lg-UG",  # Luganda language code
    )

    # Send the audio request to the API
    response = client.recognize(config=config, audio=audio)

    # Process the API response
    transcripts = []
    for result in response.results:
        transcript = result.alternatives[0].transcript
        transcripts.append(transcript)

    return transcripts


# Provide the path to the recorded audio file in your system
audio_file_path = "Pytorch\luganda.wav"

# Transcribe the Luganda speech
transcriptions = transcribe_luganda_speech(audio_file_path)

# Print the transcriptions
for transcript in transcriptions:
    print(transcript)
