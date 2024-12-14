import json


from utils.dictionary_utils import deep_merge
from utils.list_utils import merge_named_lists


class ConfigHelper:


    CONFIG_FILE_PATH = 'manifest.json'
    _config = None


    @classmethod
    def load_config(cls):
        if cls._config is None:
            with open(cls.CONFIG_FILE_PATH, 'r') as file:
                cls._config = json.load(file)
        return cls._config


    @classmethod
    def get_scene_names(cls):
        config = cls.load_config()
        return [scene['name'] for scene in config['scenes']]


    @classmethod
    def get_scene_layers(cls, scene_name):
        config = cls.load_config()
        for scene in config['scenes']:
            if scene['name'] == scene_name:
                return scene['layers']
        return None


    @classmethod
    def get_tracks_by_type(cls, scene_name, track_type):
        selected_layer = cls.get_scene_layers(scene_name)[track_type]


        for track in selected_layer['tracks']:
            cloned_layer_options = dict(selected_layer.get('options',{}))
            cloned_layer_options_eq = cloned_layer_options.pop('equalizers', [])

            if track.get('options') is None:
                continue

            track_eq = track['options'].pop('equalizers', {})

            track['options'] = deep_merge(
                cloned_layer_options,
                track.get('options',{})
            )

            if track_eq != {} or cloned_layer_options_eq != {}:
                track['options']['equalizers'] = merge_named_lists(
                    track_eq,
                    cloned_layer_options_eq
                )

        return selected_layer['tracks']

    @classmethod
    def get_shuffled_track_sets(cls, scene_name):
        selected_layer = cls.get_scene_layers(scene_name)['shuffled']

        for track_set in selected_layer:

            for track in track_set['tracks']:
                cloned_layer_options = dict(track_set.get('options',{}))
                cloned_layer_options_eq = cloned_layer_options.pop('equalizers', [])

                if track.get('options') is None:
                    continue

                track_eq = track['options'].pop('equalizers', {})

                track['options'] = deep_merge(
                    cloned_layer_options,
                    track.get('options',{})
                )

                if track_eq != {} or cloned_layer_options_eq != {}:
                    track['options']['equalizers'] = merge_named_lists(
                        track_eq,
                        cloned_layer_options_eq
                    )

        return selected_layer


    @classmethod
    def get_intermission_seconds_minmax(cls, scene_name):
        type_layer = cls.get_scene_layers(scene_name)['shuffled']
        return type_layer['intermissionSeconds']
