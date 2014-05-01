from flask import Flask, request, jsonify, render_template, abort
import json
from helper import InputParser

app = Flask(__name__)
parser = InputParser()

@app.route('/')
def main_site():
        return render_template('index.html')

@app.route('/api/node', methods=['POST'])
def process_data():
    if request.method == 'POST':
        vres = parser.validate(request)
        if vres:
            resp = jsonify(**vres)
            resp.status_code = 400
            return resp
    else:
        abort(400)

if __name__ ==  "__main__":
    app.run(debug=True)
