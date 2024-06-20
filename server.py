from flask import Flask, request, jsonify
from audio import play_audio
import logging
import threading

# Configure logging
logging.basicConfig(
    level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s"
)

app = Flask(__name__)


def play_sound(
    file_path, gain_db, trim_start, trim_end, fade_duration, crossfade_duration
):
    try:
        play_audio(
            file_path, gain_db, trim_start, trim_end, fade_duration, crossfade_duration
        )
    except RuntimeError as e:
        logging.error(f"Error playing {file_path}: {e}")


@app.route("/play", methods=["POST"])
def play():
    config = request.json
    sounds = config.get("sounds")
    global_fade_duration = config.get(
        "fade_duration", 5
    )  # Global default fade duration
    global_crossfade_duration = config.get(
        "crossfade_duration", 10
    )  # Global default crossfade duration

    if not sounds or not isinstance(sounds, list):
        return jsonify(status="error", message="sounds array is required"), 400

    threads = []
    for sound in sounds:
        file_path = sound.get("file_path")
        gain_db = sound.get("gain_db", 0)  # Default gain to 0 if not provided
        trim_start = sound.get(
            "trim_start", 0
        )  # Default trim_start to 0 if not provided
        trim_end = sound.get("trim_end", 0)  # Default trim_end to 0 if not provided
        fade_duration = sound.get(
            "fade_duration", global_fade_duration
        )  # Use individual or global fade_duration
        crossfade_duration = sound.get(
            "crossfade_duration", global_crossfade_duration
        )  # Use individual or global crossfade_duration

        if not file_path:
            return (
                jsonify(status="error", message="file_path is required for each sound"),
                400,
            )

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
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    return jsonify(status="success", message="All sounds are playing")


@app.route("/stop", methods=["POST"])
def stop():
    # Placeholder for stop functionality
    return jsonify(status="success", message="Stop command received")


@app.route("/ping", methods=["GET"])
def ping():
    return jsonify(status="success", message="pong")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000)
