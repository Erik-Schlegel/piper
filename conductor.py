import multiprocessing
import random

from time import sleep
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
        self.play_simultaneous(self._scene_name)
        self.play_intermittent(self._scene_name)

        for subprocess in self._subprocesses:
            subprocess.join()


    def play_simultaneous(self, scene_name):
        tracks = ConfigHelper.get_tracks_by_type(scene_name, 'simultaneous')
        if not isinstance(tracks, list):
            tracks = [tracks]
        tracks = load_tracks(tracks)

        while not tracks.empty():
            proc = multiprocessing.Process(target=loop_audio, args=(tracks.get(),))
            proc.start()
            self._subprocesses.append(proc)


    def play_intermittent(self, scene_name):
        while True:
            # tracks = ConfigHelper.get_shuffled_tracks(scene_name)
            tracks = ConfigHelper.get_tracks_by_type(scene_name, 'shuffled')
            if not isinstance(tracks, list):
                tracks = [tracks]

            random.shuffle(tracks)

            for track in tracks:
                minIntermissionSeconds, maxIntermissionSeconds = ConfigHelper.get_intermission_seconds_minmax(scene_name)
                sleep_time = random.randint(minIntermissionSeconds, maxIntermissionSeconds)
                print(f"Sleeping for {sleep_time} seconds")
                sleep(sleep_time)

                loaded_track = load_tracks(track)
                proc = multiprocessing.Process(target=play_audio, args=(loaded_track.get(),))
                print(f"Playing {track['path']}")
                proc.start()
                self._subprocesses.append(proc)

                # Wait for song end
                proc.join()
                self._subprocesses.remove(proc)


    def stop(self):
        for process in self._subprocesses:
            if process.is_alive():
                process.terminate()
                process.join()
