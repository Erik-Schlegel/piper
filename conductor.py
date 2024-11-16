import time
import threading
from audio import Audio

from config_helper import ConfigHelper

class Conductor:

    _subprocesses = []
    _path = None
    _CROSS_FADE_DURATION = .25


    def __init__(self, scene_name):
        self.load_scene(scene_name)


    def load_scene(self, scene_name):
        # print(ConfigHelper.get_merged_file_options('WinterCabin'))
        self._path = ConfigHelper.get_scene_files(scene_name)[0]['path']


    def start(self):
        self.add_track(self._path, True)
        while True:
          time.sleep(1) # sleep for 1 second


    def stop(self):
        for proc in self._subprocesses:
            proc.terminate()
            proc.wait() # w/o waiting the app doesn't fully close on quit


    def add_track(self, file_path, should_loop_indefinitely=False):
        def play_and_repeat():
            while True:
                track_duration = Audio.get_duration(file_path)
                self.register_proc(Audio.play_file(file_path, self._CROSS_FADE_DURATION))
                if track_duration is not None:
                    time.sleep(track_duration - self._CROSS_FADE_DURATION)
                else:
                    break

        try:
            if not should_loop_indefinitely:
                self.register_proc(Audio.play_file(file_path))
            else:
                thread = threading.Thread(target=play_and_repeat)
                thread.daemon = True  # This ensures the thread will exit when the main program exits
                thread.start()
        except Exception as e:
            print(f"An error occurred: {e}")
            return


    def register_proc(self, proc):
        self.cleanup_procs()
        self._subprocesses.append(proc)
        print(len(self._subprocesses))


    def cleanup_procs(self):
        self._subprocesses = [proc for proc in self._subprocesses if proc.poll() is None]
