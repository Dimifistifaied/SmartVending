import uuid,json
from flask import *
from collections import deque
from Infrastructure import Runnable as rn
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__, static_folder='', static_url_path='')
app.userDict = {}

auth = HTTPBasicAuth()

users = {
    "SystemTVDummy": generate_password_hash("hello"),
}

@auth.verify_password
def verify_password(username, password):
    if username in users and \
            check_password_hash(users.get(username), password):
        return username

@app.route('/')
#@auth.login_required
def index():
    return "Hello, {}!".format(auth.current_user())	


@app.route('/generateUUID')
def generate_uuid():
    uniqueID = str(uuid.uuid1())
    app.userDict.update({uniqueID: deque()})
    return uniqueID


@app.route('/exec', methods=['POST'])
def exec_pycode():
    if not request.json or 'text' not in request.json:
        abort(400)
    else:
        return str(rn.createFile(request.json['text']))


@app.route('/save', methods=['POST'])
def save():
    for item in app.userDict.items():
        if item[0] != request.json['user']:
            item[1].append(request.json['text'])
    return 'OK'


@app.route('/stream/<UUID>', methods=['GET'])
def stream(UUID):
    def eventstream(UUID):
        while True:
            if len(app.userDict.get(UUID)) > 0:
                dataJSON = json.dumps({"text": app.userDict.get(UUID).popleft()})
                yield "event: ping\ndata:{}\n\n".format(dataJSON)
    return Response(eventstream(UUID), mimetype="text/event-stream")


@app.route('/vend', methods=['GET'])
def bulk():
    language = 'BG'
    value = {
        "language": language,
    }
    return json.dumps(value)


@app.route('/userDelete', methods=['GET'])
def user_delete():
    correlationId = 'User Deleted: ASQ00*'
    value = {
        "correlationId": correlationId,
        "createdOn": "2021-01-31T17:33:27.902+01:00"
    }
    return json.dumps(value)


@app.route('/userCreateUpdate', methods=['GET'])
def user_create_update():
    correlationId = 'User Created: ASQ00*'
    value = {
        "correlationId": correlationId,
        "createdOn": "2021-01-31T17:33:27.902+01:00"
    }
    return json.dumps(value)


@app.route('/clusterCreateUpdate', methods=['GET'])
def cluster_create_update():
    correlationId = 'Cluster Created: Great!'
    value = {
        "correlationId": correlationId,
        "createdOn": "2021-01-31T17:33:27.902+01:00"
    }
    return json.dumps(value)


@app.route('/clusterDelete', methods=['GET'])
def cluster_delete():
    correlationId = 'Cluster Deleted: Great!'
    value = {
        "correlationId": correlationId,
        "createdOn": "2021-01-31T17:33:27.902+01:00"
    }
    return json.dumps(value)


@app.route('/planogram', methods=['GET'])
def planograms():
    correlationId = 'Planogram sent: Great!'
    value = {
        "correlationId": correlationId,
        "createdOn": "2021-01-31T17:33:27.902+01:00"
    }
    return json.dumps(value)


@app.route('/machineCreateUpdate', methods=['GET'])
def machine_create_update():
    correlationId = 'Machine created: Great!'
    value = {
        "correlationId": correlationId,
        "createdOn": "2021-01-31T17:33:27.902+01:00"
    }
    return json.dumps(value)


@app.route('/machineDelete', methods=['GET'])
def machine_delete():
    correlationId = 'Machine deleted: Great!'
    value = {
        "correlationId": correlationId,
        "createdOn": "2021-01-31T17:33:27.902+01:00"
    }
    return json.dumps(value)


@app.route('/componentDelete', methods=['GET'])
def component_delete():
    correlationId = 'Component deleted: Great!'
    value = {
        "correlationId": correlationId,
        "createdOn": "2021-01-31T17:33:27.902+01:00"
    }
    return json.dumps(value)


@app.route('/componentCreateUpdate', methods=['GET'])
def component_create_update():
    correlationId = 'Component created: Great!'
    value = {
        "correlationId": correlationId,
        "createdOn": "2021-01-31T17:33:27.902+01:00"
    }
    return json.dumps(value)


@app.route('/productCreateUpdate', methods=['GET'])
def product_create_update():
    correlationId = 'Product created: Great!'
    value = {
        "correlationId": correlationId,
        "createdOn": "2021-01-31T17:33:27.902+01:00"
    }
    return json.dumps(value)


@app.route('/productDelete', methods=['GET'])
def product_deleted():
    correlationId = 'Product deleted: Great!'
    value = {
        "correlationId": correlationId,
        "createdOn": "2021-01-31T17:33:27.902+01:00"
    }
    return json.dumps(value)


@app.route('/saveVisitPlans', methods=['POST'])
def save_visit_plans():
    return request.data

if __name__ == "__main__":
    app.run(host="10.228.136.41", port=5000, threaded=True, debug=True)
