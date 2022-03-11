## GENERATED FILE, DO NOT MODIFY

import json
from main import app

BUILD_VER = 'de5e0cf84b61af54fec98df8c299bf4199b3494f'

@app.route('/build_info')
def buildInfo():
    return json.dumps({
        "ver": BUILD_VER
    })

