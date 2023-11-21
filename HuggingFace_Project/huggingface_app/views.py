from django.shortcuts import render
from .models import UserInput
import requests

# Define separate API URLs and headers for each model
NLP_API_URL = "https://api-inference.huggingface.co/models/finiteautomata/bertweet-base-sentiment-analysis"
AUDIO_API_URL = "https://api-inference.huggingface.co/models/facebook/mms-tts-eng"
VISION_API_URL = "https://api-inference.huggingface.co/models/microsoft/swin-tiny-patch4-window7-224"

HEADERS = {"Authorization": "Bearer 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"}

def process_nlp_model(user_input):
    payload = {"inputs": user_input}
    response = requests.post(NLP_API_URL, headers=HEADERS, json=payload)

    if response.status_code == 200:
        result = response.json()
        return result
    else:
        return {"error": f"Error: {response.status_code}"}

def process_audio_model(user_input):
    payload = {"inputs": user_input}
    response = requests.post(AUDIO_API_URL, headers=HEADERS, json=payload)

    if response.status_code == 200:
        result = response.json()
        return result
    else:
        return {"error": f"Error: {response.status_code}"}

def process_vision_model(user_input, filename):
    with open(filename, "rb") as f:
        data = f.read()
        response = requests.post(VISION_API_URL, headers=HEADERS, data=data)

    if response.status_code == 200:
        result = response.json()
        return result
    else:
        return {"error": f"Error: {response.status_code}"}

def index(request):
    if request.method == 'POST':
        user_input = request.POST.get('text_input', '')
        filename = request.POST.get('image_file', '')  # Assuming you have a file input for vision model

        nlp_model_output = process_nlp_model(user_input)
        audio_model_output = process_audio_model(user_input)
        vision_model_output = process_vision_model(user_input, filename)

        UserInput.objects.create(text_input=user_input)

        return render(request, 'index.html', {
            'user_input': user_input,
            'nlp_model_output': nlp_model_output,
            'audio_model_output': audio_model_output,
            'vision_model_output': vision_model_output,
        })

    return render(request, 'index.html')
