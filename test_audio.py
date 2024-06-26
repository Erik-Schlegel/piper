import sounddevice as sd
from pydub import AudioSegment
import logging
import numpy as np
import argparse

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


def play_audio(file, gain_db):
    try:
        logging.info(f"Loading audio file: {file}")
        audio_segment = AudioSegment.from_file(file)
        logging.debug("Audio file loaded successfully")

        # Apply gain adjustment
        audio_segment += gain_db
        logging.debug(f"Applied gain adjustment: {gain_db} dB")

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

        callback.counter = 0

        with sd.OutputStream(
            samplerate=frame_rate,
            channels=num_channels,
            callback=callback,
            blocksize=4096,
        ) as stream:
            logging.info("Audio playback started")
            while callback.counter < len(audio_data):
                sd.sleep(100)
            logging.info("Playback finished")
    except Exception as e:
        logging.error(f"Error playing file {file}: {e}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Play an audio file with gain adjustment."
    )
    parser.add_argument("file", type=str, help="Path to the audio file")
    parser.add_argument("gain_db", type=float, help="Gain volume adjustment in dB")
    args = parser.parse_args()

    play_audio(args.file, args.gain_db)
