from queue import Queue
import soundfile as sf
import threading
import numpy


def load_tracks(tracks):
    results = [None] * len(tracks)
    threads = []

    try:
        for index, track in enumerate(tracks):
            thread = threading.Thread(target=get_playable_track, args=(track, results, index))
            threads.append(thread)
            thread.start()

        for thread in threads:
            thread.join()

        return results

    except Exception as e:
        print(f'Error: {e}')


def get_playable_track(track, results, index):
    samples, sample_rate = load_sample_data(track['path'])
    results[index] = track, samples, sample_rate


def load_sample_data(filepath):
    samples, sample_rate = sf.read(filepath, dtype='int16')

    # Normalize for sounddevice playback
    samples = samples / (2 ** 15)
    samples = samples.astype(numpy.float32)

    return (samples, sample_rate)
