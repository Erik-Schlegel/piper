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
from utils.print_utils import overwrite_at, proc_file_path

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
        if(not isinstance(track_sets, list)):
            track_sets = [track_sets]

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
                # IMPORTANT! When debugger detatches after ~20seconds. Uncomment this line:
                # DO NOT leave that in place for actual "production" contexts.
                # proc.join(timeout=360000)
                ## IF YOU DO NOT COMMENT THIS OUT: only the first track_set will play.

            except ValueError:
                raise ValueError(f'No valid play_mode specified in {self._config.get_config_name()}')


    @staticmethod
    def play_simultaneous(track_set:dict, tracks:list):
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
    def play_sequential(track_set:dict, tracks:list):
        ignore_signals()
        setproctitle(f'piper.conductor.play_sequential')

        played_set_once = False
        while not played_set_once or track_set.get('loop', False):

            if track_set.get('shuffle', False):
                random.shuffle(tracks)

            for track in tracks:
                proc_path = proc_file_path(track['path'])
                intermission = Conductor.get_processed_intermission(track_set.get('intermission', 45))
                sleep(intermission)

                overwrite_at(3, 'Loading: ' + proc_path)
                track = load_tracks(track)
                overwrite_at(3, 'Processing: ' + proc_path)
                track = add_track_fx(track)
                overwrite_at(3, 'Playing: ' + proc_path)
                thread = threading.Thread(
                    target=play,
                    args=(track[0], )
                )
                thread.start()
                thread.join()

            played_set_once = True


    @staticmethod
    def get_processed_intermission(intermission) -> int:
        value = None
        if(isinstance(intermission, list)):
            value = int(random.uniform(*intermission))
        elif isinstance(intermission, int):
            #TODO: handle negative intermissions elsewhere. This'll mean crossfade.
            value = abs(intermission)
        else:
            #default case
            value = 45
        return value


    def end(self):
        for process in self._subprocesses:
            if process.is_alive():
                process.terminate()
                process.join()





