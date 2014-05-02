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
    val = parser.getData(request)
    vres = parser.validate(parser.getNodeRegex(), val)
    if vres:
        resp = jsonify(**vres)
        resp.status_code = 400
        return resp
    # check for duplicates
    ddres = dedup.checkDups(val['hostname'], val['mac'], val['key'])
    if ddres:
        resp = jsonify(**ddres)
        resp.status_code = 409
        return resp
    # if we reach this part the data should be correct
    resp = val
    resp['token'] = token.getToken()
    db.addNode(resp)
    resp['status'] = 'success'
    return jsonify(**resp)

@app.route('/api/node/<tok>', methods=['GET'])
def process_get(tok):
    vres = parser.validate(parser.getTokenRegex(), {'token': tok})
    if vres:
        resp = jsonify(**vres)
        resp.status_code = 400
        return resp
    tres = token.checkToken(tok)
    if tres:
        resp = jsonify(**tres)
        resp.status_code = 404
        return resp
    return jsonify(**db.getNode(tok))

if __name__ ==  "__main__":
    app.run(debug=True)
