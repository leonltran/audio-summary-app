from flask import Flask, request, jsonify
from flask_cors import CORS
import google.generativeai as genai
import ffmpeg
from dotenv import load_dotenv
import sqlite3
import json

load_dotenv()

app = Flask(__name__)
# NOTE: padb110412
CORS(app)


def _summarize(audio_file_path, prompt):
    try:
        # Initialize a Gemini model
        model = genai.GenerativeModel('models/gemini-1.5-flash')

        # Send file to Gemini API
        myfile = genai.upload_file(audio_file_path)
        result = model.generate_content([myfile, prompt])
        print(f"{result.text=}")

        # Output Gemini's response
        return result.text
    
    except Exception as e:
        return f"Error summarizing audio: {e}"

def _save_to_db(json_data):
    db_name = "people_info.db"

    try:
        # Connect to the SQLite database
        conn = sqlite3.connect(db_name)
        cursor = conn.cursor()

        # Parse the JSON string
        data = json.loads(json_data)

        # Create the `users` table (if it doesn't exist)
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        first_name TEXT,
        last_name TEXT,
        age INTEGER,
        profession TEXT,
        date_recorded TEXT
        )""")

        # Create the `children` table (if it doesn't exist)
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS children (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        parent_id INTEGER,
        first_name TEXT,
        last_name TEXT,
        age INTEGER,
        FOREIGN KEY (parent_id) REFERENCES users (id)
        )""")

        # Insert data into the `users` table
        sql = "INSERT INTO users (first_name, last_name, age, profession, date_recorded) VALUES (?, ?, ?, ?, ?)"
        val = (
            data.get('first_name'),
            data.get('last_name'),
            data.get('age'),
            data.get('profession'),
            data.get('date_recorded')
        )
        cursor.execute(sql, val)
        user_id = cursor.lastrowid # Get the ID of the inserted user

        # Insert data into the `children` table for each child
        for child in data.get('children'):
            child_sql = "INSERT INTO children (parent_id, first_name, last_name, age) VALUES (?, ?, ?, ?)"
            child_val = (
                user_id, 
                child.get('first_name'), 
                child.get('last_name'), 
                child.get('age')
            )
            cursor.execute(child_sql, child_val)

        # Commit the changes
        conn.commit()

    except (sqlite3.Error, json.JSONDecodeError) as e:
        # Handle database errors or invalid JSON data
        print(f"Error occurred: {e}")
        # Consider logging the error or taking other actions
    finally:
        # Close the connection, even if an error occurred
        if conn:
            conn.close()



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
    prompt = """
        Please summarize the contents of the audio. Return compact JSON in this format:\n
        {first_name: str, last_name: str, age: int, profession: str, date_recorded: Date, children: [{ first_name: str, last_name: str, age: int}]}\n
        If you cannot find a certain piece of information set it to null. DO NOT INCLUDE ANY MARKDOWN.
        """
    response = _summarize(mp3_filename, prompt)
    _save_to_db(response)

    return jsonify({'message': response})



@app.route('/summarize', methods=['POST'])
def summarize_audio():
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
    prompt = "Please summarize the contents of the audio."
    response = _summarize(mp3_filename, prompt)

    return jsonify({'message': response})



@app.route('/contacts', methods=['GET'])
def fetch_all():
    db_name = "people_info.db"
    try:
        # Connect to the SQLite database
        conn = sqlite3.connect(db_name)
        cursor = conn.cursor()

        # Fetch data from both tables
        user_sql = "SELECT * FROM users"
        cursor.execute(user_sql)
        users = cursor.fetchall()

        children_sql = "SELECT * FROM children"
        cursor.execute(children_sql)
        children = cursor.fetchall()

        # Combine user and child data
        results = []
        for user in users:
            user_id = user[0]
            user_data = {
                "first_name": user[1],
                "last_name": user[2],
                "age": user[3],
                "profession": user[4],
                "date_recorded": user[5],
                "children": []
            }
            for child in children:
                if child[1] == user_id:
                    user_data["children"].append({
                        "first_name": child[2],
                        "last_name": child[3],
                        "age": child[4]
                    })
            results.append(user_data)

        return results

    except sqlite3.Error as e:
        print(f"Error occurred: {e}")
    finally:
        if conn:
            conn.close()

if __name__ == '__main__':
    app.run()