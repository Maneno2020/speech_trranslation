import requests
import base64

url = 'https://sunbird-ai-api-5bq6okiwgq-ew.a.run.app'

headers = {
    'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJtYW5lbm8yMDIwIiwiZXhwIjo0ODQyMzE2MDYyfQ'
                     '.elEqO4FYZRlfKBYJI8S1ojcwHSzA9GAjLydONqPy8-0',
    "Content-Type": "application/json"
}

payload = {
    "text": "Wasuze nnyo"
}
response = requests.post(f"{url}/tasks/tts", headers=headers, json=payload)

if response.status_code == 200:
    base64_string = response.json()["base64_string"]

    with open("temp.wav", "wb") as wav_file:
        decoded_audio = base64.decodebytes(base64_string.encode('utf-8'))
        wav_file.write(decoded_audio)
else:
    print("Error:", response.status_code, response.text)