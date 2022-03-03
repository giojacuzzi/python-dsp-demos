"""Utility functions for audio conversion"""

import numpy as np

# Convert linear audio data (signed 16-bit PCM) to floating
# point (32-bit) amplitude signal in range [-1.0, 1.0)
def linearPcmToFloat32(data):
    if data.dtype.kind != 'i':
        raise TypeError('data is not signed integer')
    limits = np.iinfo(data.dtype)
    max = 2 ** (limits.bits - 1) # 32768 for 16-bit
    return (data / max).astype('float32')

# Convert floating point amplitude signal to linear audio data
# (signed 16-bit PCM). Values in excess of [-1.0,1.0) are clipped.
def floatToLinearPcm(data):
    if data.dtype.kind != 'f':
        raise TypeError('data is not floating point')
    dtype = np.dtype('int16')
    limits = np.iinfo(dtype)
    max = 2 ** (limits.bits - 1)
    return (data * max).clip(limits.min, limits.max).astype(dtype)

# Convert linear amplitude to dBFS (decibels relative to full scale)
def linearTodBFS(linear):
    return 20.0 * np.log10(abs(linear))

# Convert dBFS to linear amplitude
def dBFSToLinear(dB):
    return 10 ** (dB / 20.0)
