## GENERATED FILE, DO NOT MODIFY

import json
from main import app

BUILD_VER = '10bfeac2d120b1b6e4fe7182fe5826005128f019'

@app.route('/build_info')
def buildInfo():
    return json.dumps({
        "ver": BUILD_VER
    })

