from config_helper import ConfigHelper
import subprocess
import signal
import sys
import time

subprocesses = []

def main():

    try:
        path = ConfigHelper.get_scene_files('WinterCabin')[0]['path']
        print(ConfigHelper.get_merged_file_options('WinterCabin'))
        subprocesses.append(subprocess.Popen(['play', 'resources/BlackRainfall_final.wav', 'vol', '1', 'repeat', '2']))

        while True:
            # Keep the main function running to handle signals
            time.sleep(1)

    except Exception as e:
        print(f"An error occurred: {e}")
        terminate_subprocesses()


def terminate_subprocesses():
    for proc in subprocesses:
        proc.terminate()
        proc.wait() # w/o waiting the app doesn't fully close on quit


def signal_handler(sig, frame):
    terminate_subprocesses()
    sys.exit(0)


signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)


if __name__ == "__main__":
    main()