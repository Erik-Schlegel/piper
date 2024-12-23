import sys
import signal
import multiprocessing
from setproctitle import setproctitle

from config_helper import ConfigHelper
from conductor import Conductor

conductor = None


def main():

    multiprocessing.set_start_method('spawn')
    setproctitle('pipyper.main')

    global conductor
    conductor = Conductor(ConfigHelper('winter_coziness'))
    conductor.begin()


def get_scene_names():
    #TODO: implement method to return a list from  ./scenes/*.json
    pass


def add_signal_handlers():
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)


def signal_handler(_sig, _frame):
    conductor.end()
    # sys.exit(0)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        signal_handler(signal.SIGINT, None)