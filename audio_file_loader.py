from pydub import AudioSegment
from queue import Queue
import threading
import numpy as np


def load_tracks(tracks):
    file_queue = Queue()
    threads = []

    try:
        for track in tracks:
            # threads work well for disk io, and non-cpu bound tasks
            thread = threading.Thread(target=load_as_numpy, args=(track, file_queue))
            threads.append(thread)
            thread.start()

        for thread in threads:
            thread.join()

        return file_queue

    except Exception as e:
        print(f'Error: {e}')


def load_as_numpy(track, queue):
    audio_segment = AudioSegment.from_file(track['path'])
    samples = np.array(audio_segment.get_array_of_samples())
    if audio_segment.channels == 2:
        samples = samples.reshape(-1, 2)
    samples = samples / (2 ** (8 * audio_segment.sample_width - 1))  # Normalize for sounddevice
    samples = samples.astype(np.float32)
    queue.put((samples, track))