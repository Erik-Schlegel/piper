import sounddevice
import prctl
from setproctitle import setproctitle
from time import sleep
from track import Track
from utils.ignore_signals import ignore_signals


def loop(track:Track):
    try:
        prctl.set_name(f'loop:{track.track_name}')
        with sounddevice.OutputStream(samplerate=track.sample_rate, channels=track.channel_count) as stream:
            while True:
                stream.write(track.samples)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

    finally:
        sounddevice.stop()


def play(track:Track):
    try:
        prctl.set_name(f'play:{track.track_name}')
        with sounddevice.OutputStream(samplerate=track.sample_rate, channels=track.channel_count) as stream:
            stream.write(track.samples)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    finally:
        sounddevice.stop()

