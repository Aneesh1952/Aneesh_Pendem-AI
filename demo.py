import openai
import os
from openai import OpenAI
from pathlib import Path
from flask import Flask, request, jsonify, render_template
import time

api_key = "use your openai key here"


api_key = "sk-proj-q0cd6SvAEg4kqOr2z7UBT3BlbkFJpf05aKcQhN3B56vjY4wp"
client = OpenAI(api_key=api_key)

app = Flask(__name__)


def generate_response(question):
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are President Biden answering questions. Give answer without line breaks. Use umm, aahs and breathing sound to make it more realistic."},
            {"role": "user", "content": question}
        ]
    )
    return response.choices[0].message.content.strip()

def text_to_speech(text, output_file):
    response = client.audio.speech.create(
        model="tts-1",
        voice="onyx",  # Choose the desired voice: alloy, echo, fable, onyx, nova, shimmer
        input=text
    )
    response.stream_to_file(output_file)

def create_lip_synced_video(video_path, audio_path, output_path):
    command = f"python Wav2Lip/inference.py --checkpoint_path checkpoints/wav2lip_gan.pth --face {video_path} --audio {audio_path} --outfile {output_path}"
    os.system(command)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    question = request.form['question']
    ai_response = generate_response(question)
    
    # Generate unique filenames using timestamp
    timestamp = int(time.time())
    audio_file = Path(f"static/ai_response_{timestamp}.mp3")
    output_video = Path(f"static/ai_biden_response_{timestamp}.mp4")
    
    text_to_speech(ai_response, audio_file)
    
    video_file = "your_biden_video.mp4"  # Replace with the path to the video of President Biden
    create_lip_synced_video(video_file, audio_file, output_video)
    
    return jsonify({
        "response": ai_response,
        "audio": str(audio_file),
        "video": str(output_video)
    })

if __name__ == "__main__":
    app.run(debug=True)