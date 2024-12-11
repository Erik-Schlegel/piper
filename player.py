import signal
import sounddevice as sd
from pysndfx import AudioEffectsChain
import numpy as np

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
    track_options = track_options.get('options', {})

    fx = AudioEffectsChain()

    eq_conf = track_options.get('equalizers', {})
    for eq in eq_conf:
        fx = fx.equalizer(
            frequency=eq['frequency'],
            q=eq['slope'],
            db=eq['db']
        )
    samples = fx(samples.T).T

    reverb_conf = track_options.get('reverb', {}).copy()
    mix = reverb_conf.pop('mix', 1) # pop b/c "mix" isn't a valid arg

    if reverb_conf.get('reverberance', 0) > 0 and mix > 0:
        # Now reverb_conf only contains valid SoX parameters
        fx = fx.reverb(**reverb_conf)
        wet_samples = fx(samples.T).T
        if wet_samples.shape != samples.shape:
            wet_samples = wet_samples.reshape(samples.shape)

        # blend wet and dry samples
        dry_amount = 1 - mix
        wet_amount = mix
        samples = (samples * dry_amount) + (wet_samples * wet_amount)

    volume = track_options.get('volume', 1)
    return samples * volume