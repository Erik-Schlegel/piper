
import sys
import signal
import time

from conductor import Conductor


audio_conductor = None


def main():
    global audio_conductor
    try:
        add_event_handlers()
        audio_conductor = Conductor('WinterCabin')
        audio_conductor.start()
        while True:
          time.sleep(1) # sleep for 1 second

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
