from flask import Flask, request, jsonify, send_file
from google.cloud import storage
import os
from io import BytesIO


os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "C:/Users/onaye/Downloads/psyched-bonfire-436413-e2-c91735889269.json"

app = Flask(__name__)


storage_client = storage.Client()
bucket_name = 'app-alua-bucket'
bucket = storage_client.bucket(bucket_name)


@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    
    blob = bucket.blob(file.filename)
    
    # Google Storage upload
    blob.upload_from_file(file)
    
    return jsonify({"message": f"File '{file.filename}' uploaded successfully!"})


@app.route('/download/<filename>', methods=['GET'])
def download_file(filename):
    blob = bucket.blob(filename)
    
    if not blob.exists():
        return jsonify({"error": f"File '{filename}' does not exist!"}), 404

    file_data = blob.download_as_bytes()
    
    return send_file(BytesIO(file_data), as_attachment=True, download_name=filename)


@app.route('/files', methods=['GET'])
def list_files():
    blobs = bucket.list_blobs()
    
    file_list = [blob.name for blob in blobs]
    
    return jsonify({"files": file_list})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)


