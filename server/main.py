from flask import Flask, send_file, abort, jsonify
import os

app = Flask(__name__)


@app.route('/id/dataset/<id>')
def dataset_handler(id):
    file_path = os.path.join('data', f'{id}.json')

    if not os.path.exists(file_path):
        abort(404)

    return send_file(file_path, mimetype='application/ld+json')


@app.route('/id/index/datasets')
def dataset_index():
    base_url = "http://127.0.0.1:8080"
    data_dir = 'data'
    
    # Create data directory if it doesn't exist
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)
        
    datasets = []
    
    # List all json files in the data directory
    for filename in os.listdir(data_dir):
        if filename.endswith('.json'):
            # Extract id from filename (remove .json extension)
            dataset_id = os.path.splitext(filename)[0]
            # Create URL for this dataset
            dataset_url = f"{base_url}/id/dataset/{dataset_id}"
            datasets.append(dataset_url)
    
    return jsonify(datasets)


if __name__ == '__main__':
    print("Server listening on port 8080")
    app.run(host='0.0.0.0', port=8080)
