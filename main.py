import sys
import signal
import multiprocessing
from argparse import ArgumentParser
from setproctitle import setproctitle

from config_helper import ConfigHelper
from conductor import Conductor

conductor = None


def main():
    parser = ArgumentParser(description="Load, process, and play one or more audio tracks simultaneously or sequentially (or both). Great for setting up audio for ambience.")
    parser.add_argument('--scene', help='optional. Run without --scene to see which named configs exist.')
    args = parser.parse_args()

    if args.scene is None or \
        len(vars(args)) == 0 or \
        not any(vars(args).values()):
        print_command_help()
    else:
        start_scene(args.scene)


def start_scene(scene_name):
    if not ConfigHelper.is_viable_scene_name(scene_name):
        print(f'{scene_name} is not a viable option.')
        return

    multiprocessing.set_start_method('spawn')
    setproctitle('piper.main')

    global conductor
    conductor = Conductor(ConfigHelper(scene_name))
    conductor.begin()


def print_command_help():
    scenes = ConfigHelper.get_scene_names()
    print('\nSpecify a scene to run. Example:')
    print(f'   ./run -s {scenes[0]}')
    print('\nViable scene names:')
    for scene in scenes:
        print(f'   {scene}')
    print('')


def add_signal_handlers():
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)


def signal_handler(_sig, _frame):
    conductor.end()
    sys.exit(0)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        signal_handler(signal.SIGINT, None)