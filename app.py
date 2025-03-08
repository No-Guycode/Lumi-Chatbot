from flask import Flask, request, jsonify, render_template
import openai
import os

app = Flask(__name__)

# Set your OpenAI API key here
openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/query', methods=['POST'])
def query():
    user_prompt = request.form.get('prompt', '')
    if not user_prompt:
        return jsonify({'response': 'Please enter a message.'})
    
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",  # Change to "gpt-3.5-turbo" for a cheaper option
            messages=[{"role": "system", "content": "You are Lumi, a helpful chatbot."},
                      {"role": "user", "content": user_prompt}]
        )
        bot_reply = response['choices'][0]['message']['content']
        return jsonify({'response': bot_reply})
    except Exception as e:
        return jsonify({'response': f'Error: {str(e)}'})

if __name__ == '__main__':
    app.run(debug=True)
