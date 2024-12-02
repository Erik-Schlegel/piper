import signal
import sounddevice as sd
from pysndfx import AudioEffectsChain
import numpy as np
import multiprocessing

def ignore_signals():
        # Play calls are handled in a separate process. Ignore signal handlers
        # internally, oherwise we get errors on exit.
        signal.signal(signal.SIGINT, signal.SIG_DFL)
        signal.signal(signal.SIGTERM, signal.SIG_DFL)


def play_audio(track):
    try:
        ignore_signals()

        sample_rate = track[1]
        samples = get_fx_processed_samples(track)
        channel_count = 2 if samples.ndim == 2 else 1
        with sd.OutputStream(samplerate=sample_rate, channels=channel_count) as stream:
            stream.write(samples)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    finally:
        sd.stop()


def loop_audio(track):
    try:
        ignore_signals()

        samples = get_fx_processed_samples(track)
        track_options = track[2].get('options', {})

        sample_rate = track[1]
        fade_samples = int((track_options.get('crossFadeDuration', 0.25)) * sample_rate)

        crossfade_samples = get_crossfade_samples(samples, fade_samples)

        channel_count = 2 if samples.ndim == 2 else 1
        with sd.OutputStream(samplerate=sample_rate, channels=channel_count) as stream:
            while True:
                if channel_count == 1:
                    stream.write(samples[:-fade_samples])
                else:
                    stream.write(samples[:-fade_samples, :])

                if (track_options.get('loop', False)):
                    stream.write(crossfade_samples)

    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    finally:
        sd.stop()


def get_crossfade_samples(samples, fade_samples):
    channel_count = 2 if samples.ndim == 2 else 1

    end_chunk = samples[-fade_samples:]
    start_chunk = samples[:fade_samples]
    fade_curve = np.linspace(0, 1, fade_samples, dtype=samples.dtype)

    crossfade = None
    if channel_count == 1:
        crossfade = (end_chunk * (1 - fade_curve)).astype(samples.dtype) + \
               (start_chunk * fade_curve).astype(samples.dtype)
    else:
        crossfade = (end_chunk * (1 - fade_curve)[:, np.newaxis]).astype(samples.dtype) + \
               (start_chunk * fade_curve[:, np.newaxis]).astype(samples.dtype)

    return crossfade


def get_fx_processed_samples(track):
    samples, _, track_options = track
    volume = track_options['options'].get('volume', 1)

    fx = AudioEffectsChain()

    reverb_conf = track_options.get('options', {}).get('reverb', {})

    if reverb_conf.get('reverberance', 0) > 0:
        fx = fx.reverb(**reverb_conf)

    processed_samples = fx((samples * volume).T).T

    # Ensure the processed_samples have the same shape as the original samples
    if processed_samples.shape != samples.shape:
        processed_samples = processed_samples.reshape(samples.shape)

    return processed_samples