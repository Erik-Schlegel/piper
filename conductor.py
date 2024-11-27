# import time
# import threading
# from audio import Audio

import sounddevice as sd
import signal
import multiprocessing
from pysndfx import AudioEffectsChain

from audio_file_loader import load_tracks
from config_helper import ConfigHelper

class Conductor:

    _scene_name = None
    _subprocesses = None

    def __init__(self, scene_name):
        self._subprocesses = []
        self._scene_name = scene_name


    def start(self):
        tracks = ConfigHelper.get_scene_tracks_by_type(self._scene_name, 'simultaneous')
        if not isinstance(tracks, list):
            tracks = [tracks]

        file_queue = load_tracks(tracks)
        self.begin_playback(file_queue)


    def begin_playback(self, queue):
        while not queue.empty():
            # processes work great for cpu bound tasks. Takes advantage of multiple cores.
            proc = multiprocessing.Process(target=self.play_audio, args=(queue.get(),))
            proc.start()
            self._subprocesses.append(proc)

        for subprocess in self._subprocesses:
            subprocess.join()


    @staticmethod
    def play_audio(loaded_tracks):
        try:
            track_config = loaded_tracks[1]

            volume = track_config['options'].get('volume', 1)
            samples = loaded_tracks[0] * volume


            # overwrite the signal handlers for the child process.
            # we want ONLY the parent process to handle signals
            signal.signal(signal.SIGINT, signal.SIG_DFL)
            signal.signal(signal.SIGTERM, signal.SIG_DFL)

            fx = (
                AudioEffectsChain()
                    .reverb(reverberance=80, hf_damping=20,
                        room_scale=4, stereo_depth=75,
                        pre_delay=0, wet_gain=1,
                        wet_only=False
                    )
            )

            # Applying fx inverts the shape of samples. Transpose to correct it.
            processed_samples = fx(samples).T

            if processed_samples.ndim == 1:
                channels = 1
            elif processed_samples.ndim == 2:
                channels = processed_samples.shape[1]
            else:
                raise ValueError("Invalid audio data shape")

            with sd.OutputStream(samplerate=41000, channels=channels) as stream:
                stream.write(processed_samples)


        except Exception as e:
            print(f"An unexpected error occurred: {e}")
        finally:
            sd.stop()


    # def _add_track(self, track):
    #     try:
    #         options = track.get('options', {})

    #         if options.get('loop'):
    #             # thread allows the main thread to continue running while this one runs indefinitely.
    #             # W/o this main would wait for _add_track->_play_and_repeat to complete (which it never does).
    #             thread = threading.Thread(target=self._play_and_repeat, args=(track,))
    #             thread.daemon = True  # ensure thread will exit when the main exits
    #             thread.start()
    #         else:
    #             play_proc = Audio.play_file(track.get('path'), options)
    #             self._register_proc(play_proc)
    #     except Exception as e:
    #         print(f"An error occurred: {e}")
    #         return


    # def _play_and_repeat(self, track):
    #     track_duration = Audio.get_duration(track['path'])
    #     cross_fade_duration = track['options'].get('crossFadeDuration', .25)
    #     while True:
    #         play_proc = Audio.play_file(track)
    #         self._register_proc(play_proc)
    #         time.sleep(track_duration - cross_fade_duration)


    # def _register_proc(self, proc):
    #     self._subprocesses.append(proc)

    #     thread = threading.Thread(target=self._wait_for_proc, args=(proc,))
    #     thread.daemon = True  # Ensure thread will exit when the main exits
    #     thread.start()


    # def _wait_for_proc(self, proc):
    #     proc.wait()
    #     self._cleanup_procs()


    # def _cleanup_procs(self):
    #     self._subprocesses = [proc for proc in self._subprocesses if proc.poll() is None]


    def stop(self):
        for process in self._subprocesses:
            if process.is_alive():
                process.terminate()
                process.join()
        sd.stop()
