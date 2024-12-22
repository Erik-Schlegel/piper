import json
import copy

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
        named_layer_tracks = copy.deepcopy(self.get_track_set(name).get('tracks', []))

        for track in named_layer_tracks:
            named_layer_options = copy.deepcopy(self.get_track_set_audio_options(name))

            # Equalizers should not be deep merged. We'll use some custom rules.
            named_layer__eq = named_layer_options.pop('equalizers', [])
            track_eq = track.get('audio_options', {}).get('equalizers', [])

            track['audio_options'] = deep_merge(
                named_layer_options,
                track.get('audio_options', {})
            )

            if track_eq != {} or named_layer__eq != {}:
                track['audio_options']['equalizers'] = merge_named_lists(
                    track_eq,
                    named_layer__eq
                )

        if not isinstance(named_layer_tracks, list):
            named_layer_tracks = [named_layer_tracks]
        return named_layer_tracks



    @staticmethod
    def get_filename_from_track(track):
        return str.split(track.get('path'), '/')[-1]
