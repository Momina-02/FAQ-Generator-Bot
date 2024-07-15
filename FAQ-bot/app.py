# app.py
import os
from flask import Flask, request, jsonify, render_template
from dotenv import load_dotenv
import openai
import requests
import json

app = Flask(__name__)

# Load environment variables from .env file
load_dotenv()

# Access the API key from environment variables
openai.api_key = os.getenv('OPENAI_API_KEY')

# Define OpenAI API URL and headers
chatgpt_url = "https://api.openai.com/v1/chat/completions"
chatgpt_headers = {
    "content-type": "application/json",
    "Authorization": "Bearer {}".format(os.getenv('OPENAI_API_KEY'))  # Access API key from environment variable
}

# Example function to generate FAQs
def generate_faqs(text, count=3):
    prompt = f"""{text}
--------------------------
Generate {count} FAQs (frequently asked questions) from the above text. Generate a question and a corresponding answer."""

    messages = [
        {"role": "system", "content": "You are an experienced FAQ creator."},
        {"role": "user", "content": prompt}
    ]

    chatgpt_payload = {
        "model": "gpt-3.5-turbo-16k",
        "messages": messages,
        "temperature": 1.2,
        "max_tokens": 300,
        "top_p": 1,
        "stop": ["###"]
    }

    response = requests.request("POST", chatgpt_url, json=chatgpt_payload, headers=chatgpt_headers)
    response = response.json()
    faqs = []
    for choice in response['choices']:
        faq = {
            'q': choice['message']['content'],
            'a': 'Your answer here'  # You can fill this with actual answers if needed
        }
        faqs.append(faq)

    return faqs

# Flask routes
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/generate_faqs', methods=['POST'])
def handle_generate_faqs():
    data = request.json  # Assuming JSON data is sent from frontend
    text = data.get('text')
    count = int(data.get('count', 3))  # Default to 3 FAQs if count is not provided

    if not text:
        return jsonify({'error': 'No text provided'}), 400

    try:
        faqs = generate_faqs(text, count)
        return jsonify(faqs), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
