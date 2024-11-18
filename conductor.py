import time
import threading
from audio import Audio

from config_helper import ConfigHelper

class Conductor:

    _subprocesses = []

    _scene_name = None


    def __init__(self, scene_name):
        self._scene_name = scene_name


    def start(self):
        tracks = ConfigHelper.get_scene_tracks_by_type(self._scene_name, 'simultaneous')
        for track in tracks:
            self.add_track(track)


    def stop(self):
        for proc in self._subprocesses:
            proc.terminate()
            proc.wait() # w/o waiting the app doesn't fully close on quit


    def add_track(self, track):
        try:
            options = track.get('options', {})

            if not options.get('loop'):
                self.register_proc(Audio.play_file(track.get('path'), options))
            else:
                # thread allows the main thread to continue running while this one runs indefinitely.
                # W/o this main would wait for add_track->play_and_repeat to complete (which it never does).
                thread = threading.Thread(target=self.play_and_repeat, args=(track,))
                thread.daemon = True  # ensure thread will exit when the main exits
                thread.start()
        except Exception as e:
            print(f"An error occurred: {e}")
            return


    def register_proc(self, proc):
        self.cleanup_procs()
        self._subprocesses.append(proc)


    def cleanup_procs(self):
        self._subprocesses = [proc for proc in self._subprocesses if proc.poll() is None]


    def play_and_repeat(self, track):
        track_duration = Audio.get_duration(track['path'])
        cross_fade_duration = track['options'].get('crossFadeDuration', 250)
        while True:
            self.register_proc(Audio.play_file(track))
            if track_duration is not None:
                time.sleep(track_duration - cross_fade_duration)
            else:
                break

