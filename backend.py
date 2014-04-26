from flask import Flask, request, jsonify, render_template
import json
app = Flask(__name__)

@app.route('/')
def main_site():
        return render_template('index.html')

@app.route('/api/node', methods=['POST'])
def print_data():
    if request.method == 'POST':
        node = request.form.to_dict();
        print(node)
        node['status'] = 'success'
        node['token'] = '1234567abcdef'
        print(json.dumps(node))
    return jsonify(node)

if __name__ ==  "__main__":
    app.run(debug=True)
