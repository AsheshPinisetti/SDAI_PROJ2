from flask import Flask, flash, request, redirect, render_template, send_from_directory
import os
from pydub import AudioSegment
import time

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'wav', 'mp3'}
BIRDS = {0: 'aldfly', 1: 'ameavo', 2: 'amebit', 3: 'amecro', 4: 'amegfi', 5: 'amekes', 
         6: 'amepip', 7: 'amered', 8: 'amerob', 9: 'amewig', 10: 'amewoo', 11: 'amtspa', 
         12: 'annhum', 13: 'astfly', 14: 'baisan', 15: 'baleag', 16: 'balori', 17: 'banswa', 
         18: 'barswa', 19: 'bawwar', 20: 'belkin1', 21: 'belspa2', 22: 'bewwre', 23: 'bkbcuc', 
         24: 'bkbmag1', 25: 'bkbwar', 26: 'bkcchi', 27: 'bkchum', 28: 'bkhgro', 29: 'bkpwar', 
         30: 'bktspa', 31: 'blkpho', 32: 'blugrb1', 33: 'blujay', 34: 'bnhcow', 35: 'boboli', 
         36: 'bongul', 37: 'brdowl', 38: 'brebla', 39: 'brespa', 40: 'brncre', 41: 'brnthr', 
         42: 'brthum', 43: 'brwhaw', 44: 'btbwar', 45: 'btnwar', 46: 'btywar', 47: 'buffle', 
         48: 'buggna', 49: 'buhvir', 50: 'bulori', 51: 'bushti', 52: 'buwtea', 53: 'buwwar'}



app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = 'supersecretkey'

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def model_process(audio):
    result = 0
    precision = 0.86909
    return BIRDS[result], f'{precision:.2f}'


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
            

            # # # Check if audio is shorter than 10 seconds (10000 milliseconds)
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