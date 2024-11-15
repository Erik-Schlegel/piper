import json
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
    def get_scene_files(cls, scene_name):
        config = cls.load_config()
        for scene in config['scenes']:
            if scene['name'] == scene_name:
                return scene['layers'][0]['files']
        return None


    @classmethod
    def get_merged_file_options(cls, scene_name):
        layer = cls.get_scene_layers(scene_name)[0]
        options = deep_merge(layer['options'], layer['files'][0]['options'])
        return options
