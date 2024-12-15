import sys
import signal
import multiprocessing
from setproctitle import setproctitle

from conductor import Conductor

audio_conductor = None

def main():
    setproctitle('piper.main')
    multiprocessing.set_start_method('spawn')
    add_signal_handlers()

    global audio_conductor
    audio_conductor = Conductor('winter_cabin')
    audio_conductor.start_playback()


def add_signal_handlers():
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)


def signal_handler(_sig, _frame):
    audio_conductor.stop_playback()
    sys.exit(0)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print('is this necessary?')
        signal_handler(signal.SIGINT, None)
