from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/upload-audio', methods=['POST'])
def upload_audio():
    if 'audio_file' not in request.files:
        return jsonify({'error': 'No audio file provided'}), 400

    audio_file = request.files['audio_file']
    if audio_file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    # Generate a unique filename for the uploaded file
    filename = f'audio_{datetime.datetime.now().strftime("%Y%m%d_%H%M%S")}.{audio_file.filename.rsplit(".", 1)[1]}'

    # Create a reference to the desired location in your Cloud Storage bucket
    bucket = storage.bucket()
    blob = bucket.blob(filename)

    # Upload the file to Cloud Storage
    blob.upload_from_string(audio_file.read())

    return jsonify({'message': 'Audio file uploaded successfully', 'filename': filename}), 200