import os
import re
import git_info
import json
import logging
import requests
from flask import Flask

app = Flask(__name__)
logging.basicConfig(
    filename='record.log',
    level=logging.WARN,
    format=f'%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')


def getGitOrgAndRepo():
    git_origin_pattern = r"(:|/)([^/:]*)/([^:/]*?)(\.git)?$"
    matches = re.search(git_origin_pattern, git_info.GIT_ORIGIN)
    return matches.group(2), matches.group(3)

@app.route("/head")
def checkHead():
    org, repo = getGitOrgAndRepo()
    git_api = 'https://api.github.com/repos/{}/{}/branches/main'.format(
        org, repo)

    app.logger.info('git api url: {}'.format(git_api))
    head_info = requests.get(git_api).json()
    app.logger.debug('head info: {}'.format(head_info))
    
    info = {
        'current_head': head_info['commit']['sha']
    }
    return json.dumps(info)

@app.route("/update", methods=["POST"])
def update():
    try:
        os.system('/var/lib/thermostat/updates/download_update.sh')
    except:
        app.logger.exception("Failed to download update")
        return json.dumps({"status": "error"})
    return json.dumps({"status": "ok"})
