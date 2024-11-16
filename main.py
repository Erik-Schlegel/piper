
import sys
import signal

from conductor import Conductor


audio_conductor = None


def main():
    global audio_conductor
    try:
        add_event_handlers()
        audio_conductor = Conductor('WinterCabin')
        audio_conductor.start()

    except Exception as e:
        exit(f"An error occurred: {e}")


def exit(message='Exiting...'):
    if audio_conductor:
        audio_conductor.stop()
    print(message)
    sys.exit(0)


def signal_handler(sig, frame):
    exit()


def add_event_handlers():
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)


if __name__ == "__main__":
    main()
