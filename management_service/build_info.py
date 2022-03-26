## GENERATED FILE, DO NOT MODIFY

import json
from main import app

BUILD_VER = '4ca379659a85e3d6777efa3f154255ad46c91fdc'

@app.route('/build_info')
def buildInfo():
    return json.dumps({
        "ver": BUILD_VER
    })

