from flask import Flask, send_file, abort
import os

app = Flask(__name__)


@app.route('/api/datasets/<id>')
def dataset_handler(id):
    file_path = os.path.join('data', f'{id}.json')

    if not os.path.exists(file_path):
        abort(404)

    return send_file(file_path, mimetype='application/ld+json')


if __name__ == '__main__':
    print("Server listening on port 8080")
    app.run(host='0.0.0.0', port=8080)

