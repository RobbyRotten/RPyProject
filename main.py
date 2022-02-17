from flask import Flask, render_template, jsonify, request
#import pathlib
#import os

app = Flask(__name__, template_folder='templates')
#app_dir = pathlib.Path(__file__).parent.resolve()

@app.route('/index', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
    success = True
    error = ''
    data = {}
    try:
        info = request.json
        data = str(info)
    except BaseException as e:
        success = False
        error = str(e)        
    finally:
        return jsonify({'Success': success, 'Error': error, 'Response': data})

if __name__ == "__main__":
    app.run()