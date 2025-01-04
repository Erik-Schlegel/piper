import json
import copy
import os

from utils.dictionary_utils import deep_merge
from utils.list_utils import merge_named_lists


class ConfigHelper:
    _config_name = None
    _config = None


    def __init__(self, config_name):
        self._config_name = config_name
        self._config = self._load_config(config_name)


    def _load_config(self, config_name):
        with open(f'scenes/{config_name}.json') as file:
            return json.load(file)


    def get_config_name(self):
        return self._config_name


    def get_track_sets(self, include_ignored=False):
        track_sets = self._config.get('track_sets', [])

        # Don't include track_sets with "ignore": true
        if include_ignored:
            return track_sets
        else:
            return [
                track_set for track_set in track_sets
                    if not track_set.get('ignore', False)
            ]


    def get_track_set(self, name):
        track_sets = self.get_track_sets()
        for track_set in track_sets:
            if track_set.get('name', '') == name:
                return track_set
        return None


    def get_track_set_audio_options(self, name):
        named_layer = self.get_track_set(name)
        return named_layer.get('audio_options', {})


    def get_tracks(self, name):

        track_set = self.get_track_set(name).get('tracks', [])

        # handle folder paths: e.g. "tracks": [ "my/folder/path", ... ]
        if isinstance(track_set, str):
            track_set = self.prep_tracks_from_path(track_set)
        elif isinstance(track_set, list) and all(isinstance(item, str) for item in track_set):
            paths = track_set
            track_set = []
            for path in paths:
                track_set += self.prep_tracks_from_path(path)

        named_layer_tracks = copy.deepcopy(track_set)
        for track in named_layer_tracks:
            named_layer_options = copy.deepcopy(self.get_track_set_audio_options(name))

            # Equalizers should not be deep merged. We'll use some custom rules.
            named_layer_eq = named_layer_options.pop('equalizers', [])
            track_eq = track.get('audio_options', {}).get('equalizers', [])

            track['audio_options'] = deep_merge(
                named_layer_options,
                track.get('audio_options', {})
            )

            if track_eq or named_layer_eq:
                track['audio_options']['equalizers'] = merge_named_lists(
                    track_eq,
                    named_layer_eq
                )

        if not isinstance(named_layer_tracks, list):
            named_layer_tracks = [named_layer_tracks]
        return named_layer_tracks


    def prep_tracks_from_path(self, path):
        types = ('.mp3','.wav')
        files = os.listdir(path)
        return [
            {
                'path': f'{path}/{f}',
                'audio_options': {}
            } for f in files if f.endswith(types)
        ]


    @staticmethod
    def get_filename_from_track(track):
        return str.split(track.get('path'), '/')[-1]
