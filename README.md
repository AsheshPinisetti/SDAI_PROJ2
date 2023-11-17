# SDAI_PROJ2
# Bird Sound Classifier App
Description
This Flask application allows users to upload an audio file (in WAV or MP3 format) to classify bird sounds. The app identifies specific bird species based on their vocalizations using a pre-trained machine learning model.

## Features
File Upload: Users can upload audio files in WAV or MP3 format.
Audio Processing: The app processes audio files, converting MP3s to WAV format if necessary.
Bird Sound Classification: The application predicts the bird species from the audio file.

## Online Access
Deployment on Heroku
The deployed application can be accessed at [Heroku-App-URL].


## Local Access
To run this application on your local machine, you need to have Python installed. Follow these steps:

1. Clone the repository to your local machine:
```
git clone https://github.com/AsheshPinisetti/SDAI_Proj2.git
cd SDAI_Proj2
```

2. Install the required packages:
- Python 3.x
- Flask
- NumPy
- Tensorflow
```
pip install Flask Pillow numpy tensorflow
```
Run the Flask application:

```
python app.py
```
3. Usage
Once the application is running open your web browser and go to [http://127.0.0.1:5000/].
Use the interface to upload an audio file.
The application will process the file and display the classification result.


## License
This project is licensed under the MIT License - see the LICENSE file for details.
