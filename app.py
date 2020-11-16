import json

from flask import Flask, request, abort, jsonify

import Main

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/api', methods=['POST'])
def api():
    if not request.json:
        abort(400)
    task = {
        'id':  json.loads(request.json['index']),
        'x':  json.loads(request.json['x']),
        'y':  json.loads(request.json['y']),
        'list_h': json.loads(request.json['list_h'])
    }

    answer = Main.start_solution(task)

    return jsonify({'answer': answer}), 201


if __name__ == '__main__':
    app.run(host='0.0.0.0')
