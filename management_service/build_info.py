## GENERATED FILE, DO NOT MODIFY

import json
from main import app

BUILD_VER = 'c45e15d556448411ce9db45fdd34f239bb0c0d87'

@app.route('/build_info')
def buildInfo():
    return json.dumps({
        "ver": BUILD_VER
    })

