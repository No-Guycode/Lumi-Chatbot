from flask import Flask, request, jsonify, render_template
import openai
import os

app = Flask(__name__)

# Ensure OpenAI API Key is set
if not os.getenv("OPENAI_API_KEY"):
    raise ValueError("Missing OpenAI API Key. Set OPENAI_API_KEY in environment variables.")

openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/query', methods=['POST'])
def query():
    data = request.json
    messages = data.get("messages", [])
    model = data.get("model", "gpt-4o")  # Default to GPT-4o

    if not messages:
        return jsonify({'response': 'Please enter a message.'})

    try:
        response = openai.ChatCompletion.create(
            model=model,  # Use the selected model
            messages=messages
        )
        bot_reply = response["choices"][0]["message"]["content"]
        return jsonify({'response': bot_reply})
    except Exception as e:
        return jsonify({'response': f'Error: {str(e)}'})

if __name__ == '__main__':
    app.run(debug=True)
