import sounddevice
from setproctitle import setproctitle

from track import Track
from utils.ignore_signals import ignore_signals


def play(track:Track):
    try:
        ignore_signals()
        setproctitle(f'pipyper.{track.track_name}')
        while True:
            with sounddevice.OutputStream(samplerate=track.sample_rate, channels=track.channel_count) as stream:
                stream.write(track.samples)

    except Exception as e:
        print(f"An unexpected error occurred: {e}")

    finally:
        sounddevice.stop()
