
class Track:
    _config = None
    _sample_data = None
    _sample_rate = None


    def __init__(self, config, sample_data, sample_rate):
        self._config = config
        self._sample_data = sample_data
        self._sample_rate = sample_rate


    def get_audio_option(self, name=None):
        options = self._config.get('audio_options',{})
        return options.get(name, None)


    @property
    def track_name(self):
        return str.split(self._config.get('path'), '/')[-1]


    @property
    def config(self):
        return self._config


    @property
    def samples(self):
        return self._sample_data


    @samples.setter
    def samples(self, value):
        self._sample_data = value


    @property
    def sample_rate(self):
        return self._sample_rate


    @property
    def channel_count(self):
        return self._sample_data.ndim


