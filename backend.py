from flask import Flask, request, jsonify, render_template, abort
import json
from helper import InputParser, Token
import db as database

app = Flask(__name__)
parser = InputParser()
tokgen = Token()
db = database.DB()

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
            resp = parser.getData(request)
            resp['token'] = tokgen.getToken()
            db.addNode(resp)
            resp['status'] = 'success'
            return jsonify(**resp)
    else:
        abort(400)

if __name__ ==  "__main__":
    app.run(debug=True)
