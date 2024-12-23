import multiprocessing
import numpy
from pysndfx import AudioEffectsChain


def add_track_fx(tracks):
    with multiprocessing.Pool() as pool:
        results = pool.map(process_track_fx, tracks)

    for track, processed_samples in zip(tracks, results):
        track.samples = processed_samples

    return tracks


def process_track_fx(track):
    fx = AudioEffectsChain()
    samples = track.samples

    for eq in track.get_audio_option('equalizers'):
        fx = fx.equalizer(
            frequency=eq['frequency'],
            q=eq['slope'],
            db=eq['db']
        )
    samples = fx(samples.T).T

    reverb_conf = track.get_audio_option('reverb')
    mix = reverb_conf.pop('mix', 1)

    if reverb_conf.get('reverberance', 0) > 0 and mix > 0:
        fx = fx.reverb(**reverb_conf)
        wet_samples = fx(samples.T).T
        if wet_samples.shape != samples.shape:
            wet_samples = wet_samples.reshape(samples.shape)

        dry_amount = 1 - mix
        wet_amount = mix
        samples = (samples * dry_amount) + (wet_samples * wet_amount)

    samples = samples * track.get_audio_option('volume')
    return samples


def add_self_cross_fade(samples, fade_samples):
    channel_count = 2 if samples.ndim == 2 else 1

    end_chunk = samples[-fade_samples:]
    start_chunk = samples[:fade_samples]
    fade_curve = numpy.linspace(0, 1, fade_samples, dtype=samples.dtype)

    crossfade = None
    if channel_count == 1:
        crossfade = (end_chunk * (1 - fade_curve)).astype(samples.dtype) + \
               (start_chunk * fade_curve).astype(samples.dtype)
    else:
        crossfade = (end_chunk * (1 - fade_curve)[:, numpy.newaxis]).astype(samples.dtype) + \
               (start_chunk * fade_curve[:, numpy.newaxis]).astype(samples.dtype)

    return crossfade