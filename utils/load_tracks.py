import os
import json
import prctl
import numpy
import threading
import soundfile
import hashlib
from typing import List


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

    hashed_cfg = get_hash(track_cfg)
    hashed_path = f"{PREPROCESSED_FOLDER}/{hashed_cfg}"

    if os.path.exists(hashed_path):
        track_cfg['from_preprocess'] = True
        samples, sample_rate = _load_preprocessed_sample_data(hashed_path)
    else:
        filepath = track_cfg['path']
        samples, sample_rate = _load_sample_data(filepath)
        track_cfg['hashpath'] = hashed_path
        # soundfile.write(hashed_path, samples, sample_rate, format='MP3')

    results[index] = Track(track_cfg, samples, sample_rate)


def _load_preprocessed_sample_data(filepath):
    samples, sample_rate = soundfile.read(filepath, dtype='float32')
    print('from pre')
    return (samples, sample_rate)



def _load_sample_data(filepath):
    samples, sample_rate = soundfile.read(filepath, dtype='int16')

    # Normalize for sounddevice playback
    samples = samples / (2 ** 15)
    samples = samples.astype(numpy.float32)

    return (samples, sample_rate)


def get_hash(obj):
    obj_str = json.dumps(obj, sort_keys=True)
    hash_obj = hashlib.sha256(obj_str.encode('utf-8'))
    return hash_obj.hexdigest()




