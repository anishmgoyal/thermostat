## GENERATED FILE, DO NOT MODIFY

import json
from main import app

BUILD_VER = '2209770d8347e622a592b55401563726915f210e'

@app.route('/build_info')
def buildInfo():
    return json.dumps({
        "ver": BUILD_VER
    })

