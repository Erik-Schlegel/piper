from queue import Queue
import soundfile as sf
import threading
import numpy


def load_tracks(tracks):
    file_queue = Queue()
    threads = []

    if not isinstance(tracks, list):
        tracks = [tracks]

    try:
        for track in tracks:
            # threads work well for disk io and non cpu-bound tasks
            thread = threading.Thread(target=load_as_numpy, args=(track, file_queue))
            threads.append(thread)
            thread.start()

        for thread in threads:
            thread.join()

        return file_queue

    except Exception as e:
        print(f'Error: {e}')


def load_as_numpy(track, queue):
    samples, sample_rate = sf.read(track['path'], dtype='int16')

    # Normalize for sounddevice playback
    samples = samples / (2 ** 15)
    samples = samples.astype(numpy.float32)

    queue.put((samples, sample_rate, track))
