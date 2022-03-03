# NPS SIP Demos - Gio Jacuzzi

This folder contains two python programs, `demo_dsp.py` and `demo_sine.py`, as well as several helper classes and utility functions. The `audio` directory contains input files for testing. See `requirements.txt` for package dependencies.

System dependencies:
- python (tested with version 3.9.10)
- [portaudio](http://www.portaudio.com/) (`brew install portaudio`)

## demo_dsp.py

Example usage:
```
python demo_dsp.py audio/bewicks-wren.wav audio/output.wav
```

This demo reads audio data from a file, performs some signal processing on it, and writes the result to a new file. It also plots the signal before and after processing in the time and frequency domains.


## demo_sine.py

Usage:
```
python demo_sine.py
```

This demo controls a sine wave oscillator with a GUI window.

---

_Contact: giojacuzzi@gmail.com_
