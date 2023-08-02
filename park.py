import requests

API_URL = "https://api-inference.huggingface.co/models/ak3ra/wav2vec2-sunbird-speech-lug"
headers = {"Authorization": f"Bearer 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"}

def query(filename):
    with open(filename, "rb") as f:
        data = f.read()
    response = requests.post(API_URL, headers=headers, data=data)
    return response.json()


output = query("luganda.wav")
print(output)