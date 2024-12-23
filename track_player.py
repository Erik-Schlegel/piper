import sounddevice
from setproctitle import setproctitle
from time import sleep
from track import Track
from utils.ignore_signals import ignore_signals


def play(track:Track, loop:bool, intermission:int):
    try:
        ignore_signals()
        setproctitle(f'piper.play:{track.track_name}')

        first_run = True
        while first_run or loop:
            with sounddevice.OutputStream(samplerate=track.sample_rate, channels=track.channel_count) as stream:
                stream.write(track.samples)

            first_run = False
            sleep(0 if intermission < 0 else intermission)

    except Exception as e:
        print(f"An unexpected error occurred: {e}")

    finally:
        sounddevice.stop()
