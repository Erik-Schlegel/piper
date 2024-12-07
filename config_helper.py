import json
import random

from dictionary_utils import deep_merge

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
    def get_simultaneous_tracks(cls, scene_name):
        simultaneous_layer = cls.get_scene_layers(scene_name)['simultaneous']
        for track in simultaneous_layer['tracks']:
            clone = dict(simultaneous_layer['options'])
            track['options'] = deep_merge(clone, track['options'])
        return simultaneous_layer['tracks']


    @classmethod
    def get_shuffled_tracks(cls, scene_name):
        shuffled_layer = cls.get_scene_layers(scene_name)['shuffled']
        for track in shuffled_layer['tracks']:
            clone = dict(shuffled_layer['options'])
            track['options'] = deep_merge(clone, track['options'])
        random.shuffle(shuffled_layer['tracks'])
        return shuffled_layer['tracks']


    @classmethod
    def get_merged_file_options(cls, scene_name, type):
        type_layer = cls.get_scene_layers(scene_name)[type]
        options = deep_merge(type_layer['options'], type_layer['files'][type]['options'])
        return options


    @classmethod
    def get_scene_folder_path_by_type(cls, scene_name, type):
        type_layer = cls.get_scene_layers(scene_name)[type]
        return type_layer['folderPath']

    @classmethod
    def get_intermission_seconds_minmax(cls, scene_name):
        type_layer = cls.get_scene_layers(scene_name)['shuffled']
        return type_layer['intermissionSeconds']

