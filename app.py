from flask import Flask, flash, request, redirect, render_template, send_from_directory
import os
from pydub import AudioSegment
import time

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'wav', 'mp3'}
BIRDS = {0:"macburn", 1:"loptus"}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = 'supersecretkey'

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def trim_audio(file):
    # Determine the file extension
    file_extension = file.filename.rsplit('.', 1)[1].lower()

    # Define the converted filename
    converted_filename = 'uploaded_audio.wav'
    converted_file_path = os.path.join(app.config['UPLOAD_FOLDER'], converted_filename)

    if file_extension == 'mp3':
        # Load the MP3 file
        audio = AudioSegment.from_mp3(file.filename)
        # Convert to WAV and save
        audio.export(converted_file_path, format="wav")
    elif file_extension == 'wav':
        # If it's already a WAV file, save it in the upload folder
        file.save(converted_file_path)

    return converted_filename
    

def save(file):
    filename = 'uploaded_audio.wav' #+ file.filename.rsplit('.', 1)[1].lower()
    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

    return filename

def model_process(audio):
    output = "Malera"
    precision = 0.86
    return output, precision

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            timestamp = int(time.time()*1000)
            filename = f'{timestamp}_uploaded_audio'
            # file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            # filename = 'uploaded_audio.wav'  # + file.filename.rsplit('.', 1)[1].lower()
            # filename = trim_audio(file.filename)
            file_extension = file.filename.rsplit('.', 1)[1].lower()
            # Path where the uploaded file will be saved
            upload_path = os.path.join(app.config['UPLOAD_FOLDER'], f'{filename}.{file_extension}')


            # Save the original audio file
            file.save(upload_path)

            
            # # Load the audio file
            if file_extension == 'mp3':
                audio = AudioSegment.from_mp3(upload_path)
            else:
                audio = AudioSegment.from_file(upload_path, format='wav')
            

            # # Check if audio is shorter than 10 seconds (10000 milliseconds)
            if len(audio) < 10000:
                # Handle shorter audio - maybe skip trimming or do something else
                # For example, just use the original audio
                trimmed_audio = audio[:10000]
            else:
                # Trim to the first 10 seconds
                trimmed_audio = audio[:10000]
            
            #Process the audio file:
            bird, accuracy = model_process(trimmed_audio)


            # # Save the trimmed or original audio
            trimmed_audio_filename = f'trimmed_{filename}.wav'
            trimmed_audio_path = os.path.join(app.config['UPLOAD_FOLDER'], trimmed_audio_filename)
            trimmed_audio.export(trimmed_audio_path, format='wav')

            return render_template('index.html', filename=trimmed_audio_filename, bird=bird, accuracy=accuracy)
    return render_template('index.html')

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


if __name__ == '__main__':
    app.run(debug=True)