from setproctitle import setproctitle
import multiprocessing
import threading
from time import sleep
import random

from enums.play_mode import PlayMode
from audio_processor import add_track_fx
from track_player import loop, play
from utils.load_tracks import load_tracks
from utils.ignore_signals import ignore_signals

import typing
from config_helper import ConfigHelper
from track import Track

class Conductor:

    _config = None
    _subprocesses = None
    _threads = None


    def __init__(self, config: ConfigHelper):
        ignore_signals()
        self._config = config
        self._subprocesses = []


    def begin(self):
        track_sets = self._config.get_track_sets()
        for track_set in track_sets:

            try:
                play_fn = ({
                    PlayMode.SIMULTANEOUS: Conductor.play_simultaneous,
                    PlayMode.SEQUENTIAL: Conductor.play_sequential
                })[PlayMode(track_set.get('play_mode', None))]

                proc = multiprocessing.Process(
                    target=play_fn,
                    args=(
                        track_set,
                        self._config.get_tracks(track_set.get('name', None))
                    )
                )

                self._subprocesses.append(proc)
                proc.start()
                # when attaching a debugger, uncomment the following line, else the debugger may detatch after ~30 seconds.
                # IMPORTANT! DO NOT leave uncommented for actual "production" contexts.
                # proc.join(timeout=360000)

            except ValueError:
                raise ValueError(f'No valid play_mode specified in {self._config.get_config_name()}')


    @staticmethod
    def play_simultaneous(track_set:dict, tracks:list[Track]):
        ignore_signals()
        setproctitle(f'piper.conductor.play_simultaneous')

        try:
            tracks = load_tracks(tracks)
            tracks = add_track_fx(tracks)

            for track in tracks:
                thread =  threading.Thread(
                    target=loop,
                    args=(track, )
                )
                thread.start()

        except Exception as e:
            print(e)


    @staticmethod
    def play_sequential(track_set:dict, tracks:list[Track]):
        ignore_signals()
        setproctitle(f'piper.conductor.play_sequential')

        played_set_once = False
        while not played_set_once or track_set.get('loop', False):

            if track_set.get('shuffle', False):
                random.shuffle(tracks)

            for track in tracks:
                #TODO: sleep for intermission
                sleep(45)

                track = load_tracks(track)
                track = add_track_fx(track)
                thread = threading.Thread(
                    target=play,
                    args=(track[0], )
                )
                thread.start()
                thread.join()


            played_set_once = True


    def end(self):
        for process in self._subprocesses:
            if process.is_alive():
                process.terminate()
                process.join()



