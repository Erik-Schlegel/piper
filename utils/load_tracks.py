import json
import prctl
import numpy
import threading
import soundfile
import hashlib
from typing import List

from utils.preprocessed_file_helper import get_hashed_path, is_hashed_path_existing
from track import Track


PREPROCESSED_FOLDER = 'resources/preprocessed'



def load_tracks(tracks:list) -> List[Track]:
    if not isinstance(tracks, list):
        tracks = [tracks]

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

    if is_hashed_path_existing(track_cfg):
        samples, sample_rate = _load_preprocessed_sample_data(get_hashed_path(track_cfg))
    else:
        samples, sample_rate = _load_sample_data(track_cfg['path'])

    results[index] = Track(track_cfg, samples, sample_rate)


def _load_preprocessed_sample_data(filepath):
    samples, sample_rate = soundfile.read(filepath, dtype='float32')
    return (samples, sample_rate)


def _load_sample_data(filepath):
    samples, sample_rate = soundfile.read(filepath, dtype='int16')

    # Normalize for sounddevice playback
    samples = samples / (2 ** 15)
    samples = samples.astype(numpy.float32)

    return (samples, sample_rate)
