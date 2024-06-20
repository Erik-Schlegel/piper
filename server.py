from flask import Flask, request, jsonify
from audio import play_audio
import logging

# Configure logging
logging.basicConfig(
    level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s"
)

app = Flask(__name__)


@app.route("/play", methods=["POST"])
def play():
    config = request.json
    file_path = config.get("file_path")
    gain_db = config.get("gain_db", 0)  # Default gain to 0 if not provided
    trim_start = config.get("trim_start", 0)  # Default trim_start to 0 if not provided
    trim_end = config.get("trim_end", 0)  # Default trim_end to 0 if not provided
    if not file_path:
        return jsonify(status="error", message="file_path is required"), 400

    try:
        play_audio(file_path, gain_db, trim_start, trim_end)
        return jsonify(
            status="success",
            message="Playing",
            file_path=file_path,
            gain_db=gain_db,
            trim_start=trim_start,
            trim_end=trim_end,
        )
    except RuntimeError as e:
        return jsonify(status="error", message=str(e)), 500


@app.route("/stop", methods=["POST"])
def stop():
    # Placeholder for stop functionality
    return jsonify(status="success", message="Stop command received")


@app.route("/ping", methods=["GET"])
def ping():
    return jsonify(status="success", message="pong")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000)
