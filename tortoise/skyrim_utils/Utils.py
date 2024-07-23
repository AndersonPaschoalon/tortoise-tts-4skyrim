import wave
import numpy as np


def check_package(package_name):
    """
    Check if a given package is available for import.

    Args:
        package_name (str): The name of the package to check.

    Returns:
        bool: True if the package can be imported, False otherwise.
    """
    try:
        __import__(package_name)
        return True
    except ImportError:
        return False


def create_empty_audio(filename, duration, sample_rate=44100):
    """
    Create an empty audio file in WAV format of specified duration.

    Args:
        filename (str): The name of the file to save the audio.
        duration (float): The duration of the audio in seconds.
        sample_rate (int): The sample rate of the audio. Default is 44100 Hz.
    """
    # Calculate the total number of frames
    num_frames = int(duration * sample_rate)

    # Create an array of zeros (silence)
    audio_data = np.zeros(num_frames, dtype=np.int16)

    # Create a wave file
    with wave.open(filename, 'w') as wav_file:
        # Set the parameters for the wave file
        wav_file.setnchannels(1)  # Mono
        wav_file.setsampwidth(2)  # 16 bits per sample
        wav_file.setframerate(sample_rate)

        # Write the audio data to the wave file
        wav_file.writeframes(audio_data.tobytes())
