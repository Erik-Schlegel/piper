from flask import Flask, request, jsonify
from audio import play_audio
import logging
import threading

# Configure logging
logging.basicConfig(
    level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s"
)

app = Flask(__name__)

# Global dictionaries to keep track of threads, events, and active data
audio_threads = {}
stop_events = {}


def play_sound(
    file_path, gain_db, trim_start, trim_end, fade_duration, crossfade_duration
):
    try:
        play_audio(
            file_path,
            gain_db,
            trim_start,
            trim_end,
            fade_duration,
            crossfade_duration,
            stop_events[file_path],
        )
    except RuntimeError as e:
        logging.error(f"Error playing {file_path}: {e}")


@app.route("/play", methods=["POST"])
def play():
    config = request.json
    sounds = config.get("sounds")
    global_fade_duration = config.get("fade_duration", 5)

    # Global default fade duration
    global_crossfade_duration = config.get("crossfade_duration", 10)

    # Global default crossfade duration
    if not sounds or not isinstance(sounds, list):
        return jsonify(status="error", message="sounds array is required"), 400

    for sound in sounds:
        file_path = sound.get("file_path")

        if not file_path:
            return (
                jsonify(status="error", message="file_path is required for each sound"),
                400,
            )

        gain_db = sound.get("gain_db", 0)
        trim_start = sound.get("trim_start", 0)
        trim_end = sound.get("trim_end", 0)
        fade_duration = sound.get("fade_duration", global_fade_duration)
        crossfade_duration = sound.get("crossfade_duration", global_crossfade_duration)

        thread = threading.Thread(
            target=play_sound,
            args=(
                file_path,
                gain_db,
                trim_start,
                trim_end,
                fade_duration,
                crossfade_duration,
            ),
        )
        audio_threads[file_path] = thread
        stop_events[file_path] = threading.Event()
        thread.start()

    return jsonify(status="success", message="All sounds are playing")


@app.route("/stop", methods=["POST"])
def stop():
    sound_paths = request.json.get("sound_paths")

    if sound_paths:
        if not isinstance(sound_paths, list):
            return jsonify(status="error", message="sound_paths must be a list"), 400

        for file_path in sound_paths:
            if file_path in stop_events:
                stop_events[file_path].set()
                audio_threads[file_path].join()
                del stop_events[file_path]
                del audio_threads[file_path]

        return jsonify(status="success", message="Specified sounds stopped")

    else:
        # Stop all sounds
        for file_path in list(stop_events.keys()):
            stop_events[file_path].set()
            audio_threads[file_path].join()
            del stop_events[file_path]
            del audio_threads[file_path]

        return jsonify(status="success", message="All sounds stopped")


@app.route("/update", methods=["POST"])
def update():
    data = request.json
    sounds = data.get("sounds")

    if not sounds:
        return jsonify(status="error", message="No sounds provided"), 400

    for sound in sounds:
        file_path = sound.get("file_path")
        gain_db = sound.get("gain_db")

        if not file_path or gain_db is None:
            return (
                jsonify(
                    status="error",
                    message="file_path and gain_db are required for each sound",
                ),
                400,
            )

        # Update the gain for the playing audio
        # update_audio_gain(file_path, gain_db)
        app.logger.info(f"Received update for {file_path} with gain_db={gain_db}")

    return jsonify(status="success", message="Sounds update received")


@app.route("/ping", methods=["GET"])
def ping():
    return jsonify(status="success", message="pong")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000)
