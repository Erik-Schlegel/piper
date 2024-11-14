from config_helper import ConfigHelper
import subprocess
import signal
import sys


subprocesses = []


def main():
    try:
        path = ConfigHelper.get_scene_files('WinterCabin')[0]['path']
        proc = subprocess.Popen(['play', path])
        subprocesses.append(proc)

        # Wait for all subprocesses to finish
        for proc in subprocesses:
            proc.wait()

    except Exception as e:
        print(e)
        terminate_subprocesses()


def terminate_subprocesses():
    for proc in subprocesses:
        proc.terminate()
    sys.exit(0)


def signal_handler(sig, frame):
    print('Terminating...')
    terminate_subprocesses()


signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)


if __name__ == "__main__":
    main()