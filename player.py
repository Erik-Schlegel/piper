import signal
import sounddevice as sd
from pysndfx import AudioEffectsChain


def play_audio(track):
    try:
        # Ignore signal handlers for the child process so we don't try to kill the proc more than once.
        signal.signal(signal.SIGINT, signal.SIG_DFL)
        signal.signal(signal.SIGTERM, signal.SIG_DFL)

        samples = get_processed_samples(track)
        if samples.ndim == 1:
            channels = 1
        elif samples.ndim == 2:
            channels = samples.shape[1]
        else:
            raise ValueError("Invalid audio data shape")

        with sd.OutputStream(samplerate=41000, channels=channels) as stream:
            stream.write(samples)


    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    finally:
        sd.stop()


def get_processed_samples(track):
    track_config = track[1]
    volume = track_config['options'].get('volume', 1)

    fx = get_fx_chain(track_config)
    return (fx(track[0] * volume).T)  # fx inverts shape of samples; '.T' transposes it back.


def get_fx_chain(track_config):

    fx = AudioEffectsChain()

    reverb_conf = track_config.get('options',{}).get('reverb', {})

    if reverb_conf.get('reverberance', 0) > 0:
        print(f'applying reverb to track: {track_config["path"]}')
        fx = fx.reverb(**reverb_conf)
    else:
        print(f'not applying reverb to track: {track_config["path"]}')

    return fx

