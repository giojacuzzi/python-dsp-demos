"""Read audio data from a file, perform some signal processing on it, and write the result to a new file"""

import struct, sys, wave
import matplotlib.pyplot as plt
import numpy as np
from os.path import exists
from audioplayer import AudioBufferPlayer
from utils import linearPcmToFloat32, floatToLinearPcm, dBFSToLinear

# Read audio data from file as amplitude signal
try:
    if len(sys.argv) != 3:
        raise ValueError(f'Usage: {sys.argv[0]} path/to/input.wav path/to/output.wav')
    filepath = sys.argv[1]
    if not exists(filepath):
        raise RuntimeError('Input file does not exist')

    # Open input file and check compatibility
    file = wave.open(filepath, 'r')
    if file.getsampwidth() != 2 or file.getnchannels() != 1:
        raise ValueError('Input file must be a signed 16-bit PCM mono .wav')
    
    # Read raw audio data from input file
    framerate = file.getframerate()
    nframes = file.getnframes()
    data = file.readframes(nframes)
    data = np.frombuffer(data, 'int16')

    # Convert data to floating point amplitude signal in range [-1.0, 1.0)
    input = linearPcmToFloat32(data)
    nchannels = file.getnchannels()
    nframes = file.getnframes()
    framerate = file.getframerate()
    file.close()
except Exception as e:
    print(e)
    sys.exit(-1)

# Perform some digital signal processing
output = input.copy()
output *= dBFSToLinear(24.0) # apply a 24dB gain

# Listen to the output signal
audio_player = AudioBufferPlayer()
audio_player.play(output, nchannels, framerate)

# Write resulting audio data to output file
try:
    # Convert output signal to signed 16-bit PCM data
    pcm = floatToLinearPcm(output)

    # Write audio data to file
    file = wave.open(sys.argv[2],'w')
    file.setnchannels(nchannels)
    file.setsampwidth(2)
    file.setframerate(framerate)
    for i in range(len(pcm)):
        file.writeframesraw(struct.pack('<h', pcm[i]))
    file.close()
except Exception as e:
    print(e)
    sys.exit(-1)

# Plot the signals in the time and frequency domains
time = np.linspace(0, len(input) / framerate, num=len(input))
fig, ax = plt.subplots(2, 2)
ax1A = ax[0,0]
ax1B = ax[0,1]
ax2A = ax[1,0]
ax2B = ax[1,1]
 
ax1A.plot(time, input)
ax1A.set_title('Time domain (input)')
ax1A.set_ylabel('Amplitude')
ax1A.set_xbound(0.0, time[-1])
ax1A.set_ybound(-1.0, 1.0)

ax1B.plot(time, output)
ax1B.set_title('Time domain (output)')
ax1B.set_xbound(0.0, time[-1])
ax1B.set_ybound(-1.0, 1.0)

spectrum, freqs, t, im = ax[1, 0].specgram(input, Fs=framerate, vmin=-140, vmax=0)
ax2A.set_title('Frequency domain (input)')
ax2A.set_xlabel('Time (sec)')
ax2A.set_ylabel('Frequency (Hz)')
ax2A.set_xbound(0.0, time[-1])

spectrum, freqs, t, im = ax[1, 1].specgram(output, Fs=framerate, vmin=-140, vmax=0)
ax2B.set_title('Frequency domain (output)')
ax2B.set_xlabel('Time (sec)')
ax2B.set_xbound(0.0, time[-1])

fig.tight_layout() 
plt.show()
