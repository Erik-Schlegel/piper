from flask import Flask, jsonify, request

app = Flask(__name__)


# Define a simple route
@app.route("/")
def home():
    return "Welcome to the Flask API!"


# Define an example API route
@app.route("/api/hello", methods=["GET"])
def hello():
    name = request.args.get("name", "World")
    return jsonify(message=f"Hello, {name}!")


# Run the app
if __name__ == "__main__":
    app.run(debug=True)
