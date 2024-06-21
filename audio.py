import sounddevice as sd
from pydub import AudioSegment
import logging
import numpy as np
import threading

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


def apply_fades_and_crossfade(audio_segment, fade_duration, crossfade_duration):
    # Apply fade-in
    audio_segment = audio_segment.fade_in(fade_duration)

    # Apply crossfade to create a seamless loop
    if crossfade_duration > 0:
        crossfade_segment = (
            audio_segment[-crossfade_duration:]
            .fade_out(crossfade_duration)
            .overlay(audio_segment[:crossfade_duration].fade_in(crossfade_duration))
        )
        audio_segment = audio_segment[:-crossfade_duration] + crossfade_segment

    return audio_segment


def play_audio(
    file,
    gain_db,
    trim_start=0,
    trim_end=0,
    fade_duration=10,
    crossfade_duration=10,
    stop_event=None,
):
    try:
        logging.info(f"Loading audio file: {file}")
        audio_segment = AudioSegment.from_file(file)
        logging.debug("Audio file loaded successfully")

        # Apply gain adjustment
        audio_segment += gain_db
        logging.debug(f"Applied gain adjustment: {gain_db} dB")

        # Trim audio segment
        duration = len(audio_segment)
        audio_segment = audio_segment[trim_start : duration - trim_end]
        logging.debug(
            f"Trimmed audio segment: trim_start={trim_start}ms, trim_end={trim_end}ms"
        )

        # Apply fades and crossfade
        audio_segment = apply_fades_and_crossfade(
            audio_segment, fade_duration, crossfade_duration
        )
        logging.debug(f"Applied fade-in and crossfade of {crossfade_duration}ms")

        # Convert audio segment to numpy array
        audio_data = np.array(audio_segment.get_array_of_samples()).reshape(
            (-1, audio_segment.channels)
        ).astype(np.float32) / (1 << 15)
        frame_rate = audio_segment.frame_rate
        num_channels = audio_segment.channels

        logging.debug(f"Audio data: channels={num_channels}, frame rate={frame_rate}")

        def callback(outdata, frames, time, status):
            if status:
                logging.warning(status)
            start = callback.counter
            end = start + frames
            if end >= len(audio_data):
                outdata[: len(audio_data) - start] = audio_data[start:]
                outdata[len(audio_data) - start :] = audio_data[
                    : frames - (len(audio_data) - start)
                ]
                callback.counter = frames - (len(audio_data) - start)
            else:
                outdata[:] = audio_data[start:end]
                callback.counter += frames

            if stop_event is not None and stop_event.is_set():
                raise sd.CallbackStop

        callback.counter = 0

        with sd.OutputStream(
            samplerate=frame_rate,
            channels=num_channels,
            callback=callback,
            blocksize=4096,
        ) as stream:
            logging.info("Audio playback started")
            while not (stop_event and stop_event.is_set()):
                sd.sleep(100)
            logging.info("Playback finished")
    except Exception as e:
        logging.error(f"Error playing file {file}: {e}")
