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


    def add_track(self, track):
        try:
            options = track.get('options', {})

            if options.get('loop'):
                # thread allows the main thread to continue running while this one runs indefinitely.
                # W/o this main would wait for add_track->play_and_repeat to complete (which it never does).
                thread = threading.Thread(target=self.play_and_repeat, args=(track,))
                thread.daemon = True  # ensure thread will exit when the main exits
                thread.start()
            else:
                play_proc = Audio.play_file(track.get('path'), options)
                self.register_proc(play_proc)
        except Exception as e:
            print(f"An error occurred: {e}")
            return


    def play_and_repeat(self, track):
        track_duration = Audio.get_duration(track['path'])
        cross_fade_duration = track['options'].get('crossFadeDuration', .25)
        while True:
            play_proc = Audio.play_file(track)
            self.register_proc(play_proc)
            time.sleep(track_duration - cross_fade_duration)


    def register_proc(self, proc):
        self._subprocesses.append(proc)

        thread = threading.Thread(target=self.wait_for_proc, args=(proc,))
        thread.daemon = True  # Ensure thread will exit when the main exits
        thread.start()


    def wait_for_proc(self, proc):
        proc.wait()
        self.cleanup_procs()


    def cleanup_procs(self):
        self._subprocesses = [proc for proc in self._subprocesses if proc.poll() is None]


    def stop(self):
        for proc in self._subprocesses:
            try:
                proc.terminate()
                proc.wait()  # Wait for the process to terminate
            except Exception as e:
                print(f"An error occurred while terminating process: {e}")
        self._subprocesses.clear()  # Clear the list of subprocesses
