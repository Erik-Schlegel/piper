from enums.play_mode import PlayMode
from utils.load_tracks import load_tracks

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

            tracks = load_tracks(self._config.get_tracks(track_set.get('name', None)))
            print('hello')
        except Exception as e:
            print('whatsaasdg')


    def conduct_sequential(self, track_set:list):
        print('seq')



    def end():
        pass
