from flask import Flask, render_template, request, jsonify
from werkzeug.utils import secure_filename
import os
from openai import OpenAI

# Initialize Flask app
app = Flask(__name__)

# Configure upload folder
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Initialize OpenAI client
client = OpenAI(
    # This will automatically read from OPENAI_API_KEY environment variable
    # Alternatively, you can pass the API key directly:
    # api_key="your-api-key-here"
)

def get_answer(question):
    """
    Get an answer from OpenAI's chat completion API
    
    Args:
        question (str): The user's question
    
    Returns:
        str: The AI's response or an error message
    """
    try:
        # Updated method for creating chat completion
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": question}
            ],
            max_tokens=150,
            temperature=0.7
        )
        
        # Updated way of accessing response content
        answer = response.choices[0].message.content.strip()
        return answer
    except Exception as e:
        return f"An error occurred: {e}"

@app.route('/')
def index():
    """
    Render the main index page
    """
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    """
    Handle audio file upload, transcription, and get AI response
    """
    # Check if audio file is present
    if 'audio' not in request.files:
        return jsonify({'error': 'No audio file found in the request'}), 400
    
    file = request.files['audio']
    
    # Check if filename is empty
    if file.filename == '':
        return jsonify({'error': 'No filename provided'}), 400
    
    # Secure and save the filename
    filename = secure_filename(file.filename)
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(filepath)
    
    try:
        # Open the file for transcription
        with open(filepath, "rb") as audiofile:
            # Updated transcription method
            trans = client.audio.transcriptions.create(
                model="whisper-1", 
                file=audiofile
            )
        
        # Get transcribed text
        tr = trans.text
        
        # Get AI answer based on transcription
        ans = get_answer(tr)
        
        # Send the answer to the frontend
        return jsonify({'answer': ans}), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)