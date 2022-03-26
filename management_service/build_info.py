## GENERATED FILE, DO NOT MODIFY

import json
from main import app

BUILD_VER = 'b0a11ccd9ce4da93d1801f50916138a6afa286bb'

@app.route('/build_info')
def buildInfo():
    return json.dumps({
        "ver": BUILD_VER
    })

