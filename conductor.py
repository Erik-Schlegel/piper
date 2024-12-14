import multiprocessing
import random
from time import sleep


from audio_file_loader import load_tracks
from player import play_audio, loop_audio
from n_config_helper import NConfigHelper
from enums.play_mode import PlayMode


class Conductor:

    _config = None
    _subprocesses = None

    def __init__(self, scene_name):
        self._subprocesses = []
        self._config = NConfigHelper(scene_name)


    def start_playback(self):
        for layer_set in self._config.get_layer_sets():
            play_mode = PlayMode.get_mode(layer_set.get('play_mode', None))
            play_fn = ({
                PlayMode.ORDERED: self.play_ordered,
                PlayMode.SHUFFLED: self.play_shuffled,
                PlayMode.SIMULTANEOUS: self.play_simultaneous
            }.get(play_mode))

            name = layer_set.get('name', None)
            if play_fn is None or name is None:
                continue

            proc = multiprocessing.Process(
                target=play_fn,
                args=(
                    self._config.get_layer_set_tracks(name),
                    layer_set.get('loop', False),
                    layer_set.get('intermission', 3))
            )
            proc.start()
            self._subprocesses.append(proc)


        for subprocess in self._subprocesses:
            subprocess.join()


    def play_simultaneous(self, tracks, loop, intermission):
        if not isinstance(tracks, list):
            tracks = [tracks]
        tracks = load_tracks(tracks)

        while not tracks.empty():
            proc = multiprocessing.Process(target=loop_audio, args=(tracks.get(),))
            proc.start()
            self._subprocesses.append(proc)


    def play_consecutive(self, tracks, loop, intermission, shuffle=False):
        print("-------")
        print(f"Track Count: {len(tracks)}")
        print(f"Playing shuffled")
        print(f"loop: {loop}, intermission: {intermission}, shuffle: {shuffle}")
        # print(json.dumps(tracks, indent=2))


    def play_ordered(self, tracks, loop, intermission):
        self.play_consecutive(tracks, loop, intermission, shuffle=False)


    def play_shuffled(self, tracks, loop, intermission):
        self.play_consecutive(tracks, loop, intermission, shuffle=True)




    def o_play_simultaneous(self, scene_name):
        pass
        # tracks = ConfigHelper.get_tracks_by_type(scene_name, 'simultaneous')
        # if not isinstance(tracks, list):
        #     tracks = [tracks]
        # tracks = load_tracks(tracks)

        # while not tracks.empty():
        #     proc = multiprocessing.Process(target=loop_audio, args=(tracks.get(),))
        #     proc.start()
        #     self._subprocesses.append(proc)


    @staticmethod
    def o_play_intermittent(scene_name, track_set):
        pass
        # try:

        #     tracks = track_set['tracks']
        #     while True:
        #         if not isinstance(tracks, list):
        #             tracks = [tracks]
        #         random.shuffle(tracks)

        #         for track in tracks:
        #             try:
        #                 minIntermissionSeconds, maxIntermissionSeconds = track_set.get('intermissionSeconds')
        #                 sleep_time = random.randint(minIntermissionSeconds, maxIntermissionSeconds)
        #                 print(f"Sleep for {sleep_time} seconds")
        #                 sleep(sleep_time)

        #                 loaded_track = load_tracks(track)
        #                 proc = multiprocessing.Process(target=play_audio, args=(loaded_track.get(),))
        #                 print(f"Playing {track['path']}")
        #                 proc.start()

        #                 # Wait for audio track end
        #                 proc.join()
        #             except KeyboardInterrupt:
        #                 if proc and proc.is_alive():
        #                     proc.terminate()
        #                     proc.join()
        #                 return
        #             except Exception as e:
        #                 print(f"Error: {e}")
        #                 continue

        # except KeyboardInterrupt:
        #     if proc and proc.is_alive():
        #         proc.terminate()
        #         proc.join()
        #     return
        # except Exception as e:
        #     print(f"Error: {e}")


    def stop_playback(self):
        for process in self._subprocesses:
            if process.is_alive():
                process.terminate()
                process.join()
