from flask import Flask, request, jsonify
import google.generativeai as genai
import ffmpeg
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
# NOTE: padb110412



def _summarize(audio_file_path):
    try:
        # Initialize a Gemini model
        model = genai.GenerativeModel('models/gemini-1.5-flash')

        prompt = """
        Please summarize the contents of the audio. Return compact JSON in this format with no
        markdown. If you cannot find a certain piece of information set it to null.\n
        {first_name: str, last_name: str, age: int, profession: str, date_recorded: Date, children: [{ first_name: str, last_name: str, age: int}]}
        """

        # Send file to Gemini API
        myfile = genai.upload_file(audio_file_path)
        result = model.generate_content([myfile, prompt])
        print(f"{result.text=}")

        # Output Gemini's response
        return result.text
    
    except Exception as e:
        return f"Error summarizing audio: {e}"



@app.route('/upload', methods=['POST'])
def upload_audio():
    # Check if audio file is present in the request
    if 'audio' not in request.files:
        return jsonify({'error': 'No audio file provided'}), 400

    audio_file = request.files['audio']

    # Create a temporary file for the audio
    mp3_filename = f'./tmp/temp.mp3'
    if (audio_file.mimetype == 'audio/mpeg' or audio_file.mimetype == 'audio/mp3'):
        audio_file.save(mp3_filename)
    else:
        temp_path = f'./tmp/temp'
        audio_file.save(temp_path)

        # Use ffmpeg to convert webm to mp3
        input_stream = ffmpeg.input(temp_path)
        output_stream = input_stream.output(mp3_filename)
        output_stream.run(overwrite_output=True)

    # Send the MP3 file to Gemini API for summarization (replace with your Gemini API logic)
    response = _summarize(mp3_filename)

    return jsonify({'message': response})



if __name__ == '__main__':
    app.run()