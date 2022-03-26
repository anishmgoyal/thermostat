## GENERATED FILE, DO NOT MODIFY

import json
from main import app

BUILD_VER = '0dcc3dffb25425984f2a35cda026dc467a74d020'

@app.route('/build_info')
def buildInfo():
    return json.dumps({
        "ver": BUILD_VER
    })

