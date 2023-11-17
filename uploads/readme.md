# `uploads` Directory

## Overview
This directory is an integral part of the Flask application designed for bird sound classification. It serves as a temporary storage location for audio files uploaded by users.

## Usage
- The Flask app saves uploaded audio files (WAV or MP3 formats) in this folder.
- These files are used for further processing, such as trimming and classification.
- After processing, the audio files can either be deleted or archived, depending on the application's configuration.

## File Management
- Temporary Storage: Files in this directory are meant for temporary use. They are subject to modification or deletion during the application's runtime.
- Security Note: Be cautious about the types of files stored here and their accessibility, as this folder is part of the web application.