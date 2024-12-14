from enum import Enum

class PlayMode(Enum):
    ORDERED = 'ordered'
    SHUFFLED = 'shuffled'
    SIMULTANEOUS = 'simultaneous'


    @staticmethod
    def get_mode(value):
        try:
            return PlayMode(value)
        except ValueError:
            raise ValueError(f"Invalid PlayMode: {value}. Check your configuration file. Valid values are: {', '.join([mode.value for mode in PlayMode])}")