# Copyright 2018, Eric Clack, eric@bn7.net
# This program is distributed under the terms of the GNU General 
# Public License

"""Sounds for PyScratch using simpleaudio.

See examples in the folder examples, or more info on github.com:
https://github.com/ericclack/geekclub/sound1.py

To install: pip3 install simpleaudio
Get free to use sounds here: https://freesound.org/

Author: Eric Clack, eric@bn7.net
"""

from geekclub.pyscratch import canvas, future_action, END_GAME

class DummySoundLib():
    "No-op sound library if we can't load simpleaudio"
    WaveObject = None

    def __init__(self):
        print("Can't play sound!")
        print("You need to install simpleaudio with `pip3 install simpleaudio`")
        DummySoundLib.WaveObject = self

    def from_wave_file(self, file):
        return self

    def play(self):
        pass

try:
    import simpleaudio as sa
except ImportError:
    sa = DummySoundLib()

import time

BPM = 1 * 60
def bpm(): return BPM

def set_bpm(b):
    global BPM
    BPM = b

def bps():
    "Beats per second"
    return BPM / 60

def beat_ms():
    "The length of a beat in miliseconds"
    return int(1000 / bps())

def load_sound(file):
    "Load a sound, tested with WAV files"
    return sa.WaveObject.from_wave_file(file)

def every_beat(fn):
    def wrapper():
        fn()
        if not END_GAME:
            canvas().after(beat_ms(), wrapper)
    canvas().after(beat_ms(), wrapper)
            
def every_off_beat(fn):
    def wrapper():
        fn()
        if not END_GAME:
            canvas().after(beat_ms(), wrapper)
    canvas().after(int(beat_ms() * 1.5), wrapper)
    

def every_n_beats(beats, fn):
    def wrapper():
        fn()
        if not END_GAME:
            canvas().after(beat_ms() * beats, wrapper)
    canvas().after(beat_ms() * beats, wrapper)