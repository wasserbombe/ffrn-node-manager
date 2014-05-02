from flask import Flask, request, jsonify, render_template, abort
import json
from helper import InputParser, Token, Dedup
import db as database

app = Flask(__name__)
parser = InputParser()
token = Token()
db = database.DB()
dedup = Dedup()

@app.route('/')
def main_site():
        return render_template('index.html')

@app.route('/api/node', methods=['POST'])
def process_new():
    # check for invalid data
    vres = parser.validate(request, parser.getNodeRegex())
    if vres:
        resp = jsonify(**vres)
        resp.status_code = 400
        return resp
    val = parser.getData(request)
    # check for duplicates
    ddres = dedup.checkDups(val['hostname'], val['mac'], val['key'])
    if ddres:
        resp = jsonify(**ddres)
        resp.status_code = 409
        return resp
    # if we reach this part the data should be correct
    resp = parser.getData(request)
    resp['token'] = token.getToken()
    db.addNode(resp)
    resp['status'] = 'success'
    return jsonify(**resp)

if __name__ ==  "__main__":
    app.run(debug=True)
