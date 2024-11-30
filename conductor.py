import multiprocessing

from config_helper import ConfigHelper
from audio_file_loader import load_tracks
from player import play_audio

class Conductor:

    _scene_name = None
    _subprocesses = None

    def __init__(self, scene_name):
        self._subprocesses = []
        self._scene_name = scene_name


    def start(self):
        tracks = ConfigHelper.get_scene_tracks_by_type(self._scene_name, 'simultaneous')
        folder_path = ConfigHelper.get_scene_folder_path_by_type(self._scene_name, 'simultaneous')
        if not isinstance(tracks, list):
            tracks = [tracks]

        file_queue = load_tracks(folder_path, tracks)
        self.begin_playback(file_queue)


    def begin_playback(self, queue):
        while not queue.empty():
            # processes work great for cpu bound tasks. Takes advantage of multiple cores.
            proc = multiprocessing.Process(target=play_audio, args=(queue.get(),))
            proc.start()
            self._subprocesses.append(proc)

        for subprocess in self._subprocesses:
            subprocess.join()


    def stop(self):
        for process in self._subprocesses:
            if process.is_alive():
                process.terminate()
                process.join()
        # sd.stop()
