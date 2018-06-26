import json

import requests
from flask import request
from flask_api import FlaskAPI, status

app = FlaskAPI(__name__)

STATUS_ERROR = 'error'
STATUS_FAILURE = 'failure'
STATUS_PENDING = 'pending'
STATUS_SUCCESS = 'success'
BASE_GITHUB_URL = 'https://api.github.com/'


@app.route("/", methods=['GET', 'POST'])
def root_list():
    return []


@app.route("/prcomment", methods=['POST'])
def pull_request_comment():
    owner = request.data.get('pull_request', {}).get('repo', {}).get('owner', {}).get('login', '')
    repo = request.data.get('pull_request', {}).get('repo', {}).get('name', '')
    sha = request.data.get('comment', {}).get('commit_id', '')
    set_status(owner, repo, sha, STATUS_PENDING, "Checking dependencies...")
    return {}, status.HTTP_201_CREATED


def set_status(owner, repo, sha, commit_status, description=None):
    url = '{}repos/{}/{}/statuses/{}'.format(
        BASE_GITHUB_URL,
        owner,
        repo,
        sha
    )

    payload = {
        "state": commit_status,
        "target_url": "foo",
        "description": description,
        "context": "continuous-integration/merge-watcher"
    }

    requests.request('POST', url, data=json.dumps(payload))


if __name__ == "__main__":
    app.run(debug=True)
