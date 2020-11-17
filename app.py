import json

from flask import Flask, request, abort, jsonify

import Main
from config import SPACE
from logger import logger

app = Flask(__name__)
log = logger.get_logger('server')


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/api', methods=['POST'])
def api():
    if not request.json:
        log.warn('Bad json request. Client IP: {0} '.format(request.remote_addr))
        abort(400)

    task = {
        'id':  json.loads(request.json['index']),
        'x':  json.loads(request.json['x']),
        'y':  json.loads(request.json['y']),
        'list_h': json.loads(request.json['list_h'])
    }

    log.info('Start solution task: {}'.format(task['id']))
    answer = Main.start_solution(task)
    log.info('Complete solution task: {}'.format(task['id']))

    return jsonify({'answer': answer}), 201


if __name__ == '__main__':
    if SPACE == 'dev':
        app.run(host='0.0.0.0', debug=True)
    else:
        from waitress import serve

        serve(app, host="0.0.0.0", port=5000)
