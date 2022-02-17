from flask import Flask, render_template
#import pathlib
#import os

app = Flask(__name__, template_folder='templates')
#app_dir = pathlib.Path(__file__).parent.resolve()

@app.route('/index')
def index():
    return render_template('index.html')

if __name__ == "__main__":
    app.run()