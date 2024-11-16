import time
import threading
from audio import Audio

from config_helper import ConfigHelper

class Conductor:

    subprocesses = []
    scene_data = None
    path = None
    cross_fade_duration = .25


    def __init__(self, scene_name):
        self.load_scene(scene_name)


    def load_scene(self, scene_name):
        # print(ConfigHelper.get_merged_file_options('WinterCabin'))
        self.path = ConfigHelper.get_scene_files(scene_name)[0]['path']


    def start(self):
        self.add_track(self.path, True)
        while True:
          time.sleep(1) # sleep for 1 second


    def stop(self):
        for proc in self.subprocesses:
            proc.terminate()
            proc.wait() # w/o waiting the app doesn't fully close on quit


    def add_track(self, file_path, should_loop_indefinitely=False):
        def play_and_repeat():
            while True:
                track_duration = Audio.get_duration(file_path)
                self.register_proc(Audio.play_file(file_path, self.cross_fade_duration))
                if track_duration is not None:
                    time.sleep(track_duration - self.cross_fade_duration)
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
        self.cleanup_subprocesses()
        self.subprocesses.append(proc)
        print(len(self.subprocesses))


    def cleanup_procs(self):
        self.subprocesses = [proc for proc in self.subprocesses if proc.poll() is None]
