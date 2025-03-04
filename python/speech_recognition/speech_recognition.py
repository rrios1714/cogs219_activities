# MJP - Written for Psych750 Fall 2023
import sounddevice as sd
import wavio
import whisper
import numpy as np
from scipy.io import wavfile as wav  # needed to read .wav files for the new toolkit
from calculate_voice_onset import auto_utterance_times

'''
Uses OpenAI Whisper Toolbox to transcribe spoken English.

It detects the onset time (RT) of the speech using the new toolkit.
Output of RT and transcription will be printed on command line.
'''

# Initialize recording parameters
RATE = 44100
CHANNELS = 1
DTYPE = 'int16'
FILENAME = "recording.wav"
SECONDS = 2.5

# Load whisper model
model = whisper.load_model("base")

print("starting to record")
audio_data = sd.rec(int(SECONDS * RATE), samplerate=RATE, channels=CHANNELS, dtype=DTYPE, blocking=True)
print("ended recording after ", SECONDS, " seconds")
wavio.write(FILENAME, audio_data, RATE, sampwidth=2)

fs, signal = wav.read(FILENAME)
idx, rt_milliseconds = auto_utterance_times(signal, fs)
rt_seconds = rt_milliseconds / 1000  # Convert from ms to s
print(f"Detected speech onset at: {rt_seconds:.3f} seconds")
result = model.transcribe(FILENAME)
print(f"Transcription: {result['text']}")
