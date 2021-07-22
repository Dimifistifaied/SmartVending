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
@auth.login_required
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
@auth.login_required
def bulk():
    language = 'BG'
    value = {
        "language": language,
    }
    return json.dumps(value)



if __name__ == "__main__":
	app.run(host="10.228.136.41", port=5000, threaded=True, debug=True)
    
