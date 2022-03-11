import os
import re
import git_info
import requests
from flask import Flask


def getGitOrgAndRepo():
    git_origin_pattern = r"(.*)/(.*)(.git)?$"
    matches = re.search(git_origin_pattern, git_info.GIT_ORIGIN)
    return matches.group(1), matches.group(2)


app = Flask(__name__)


@app.route("/check_head")
def checkHead():
    org, repo = getGitOrgAndRepo()
    git_api = 'https://api.github.com/repos/{}/{}/branches/main'.format(
        org, repo)

    head_info = requests.get(git_api).json()
    return head_info['commit']['sha']


@app.route("/update", methods=["POST"])
def update():
    os.system('/var/lib/thermostat/updates/download_update.sh')
    pass
