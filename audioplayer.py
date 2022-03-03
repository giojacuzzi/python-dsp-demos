"""Helper classes to manage playback of 32-bit floating point mono audio data via PyAudio (PortAudio)"""

import threading
from time import sleep
from pyaudio import PyAudio, paContinue, paFloat32

# Base class for AudioBufferPlayer and AudioCallbackPlayer
class AudioPlayer:

    # Constructor - Initializes PyAudio
    def __init__(self):
        self._pa = PyAudio()

    # Destructor - Terminates PyAudio
    def __del__(self):
        self._pa.terminate()

# Manages playback of an audio data buffer
class AudioBufferPlayer(AudioPlayer):

    # Constructor
    def __init__(self):
        AudioPlayer.__init__(self)

    # (Private) Opens stream and writes buffer frames until finished
    def __play(self, buffer, nchannels, framerate):
        self._stream = self._pa.open(format  = paFloat32,
                                    channels = nchannels,
                                    rate     = framerate,
                                    output   = True)

        self._stream.write(frames=buffer, num_frames=len(buffer))

        self._stream.stop_stream()
        self._stream.close()

    # Launches a background thread to manage the buffer stream
    def play(self, signal, nchannels, framerate):
        threading.Thread(target=self.__play, args=(signal, nchannels, framerate)).start()

# Manages playback through an audio callback interface
class AudioCallbackPlayer(AudioPlayer):

    # Constructor - Opens stream with given callback
    def __init__(self, callback, framerate, frames_per_buffer):
        AudioPlayer.__init__(self)
        self._callback = callback
        self._stream = self._pa.open(format           = paFloat32,
                                    channels          = 1,
                                    rate              = framerate,
                                    frames_per_buffer = frames_per_buffer,
                                    output            = True,
                                    stream_callback   = self._callback)

    # Destructor - Closes stream
    def __del__(self):
        self._stream.close()

    # (Private) Starts the stream and waits for it to finish
    def __play(self):
        self._stream.start_stream()
        while self._stream.is_active():
            sleep(0.1)

    # Launches a background thread to manage the callback stream
    def play(self):
        threading.Thread(target=self.__play, args=()).start()

    # Stops the stream, which will terminate the background thread
    def stop(self):
        self._stream.stop_stream()
