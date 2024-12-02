import multiprocessing

from config_helper import ConfigHelper
from audio_file_loader import load_tracks
from player import play_audio, loop_audio


class Conductor:

    _scene_name = None
    _subprocesses = None


    def __init__(self, scene_name):
        self._subprocesses = []
        self._scene_name = scene_name


    def start(self):
        tracks = ConfigHelper.get_scene_tracks_by_type(self._scene_name, 'simultaneous')
        self.play_tracks(tracks, loop_audio)

        tracks = ConfigHelper.get_scene_tracks_by_type(self._scene_name, 'shuffled')
        self.play_tracks(tracks, play_audio)

        for subprocess in self._subprocesses:
            subprocess.join()


    def play_tracks(self, tracks, operation):
        if not isinstance(tracks, list):
            tracks = [tracks]
        tracks = load_tracks(tracks)

        while not tracks.empty():
            proc = multiprocessing.Process(target=operation, args=(tracks.get(),))
            proc.start()
            self._subprocesses.append(proc)


    def stop(self):
        for process in self._subprocesses:
            if process.is_alive():
                process.terminate()
                process.join()
        # sd.stop()
