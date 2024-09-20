# %%
from flask import Flask, request, jsonify
from flask_cors import CORS
import google.generativeai as genai
import firebase_admin
from firebase_admin import credentials

cred = credentials.Certificate("./langchain-testing-e55cd-firebase-adminsdk-vedpa-95f28a728d.json")
firebase_admin.initialize_app(cred)

app = Flask(__name__)
CORS(app)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route('/upload', methods=['POST'])
def upload_audio():
    # Check if audio file is present in the request
    if 'audio' not in request.files:
        return jsonify({'error': 'No audio file provided'}), 400

    audio_file = request.files['audio']

    # Check if file is a valid audio file (optional)
    if audio_file.filename == '':
        return jsonify({'error': 'No selected audio file'}), 400

    # Save the audio file to a desired location (adjust as needed)
    audio_file.save('uploads/' + audio_file.filename + '.webm')

    # Process the audio file (e.g., transcribe, analyze)
    # ...

    return jsonify({'message': 'Audio file uploaded successfully'})

if __name__ == '__main__':
    app.run()