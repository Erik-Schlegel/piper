import multiprocessing

from enums.play_mode import PlayMode
from audio_processor import add_track_fx, add_self_cross_fade
from track_player import play
from utils.load_tracks import load_tracks
from utils.ignore_signals import ignore_signals


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
                    PlayMode.SIMULTANEOUS: self.conduct_simultaneous,
                    PlayMode.SEQUENTIAL: self.conduct_sequential
                })[PlayMode(track_set.get('play_mode', None))]

                play_fn(track_set)


            except ValueError:
                raise ValueError(f'No valid play_mode specified in {self._config.get_config_name()}')


    def conduct_simultaneous(self, track_set):
        try:
            ignore_signals()

            tracks = load_tracks(self._config.get_tracks(track_set.get('name', None)))
            tracks = add_track_fx(tracks)

            intermission = track_set.get('intermission', 3)

            #TODO: flesh this out.
            # if intermission < 0:
            #     tracks = add_self_cross_fade(tracks)


            for track in tracks:
                # TODO: In principal the play method shouldn't receive loop or intermission. It's Conductor's job to restart and pause restarts.
                subprocess =  multiprocessing.Process(
                    target=play,
                    args=(
                        track,
                        track_set.get('loop', False),
                        track_set.get('intermission', 3)
                    )
                )
                self._subprocesses.append(subprocess)
                subprocess.start()

        except Exception as e:
            print(e)


    def conduct_sequential(self, track_set:list):
        print('seq')


    def end(self):
        for process in self._subprocesses:
            if process.is_alive():
                process.terminate()
                process.join()
        print('donezo')
