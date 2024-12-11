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
        self._scene_name = scene_name
        self._subprocesses = []


    def start(self):

        self.play_simultaneous(self._scene_name)

        track_sets = ConfigHelper.get_shuffled_track_sets(self._scene_name)

        for track_set in track_sets:
            proc = multiprocessing.Process(target=Conductor.play_intermittent, args=(self._scene_name, track_set))
            proc.start()
            self._subprocesses.append(proc)

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


    @staticmethod
    def play_intermittent(scene_name, track_set):
        try:

            tracks = track_set['tracks']
            while True:
                if not isinstance(tracks, list):
                    tracks = [tracks]
                random.shuffle(tracks)

                for track in tracks:
                    try:
                        minIntermissionSeconds, maxIntermissionSeconds = track_set.get('intermissionSeconds')
                        sleep_time = random.randint(minIntermissionSeconds, maxIntermissionSeconds)
                        print(f"Sleep for {sleep_time} seconds")
                        sleep(sleep_time)

                        loaded_track = load_tracks(track)
                        proc = multiprocessing.Process(target=play_audio, args=(loaded_track.get(),))
                        print(f"Playing {track['path']}")
                        proc.start()

                        # Wait for audio track end
                        proc.join()
                    except KeyboardInterrupt:
                        if proc and proc.is_alive():
                            proc.terminate()
                            proc.join()
                        return
                    except Exception as e:
                        print(f"Error: {e}")
                        continue

        except KeyboardInterrupt:
            if proc and proc.is_alive():
                proc.terminate()
                proc.join()
            return
        except Exception as e:
            print(f"Error: {e}")


    def stop(self):
        for process in self._subprocesses:
            if process.is_alive():
                process.terminate()
                process.join()
