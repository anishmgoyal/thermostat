## GENERATED FILE, DO NOT MODIFY

import json
from main import app

BUILD_VER = '4ffef8c358742a3d01eaba9b07d50679eba8a816'

@app.route('/build_info')
def buildInfo():
    return json.dumps({
        "ver": BUILD_VER
    })

