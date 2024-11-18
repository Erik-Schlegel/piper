import subprocess

class Audio:

    _LOG_VERBOSE = False
    # _LOG_VERBOSE = True

    @staticmethod
    def play_file(track):
        try:
            play_command = ['play', track['path']]
            play_command.extend(Audio.get_prepared_command_options(track))

            return subprocess.Popen(
                play_command,
                stdout=None if Audio._LOG_VERBOSE else subprocess.DEVNULL,
                stderr=None if Audio._LOG_VERBOSE else subprocess.DEVNULL
            )

        except Exception as e:
            print(f"An error occurred: {e}")
            return None


    @staticmethod
    def get_prepared_command_options(track):
        command = []

        if 'volume' in track['options']:
            command.extend(['vol', str(track['options']['volume'])])

        cross_fade_duration = track['options'].get('crossFadeDuration', 0)
        if cross_fade_duration > 0:
            command.extend(['fade', 't', str(cross_fade_duration/2), str(Audio.get_duration(track['path'])), str(cross_fade_duration)])

        return command



    @staticmethod
    def get_duration(file_path):
        """Get the duration of an audio file in seconds"""
        try:
            result = subprocess.run(['soxi', '-D', file_path], stdout=subprocess.PIPE)
            return (Audio.hms_to_seconds(result.stdout.decode('utf-8')))
        except Exception as e:
            print(f"An error occurred: {e}")
            return None


    @staticmethod
    def hms_to_seconds(hms):
        parts = hms.split(':')
        seconds = 0.0
        for i, part in enumerate(parts):
            seconds += float(part) * (60 ** (len(parts) - i - 1))
        return seconds