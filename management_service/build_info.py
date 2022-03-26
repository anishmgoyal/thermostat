## GENERATED FILE, DO NOT MODIFY

import json
from main import app

BUILD_VER = '532f1912689be032409515365d264a6d78f4cd58'

@app.route('/build_info')
def buildInfo():
    return json.dumps({
        "ver": BUILD_VER
    })

