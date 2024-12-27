from setproctitle import setproctitle
# import multiprocessing
import threading

from enums.play_mode import PlayMode
from audio_processor import add_track_fx
from track_player import loop
from utils.load_tracks import load_tracks
from utils.ignore_signals import ignore_signals

import typing
from track import Track

class Conductor:

    _config = None
    _subprocesses = None


    def __init__(self, config):
        self._config = config
        self._subprocesses = []


    def begin(self):
        track_sets = self._config.get_track_sets()
        for track_set in track_sets:

            try:
                play_fn = ({
                    PlayMode.SIMULTANEOUS: self.play_simultaneous,
                    PlayMode.SEQUENTIAL: self.play_sequential
                })[PlayMode(track_set.get('play_mode', None))]

                # TODO: start this in a process.
                play_fn(track_set)


            except ValueError:
                raise ValueError(f'No valid play_mode specified in {self._config.get_config_name()}')


    def play_simultaneous(self, track_set:list):
        ignore_signals()
        setproctitle(f'piper.conductor.play_simultaneous')
        try:
            tracks = load_tracks(self._config.get_tracks(track_set.get('name', None)))
            tracks = add_track_fx(tracks)

            for track in tracks:
                subprocess =  threading.Thread(
                    target=loop,
                    args=(track, )
                )
                self._subprocesses.append(subprocess)
                subprocess.start()

        except Exception as e:
            print(e)


    def play_sequential(self, track_set:list):
        # ignore_signals()

        # TODO: Build me
        # first_run = True
        # while first_run or track_set.get('loop', False):
        #     continue
            #sleep(intermission)
            #shuffle tracks
            #foreach track
                #load individual track
                #process individual track
                #play individual track'
            #first_run = False
        pass


    def end(self):
        for process in self._subprocesses:
            if process.is_alive():
                process.terminate()
                process.join()
        print('donezo')


