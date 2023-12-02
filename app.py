from flask import Flask, flash, request, redirect, render_template, send_from_directory
import os
from pydub import AudioSegment
import time
import pandas as pd
from sklearn.model_selection import train_test_split
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import librosa
import librosa.display
import numpy as np
from PIL import Image
from keras.preprocessing.image import img_to_array
from keras.models import load_model

os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'
model = load_model('bird_classification_model.h5')



model = load_model('bird_classification_model.h5')


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


def spectral_gate(filename, audio_dir, threshold=20, frame_length=2048, hop_length=512, target_size=(128, 128)):
    y, sr = librosa.load(audio_dir, sr=None)
    stft = librosa.stft(y, n_fft=frame_length, hop_length=hop_length)
    magnitude, phase = librosa.magphase(stft)
    magnitude_db = librosa.amplitude_to_db(magnitude)

    mask = magnitude_db > threshold
    magnitude_db_filtered = magnitude_db * mask
    filtered_magnitude = librosa.db_to_amplitude(magnitude_db_filtered)
    y_filtered = librosa.istft(filtered_magnitude * phase, hop_length=hop_length)

    S = librosa.feature.melspectrogram(y=y_filtered, sr=sr)
    S_DB = librosa.power_to_db(S, ref=np.max)
    
    # Save the spectrogram to a file
    spectrogram_path = os.path.join(app.config['UPLOAD_FOLDER'], f'{filename}.png')
    # spectrogram_path = 'temp.png' #path to save the image
    plt.figure(figsize=(10, 4))
    librosa.display.specshow(S_DB, sr=sr, x_axis='time', y_axis='mel')
    plt.axis('off')
    plt.savefig(spectrogram_path, bbox_inches='tight', pad_inches=0)
    plt.close()

    # Open the saved spectrogram and resize
    img = Image.open(spectrogram_path)
    # img = img.resize(target_size, Image.ANTIALIAS)
    img = img.resize(target_size, Image.Resampling.LANCZOS)

    # Convert to array and normalize
    img_array = img_to_array(img)
    img_array = img_array / 255.0

    return [img_array]

def dataset(filename, audio_dir):
    spectrograms = []
    spectrogram = spectral_gate(filename, audio_dir)
    spectrograms.append(spectrogram)
    return np.array(spectrograms)


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

            # # Save the trimmed or original audio
            trimmed_audio_filename = f'trimmed_{filename}.wav'
            trimmed_audio_path = os.path.join(app.config['UPLOAD_FOLDER'], trimmed_audio_filename)
            trimmed_audio.export(trimmed_audio_path, format='wav')

            # Treat the audio file
            # audio_dir = 'XC133080.wav' # give the audio path here
            spectrograms = dataset(trimmed_audio_filename, trimmed_audio_path)
            spectrogram = spectrograms[0]
            prediction = model.predict(spectrogram)
            predicted_label = np.argmax(prediction, axis=1)
            pred = predicted_label[0] - 1 #offset
            bird = BIRDS[pred]


        return render_template('index.html', filename=trimmed_audio_filename, bird=bird)
    return render_template('index.html')

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


if __name__ == '__main__':
    app.run(debug=True)