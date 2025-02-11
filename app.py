from flask import Flask, request, jsonify
from transformers import AutoModelForSequenceClassification, AutoTokenizer
from flask_cors import CORS
import torch
import torch.nn.functional as F
import requests
import os
from groq import Client
from dotenv import load_dotenv

app = Flask(__name__)
CORS(app)
load_dotenv()


CUSTOM_MODEL = "Amna1917e81729/fine-tuned-imdb-sentiment-model"
CUSTOM_TOKENIZER = "Amna1917e81729/fine-tuned-imdb-sentiment-tokenizer"
tokenizer = AutoTokenizer.from_pretrained(CUSTOM_TOKENIZER)
model = AutoModelForSequenceClassification.from_pretrained(CUSTOM_MODEL)

groq_api_key = os.getenv("GROQ_API_KEY")

client = Client(api_key=groq_api_key)

def analyze_sentiment_custom(text):
    inputs = tokenizer(text, truncation=True, padding="max_length", max_length=256, return_tensors="pt")
    with torch.no_grad():
        logits = model(**inputs).logits
    probabilities = F.softmax(logits, dim=1).squeeze().tolist()
    sentiment = "positive" if probabilities[1] > probabilities[0] else "negative"
    confidence = max(probabilities)
    return sentiment, confidence

def analyze_sentiment_llama(text):
    if not groq_api_key:
        return "error", "Groq API key missing"

    prompt = f"""
        You are an AI that performs sentiment analysis. 
        Analyze sentiment: '{text}'. 
        Reply with 'positive' or 'negative' and a confidence score between 0 and 1. 
        ALWAYS only return 2 values, and just put space between the two values: 
        1. A string indicating whether the sentiment is 'positive' or 'negative'. 
        2. A numerical confidence score.
    """


    try:
        response = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
            model="llama3-8b-8192",
        )
        print(response)

    except Exception as e:
        return jsonify({'error': 'Llama failed', 'details': str(e)}), 500

    
    sentiment = response.choices[0].message.content.strip()

    # Extract sentiment and confidence score (Expected format: "positive 0.9" or "negative 0.7")
    parts = sentiment.split()
    if len(parts) == 2:
        sentiment = parts[0]
        try:
            confidence = float(parts[1])
            return sentiment, confidence
        except ValueError:
            return "error", "Invalid confidence score format"
    return "error", "Unexpected response format"

    return "error", f"Groq API error: {response.text}"

@app.route('/analyze', methods=['POST'])
def analyze():
    data = request.json
    if "text" not in data or "model" not in data:
        return jsonify({"error": "Missing 'text' or 'model' parameter"}), 400

    text = data["text"]
    model_choice = data["model"]

    if model_choice == "custom":
        sentiment, confidence = analyze_sentiment_custom(text)
    elif model_choice == "llama":
        sentiment, confidence = analyze_sentiment_llama(text)
    else:
        return jsonify({"error": "Invalid model choice. Use 'custom' or 'llama'."}), 400

    if sentiment == "error":
        return jsonify({"error": confidence}), 500

    return jsonify({
        "sentiment": sentiment,
        "confidence": round(confidence, 4)
    })

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=3000, debug=True)
