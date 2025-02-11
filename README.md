**Sentiment Analysis System**

A full-stack Sentiment Analysis System that allows users to analyze the sentiment of text using:
1. Custom Model (DistilBERT fine-tuned on sentiment analysis)
2. Llama 3 via Groq API

Built with Flask for the backend and React for the frontend.

**Steps to run the Flask backend**
1. Install dependencies with pip install -r requirements.txt
2. Create an .env file and add: GROQ_API_KEY=your_groq_api_key_here
3. Then start the backend with python app.py

**Steps to run the React Frontend**
1. Run cd UI
2. Run npm install
3. Run npm start to run the UI. The React app will run at http://localhost:3001.

**How to use the endpoint**
The Flask API provides a POST endpoint for sentiment analysis.

POST http://127.0.0.1:3000/analyze

Example Request:
{
    "text": "I love this movie!",
    "model": "custom"
}

Sample cURL:
curl -X POST "http://127.0.0.1:3000/analyze" \
-H "Content-Type: application/json" \
-d '{"text": "I love this movie!", "model": "custom"}'

