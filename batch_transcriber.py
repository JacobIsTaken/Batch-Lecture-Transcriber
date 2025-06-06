import os
import shutil
import subprocess
import time
from datetime import datetime, timedelta
import whisper

# Variables
recordings_folder = "recordings"    # Enter the folder containing the .mp4 files you want to transcribe, if doesnt exit it will be created automatically
extracted_folder = "extracted"      # Enter the folder where you want to save the transcriptions, if doesnt exit it will be created automatically
whisper_model = "turbo"             # Default 'Turbo', enter the model you want to use, use "small", "medium", "turbo" or "large" for better accuracy
whisper_language = "pl"             # Enter the language code for the model, use "en-US" for English (United States) or "pl" for Polish
media_extension = "all"             # Default 'all', enter what type of media do you want to convert, for example: "mp4", "webm" or enter "all" for all files (make sure the files can be transcribed)
delete_temp_mp3 = True              # Default 'True', choose whether to keep temporary mp3 file from ffmpeg

# Change the working directory to the script's directory
script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dir)
print(f"Working directory set to: {script_dir}")

# Ensure the extracted folder exists, if not, create it
if not os.path.exists(extracted_folder):
    print(f"The folder '{extracted_folder}' does not exist. Creating it now...")
    os.makedirs(extracted_folder)
    
# Ensure the recordings folder exists, if not, create it
if not os.path.exists(recordings_folder):
    print(f"The folder '{recordings_folder}' does not exist. Creating it now...")
    os.makedirs(recordings_folder)
    print(f"Please add your .{media_extension} files to the '{recordings_folder}' folder and run the script again.")
    time.sleep(10)
    exit(1)

# Check if there are any files in the recordings folder
if not os.listdir(recordings_folder):
    print(f"No files found in the '{recordings_folder}' folder. Please add your files and run the script again.")
    time.sleep(5)
    exit(1)
    
# Check if ffmpeg is installed
if not shutil.which("ffmpeg"):
    print("ffmpeg is not installed. Please install ffmpeg and try again.")
    time.sleep(5)
    exit(1)

# Load the model
try:
    model = whisper.load_model(whisper_model)
except Exception as e:
    print(f"Failed to load model: {e}")
    time.sleep(5)
    exit(1)
print("Loaded model:", whisper_model)

skip_if_all = media_extension == "all"

# Process each .mp4 file in the recordings folder
for file_name in os.listdir(recordings_folder):
    if file_name.endswith(f".{media_extension}") or skip_if_all:
        
        # 'all' media exception
        if skip_if_all:
            extension = file_name.split('.')[-1].lower()
        
        # Checking if proper extension
        if extension.isalnum():
            media_extension = extension
        else:
            print(f"ERROR: Invalid extension for media file, only alphanumeric characters allowed")
            break
        
        print(f"Processing \"{file_name}\"...")
        start_time = time.time()
        input_file_path = os.path.join(recordings_folder, file_name)
        audio_file_name = file_name.replace(f".{media_extension}", ".mp3")
        audio_file_path = os.path.join(recordings_folder, audio_file_name)
        
        # Convert the video to an audio file using ffmpeg
        subprocess.run([
            "ffmpeg", "-loglevel", "warning", "-i", input_file_path, 
            "-vn",                                              # Disable video
            "-ar", "16000",                                     # Set the audio sample rate to 16kHz
            "-ac", "1",                                         # Set the number of audio channels to 1 (mono)
            "-af", "loudnorm,highpass=f=200,lowpass=f=3000",    # Apply audio filters
            audio_file_path                                     # Output audio file path
        ], check=True)

        # Transcribe the audio file
        result = model.transcribe(audio_file_path, language=whisper_language)
        
        # Save the transcription to a file in the extracted folder
        output_file_path = os.path.join(extracted_folder, f"{file_name.replace(f'.{media_extension}', '')}_{whisper_model}.txt")
        with open(output_file_path, "w", encoding="utf-8") as f:
            f.write(result["text"])
        
        # Delete the audio file after transcription
        if delete_temp_mp3:
            os.remove(audio_file_path)
        
        end_time = time.time()
        duration = end_time - start_time
        
        # Log the duration of the process
        with open("logs.txt", "a", encoding="utf-8") as log_file:
            log_file.write(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - Processed \"{file_name}\" in {str(timedelta(seconds=duration))} | Used model: {whisper_model}\n")
        
        print(f"Transcription completed! Saved to \"{output_file_path}\"")
    else:
        print(f"Skipping \"{file_name}\", not an .{media_extension} file")
else:
    print("All files processed!")
