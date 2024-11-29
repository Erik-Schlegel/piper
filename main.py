import sys
import signal
import multiprocessing

from conductor import Conductor


audio_conductor = None


def main():
    global audio_conductor
    audio_conductor = Conductor('WinterCabin')
    audio_conductor.start()


def add_signal_handlers():
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)


def signal_handler(_sig, _frame):
    audio_conductor.stop()
    sys.exit(0)


if __name__ == "__main__":
    try:
        multiprocessing.set_start_method('spawn')
        add_signal_handlers()
        main()
    except KeyboardInterrupt:
        signal_handler(signal.SIGINT, None)
