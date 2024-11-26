from flask import Flask, render_template, request, jsonify
from werkzeug.utils import secure_filename
import os
import openai

openai.api_key = os.getenv("OPENAI_API_KEY")

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def get_answer(question):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant,when the question is about religion dont return answer and say sorry"},
                {"role": "user", "content": question}
            ],
            max_tokens=150,
            temperature=0.7)
        answer = response.choices[0].message['content'].strip()
        return answer
    except Exception as e:
        return f"An error occurred: {e}"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'audio' not in request.files:
        return jsonify({'error': 'No audio file found in the request'}), 400
    
    file = request.files['audio']
    if file.filename == '':
        return jsonify({'error': 'No filename provided'}), 400
    
    filename = secure_filename(file.filename)
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(filepath)

    try:
        with open(filepath, "rb") as audiofile:
            trans = openai.Audio.transcribe(
                model="whisper-1",
                file=audiofile
            )
            tr = trans.get('text', 'Transcription failed')
    except Exception as e:
        return jsonify({'error': str(e)}), 500

    
    ans = get_answer(tr)
    
    # Send the answer to the frontend
    return jsonify({'answer': ans}), 200

if __name__ == '__main__':
    app.run(debug=True)
