## GENERATED FILE, DO NOT MODIFY

import json
from main import app

BUILD_VER = '11606050f5aa02cf205c1260731ed018903e0c9f'

@app.route('/build_info')
def buildInfo():
    return json.dumps({
        "ver": BUILD_VER
    })

