"""Control a sine wave oscillator with a GUI"""

import math
import numpy as np
import tkinter as tk
from pyaudio import paContinue
from audioplayer import AudioCallbackPlayer
from utils import dBFSToLinear, linearTodBFS

FRAME_RATE = 48000              # sampling rate (Hz)
FRAMES_PER_BUFFER = 128
TIME = 1.0 / float(FRAME_RATE)  # seconds per sample
frequency = 2000.0              # oscillations per second (Hz)
amplitude = 0.5                 # linear gain
phase = 0.0                     # will shift over time
data = np.zeros(FRAMES_PER_BUFFER, dtype='float32')

# Audio callback to generate a buffer of sine wave signal data
# y(t) = A * sin(2 * pi * f * t)
def callback(in_data, frame_count, time_info, status):
    if status:
        raise Exception(f'Callback error: {status}')
    
    t = 0
    while t < frame_count:
        global phase
        data[t] = amplitude * np.sin(phase)
        delta = 2 * np.pi * frequency * TIME
        phase = math.fmod(phase + delta, 2 * np.pi) # prevent overflow by wrapping phase in range [0,2pi)
        t += 1
    return (data, paContinue)

# Listen to the signal
audio_player = AudioCallbackPlayer(callback, FRAME_RATE, FRAMES_PER_BUFFER)
audio_player.play()

# Create GUI control window
window = tk.Tk()
window.title('Sine Wave Oscillator')

# Create gain slider
def gainChanged(val):
    global amplitude
    amplitude = dBFSToLinear(float(val))
sliderGain = tk.Scale(window, from_=-96.0, to=0.0, resolution=0.1, command=gainChanged, orient=tk.HORIZONTAL, length=500, label='Gain (dBFS)')
sliderGain.set(linearTodBFS(amplitude))
sliderGain.pack()

# Create frequency slider
def frequencyChanged(val):
    global frequency
    frequency = float(val)
sliderFrequency = tk.Scale(window, from_=20, to=20000, resolution=1, command=frequencyChanged, orient=tk.HORIZONTAL, length=500, label='Frequency (Hz)')
sliderFrequency.set(frequency)
sliderFrequency.pack()

# Display the window and respond to user interaction
window.mainloop()

# Cleanup after window close
audio_player.stop()
