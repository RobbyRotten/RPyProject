from distutils.log import debug
from flask import Flask, render_template, jsonify, request, send_file
from flask_jwt_extended import JWTManager, jwt_required, create_access_token
import base64
import hashlib
from DaemonManager import DaemonManager
#import pathlib
import os
import re

users = {'madmax': 'qwerty'}

app = Flask(__name__, template_folder='templates')
app.config["JWT_SECRET_KEY"] = "GEiovn3891(&34v(FH£G*&grA:FMo3fnalw;"
app.config["JWT_TOKEN_LOCATION"] = ["headers", "query_string"]
jwt = JWTManager(app)
#app_dir = pathlib.Path(__file__).parent.resolve()

@app.route('/index', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
    success = True
    error = ''
    data = ''
    access_token = ''
    try:
        info = request.json     
        pwd = users.get(info['username'])   
        if pwd is None:
            raise CustomException(f"User {info['username']} not found. Access denied.")
        pwd_hash = base64.b64encode(hashlib.sha256(pwd.encode()).digest()).decode('utf-8')
        if pwd_hash != info['password']:
            raise CustomException("Wrong password. Access denied.")
        access_token = create_access_token(identity=info['username'])
        data = 'OK'
    except BaseException as e:
        success = False
        error = str(e)    
    finally:
        return jsonify({'Success': success, 'Error': error, 'Response': data, 'access_token': access_token})
        
@app.route('/main_page', methods=['GET'])
@jwt_required()
def main_page():
    return render_template('main_page.html')

@app.route('/get_image/<filename>', methods=['GET'])
@jwt_required()
def get_image(filename):
    path = os.path.join('daemon', 'images', filename)
    return send_file(path, mimetype='image/jpeg')
        
@app.route('/start_camera', methods=['GET'])
@jwt_required()
def start_camera():
    success = True
    error = ''
    data = 'OK'
    try:
        dm = DaemonManager()
        if not dm.isactive():
            for file in os.listdir(os.path.join('daemon', 'images')):
                if file.startswith('file'):
                    os.remove(os.path.join('daemon', 'images', file))
            dm.start_roll()
    except BaseException as e:
        success = False
        error = str(e)
        data = ''
    finally:
        return jsonify({'Success': success, 'Error': error, 'Response': data})

@app.route('/stop_camera', methods=['GET'])
@jwt_required()
def stop_camera():
    success = True
    error = ''
    data = 'OK'
    try:
        dm = DaemonManager()
        if dm.isactive():
            dm.stop_roll()
    except BaseException as e:
        success = False
        error = str(e)
        data = ''
    finally:
        return jsonify({'Success': success, 'Error': error, 'Response': data})    

@app.route('/is_next_file/<filename>', methods=['GET'])
def is_next_file(filename):
    success = True
    error = ''
    data = True
    try:
        path = os.path.join('daemon', 'images', filename)
        if not os.path.isfile(path):
            data = False
    except BaseException as e:
        success = False
        error = str(e)
        data = ''
    finally:
        return jsonify({'Success': success, 'Error': error, 'Response': data})    

@app.route('/get_last_file', methods=['GET'])
def get_last_file():
    success = True
    error = ''
    data = True
    try:
        files = os.listdir(os.path.join('daemon', 'images'))
        numbers = list(map(lambda x: re.findall(r'\d', x), files))
        max_elem = max(numbers)
        if len(max_elem) == 0:
            max_num = 0
        else:
            max_num = max_elem[0]
        data = max_num
    except BaseException as e:
        success = False
        error = str(e)
        data = ''
    finally:
        return jsonify({'Success': success, 'Error': error, 'Response': data})    

class CustomException(Exception):
    def __init__(self, message):
        self.message = message


if __name__ == "__main__":
    app.run(debug=True)