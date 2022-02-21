from distutils.log import debug
from flask import Flask, render_template, jsonify, request
from flask_jwt_extended import JWTManager, jwt_required, create_access_token
import base64
import hashlib
#import pathlib
#import os

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

class CustomException(Exception):
    def __init__(self, message):
        self.message = message


if __name__ == "__main__":
    app.run(debug=True)