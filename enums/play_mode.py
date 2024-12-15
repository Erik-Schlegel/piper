from enum import Enum

class PlayMode(Enum):
    SIMULTANEOUS = 'simultaneous'
    SEQUENTIAL = 'sequential'
    SHUFFLE = 'shuffle'


    @staticmethod
    def get_mode(value):
        try:
            return PlayMode(value)
        except ValueError:
            return None
