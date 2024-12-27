from typing import List
import prctl

import threading
import soundfile
import numpy

from track import Track


def load_tracks(tracks:list) -> List[Track]:
        threads = []
        result_tracks = [None] * len(tracks)

        for index, track_cfg in enumerate(tracks):
            thread = threading.Thread(target=_get_playable_track, args=(track_cfg, result_tracks, index))
            threads.append(thread)
            thread.start()

        for thread in threads:
            thread.join()

        return result_tracks


def _get_playable_track(track_cfg, results, index):
    prctl.set_name(f'load_tracks:{track_cfg["path"]}')
    samples, sample_rate = _load_sample_data(track_cfg['path'])
    results[index] = Track(track_cfg, samples, sample_rate)


def _load_sample_data(filepath):
    try:

        samples, sample_rate = soundfile.read(filepath, dtype='int16')

        # Normalize for sounddevice playback
        samples = samples / (2 ** 15)
        samples = samples.astype(numpy.float32)

        return (samples, sample_rate)

    except Exception as e:
        raise FileNotFoundError(f'Could not load track file{filepath}')
