from flask import Flask, request, jsonify, render_template
import openai
import os
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

app = Flask(__name__)

# Set OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")

# Initialize rate limiter (works with Koyeb)
limiter = Limiter(
    key_func=lambda: request.headers.get("X-Forwarded-For", get_remote_address()),  # Works on Koyeb
    app=app,
    default_limits=["5 per minute"]  # Change as needed
)

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/query', methods=['POST'])
@limiter.limit("5 per minute")  # Limit users to 5 messages per minute
def query():
    data = request.json
    messages = data.get("messages", [])
    model = data.get("model", "gpt-3.5-turbo")  # Default to GPT-3.5 Turbo

    if not messages:
        return jsonify({'response': 'Please enter a message.'})

    try:
        client = openai.OpenAI(api_key=openai.api_key)
        response = client.chat.completions.create(
            model=model,
            messages=messages
        )
        bot_reply = response.choices[0].message.content
        return jsonify({'response': bot_reply})
    except Exception as e:
        return jsonify({'response': f'Error: {str(e)}'})

@app.errorhandler(429)
def ratelimit_error(e):
    return jsonify({'response': 'Rate limit exceeded. Please wait a moment and try again.'}), 429

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
