import subprocess

class Audio:

    @staticmethod
    def play_file(file_path, cross_fade_duration=0):
        try:
            proc = subprocess.Popen([
                'play', file_path, 'fade', 't', str(cross_fade_duration/2), str(Audio.get_duration(file_path)), str(cross_fade_duration)
            ])
            return proc

        except Exception as e:
            print(f"An error occurred: {e}")
            return None

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