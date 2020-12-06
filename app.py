import json

from flask import Flask, request, abort, jsonify

import Main
import config

app = Flask(__name__)


@app.route('/api', methods=['POST'])
def api():
    if not request.json:
        abort(400)
    task = {
        'id':  json.loads(request.json['index']),
        'x':  json.loads(request.json['x']),
        'y':  json.loads(request.json['y']),
        'freeChlen': request.json['freeChlen'],
        'list_h': json.loads(request.json['list_h'])
    }

    answer = Main.start_solution(task)

    return jsonify({'id': task['id'], 'answer': answer}), 201


if __name__ == '__main__':
    if config.SPACE == 'dev':
        app.run(host='0.0.0.0')
    else:
        from waitress import serve
        serve(app, host="0.0.0.0", port=5000)
