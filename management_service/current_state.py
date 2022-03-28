from flask import Response
from main import app
from tstatcommon.data import filenames

@app.route("/current_state", methods=["GET"])
def current_state():
    with open(filenames.STATE_FILE, "r") as state:
        return Response(state.read(), mimetype="application/json")
