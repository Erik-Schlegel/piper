import json
import copy

from utils.dictionary_utils import deep_merge
from utils.list_utils import merge_named_lists


class ConfigHelper:
    _config = None


    def __init__(self, config_name):
        self._config = self._load_config(config_name)


    def _load_config(self, config_name):
        with open(f'scenes/{config_name}.json') as file:
            return json.load(file)


    def get_layer_sets(self, include_ignored=False):
        # if a layer_set has "ignore": true, do not include it in the result set, unless include_ignored is True
        layer_sets = self._config.get('layer_sets', [])

        if include_ignored:
            return layer_sets
        else:
            return [
                layer_set for layer_set in layer_sets
                    if not layer_set.get('ignore', False)
            ]


    def get_layer_set(self, name):
        layer_sets = self.get_layer_sets()
        for layer_set in layer_sets:
            if layer_set.get('name', '') == name:
                return layer_set
        return None


    def get_layer_set_audio_options(self, name):
        named_layer = self.get_layer_set(name)
        return named_layer.get('audio_options', {})


    def get_tracks(self, name):
        named_layer_tracks = copy.deepcopy(self.get_layer_set(name).get('tracks', []))

        for track in named_layer_tracks:
            named_layer_options = copy.deepcopy(self.get_layer_set_audio_options(name))

            # We deal with equalizers later with custom handling
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
