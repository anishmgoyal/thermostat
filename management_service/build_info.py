## GENERATED FILE, DO NOT MODIFY

import json
from main import app

BUILD_VER = 'ab8763c67dd450c43f01b4b9bf2f58fabf0005f6'

@app.route('/build_info')
def buildInfo():
    return json.dumps({
        "ver": BUILD_VER
    })

