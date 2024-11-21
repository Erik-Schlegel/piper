import threading
import multiprocessing
from queue import Queue
import numpy as np
import signal
import sys

from pydub import AudioSegment
import sounddevice as sd


processes = []


def main():

    add_signal_handlers()
    file_queue = thread_load_files([
        'resources/clock_short.wav',
        'resources/fire_short.wav',
        'resources/snow_short.wav'
    ])
    begin_playback(file_queue)


def thread_load_files(file_paths):
    file_queue = Queue()
    threads = []

    try:
        for file_path in file_paths:
            # threads work well for disk io, and non-cpu bound tasks
            thread = threading.Thread(target=load_as_numpy, args=(file_path, file_queue))
            threads.append(thread)
            thread.start()

        for thread in threads:
            thread.join()

        return file_queue

    except Exception as e:
        print(f'Error: {e}')


def load_as_numpy(file_path, queue):
    audio_segment = AudioSegment.from_file(file_path)
    samples = np.array(audio_segment.get_array_of_samples())
    if audio_segment.channels == 2:
        samples = samples.reshape(-1, 2)
    samples = samples / (2 ** (8 * audio_segment.sample_width - 1))  # Normalize for sounddevice
    samples = samples.astype(np.float32)  # Convert to float32
    queue.put(samples)


def begin_playback(queue):
    global processes

    while not queue.empty():
        audio_samples = queue.get()
        # processes work well for cpu bound tasks, not for io bound tasks. Takes advantage of multiple cores
        process = multiprocessing.Process(target=play_audio, args=(audio_samples,))
        process.start()
        processes.append(process)

    for process in processes:
        process.join()


def play_audio(samples):
    try:
        # overwrite the signal handlers for the child process.
        # we want ONLY the parent process to handle signals
        signal.signal(signal.SIGINT, signal.SIG_DFL)
        signal.signal(signal.SIGTERM, signal.SIG_DFL)

        # Use OutputStream to avoid issues with playback.
        with sd.OutputStream(samplerate=41000, channels=samples.shape[1] if samples.ndim > 1 else 1) as stream:
            stream.write(samples)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    finally:
        sd.stop()


def add_signal_handlers():
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)


def signal_handler(sig, frame):
    for process in processes:
        if process.is_alive():
            process.terminate()
            process.join()
    sd.stop()
    sys.exit(0)


if __name__ == "__main__":
    try:
        multiprocessing.set_start_method('spawn')
        main()
    except KeyboardInterrupt:
        signal_handler(signal.SIGINT, None)
