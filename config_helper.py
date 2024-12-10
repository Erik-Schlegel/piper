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
                track['options']['equalizers'] = ConfigHelper.merge_named_lists(
                    track_eq,
                    cloned_layer_options_eq
                )

        return selected_layer['tracks']



    # @classmethod
    # def get_simultaneous_tracks(cls, scene_name):
    #     simultaneous_layer = cls.get_scene_layers(scene_name)['simultaneous']
    #     for track in simultaneous_layer['tracks']:
    #         clone = dict(simultaneous_layer['options'])
    #         track['options'] = deep_merge(clone, track['options'])
    #     return simultaneous_layer['tracks']


    # @classmethod
    # def get_shuffled_tracks(cls, scene_name):
    #     shuffled_layer = cls.get_scene_layers(scene_name)['shuffled']
    #     for track in shuffled_layer['tracks']:

    #         cloned_options = dict(shuffled_layer['options'])

    #         track['options']['reverb'] = deep_merge(
    #             cloned_options.get('reverb',{}),
    #             track['options'].get('reverb',{})
    #         )

    #         track['options']['equalizers'] = ConfigHelper.merge_named_lists(
    #             track['options'].get('equalizers', []),
    #             cloned_options.get('equalizers', [])
    #         )

    #     random.shuffle(shuffled_layer['tracks'])
    #     return shuffled_layer['tracks']


    @classmethod
    def get_intermission_seconds_minmax(cls, scene_name):
        type_layer = cls.get_scene_layers(scene_name)['shuffled']
        return type_layer['intermissionSeconds']


    @staticmethod
    def merge_named_lists(list_a, list_b):
        """
        Merges two lists of dictionaries, keeping items from list_a when 'name' conflicts exist.

        Args:
            list_a: Primary list of dicts with 'name' field
            list_b: Secondary list of dicts with 'name' field

        Returns:
            List of merged dictionaries with no duplicate names
        """
        # Create a dict for fast lookup using name as key
        name_map = {item['name']: item for item in list_a}

        # Only add items from list_b if their name isn't already present
        for item in list_b:
            if item['name'] not in name_map:
                name_map[item['name']] = item

        # Convert back to list
        return list(name_map.values())
