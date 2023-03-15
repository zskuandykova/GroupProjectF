from flask import Flask, request
from cryptography.fernet import Fernet
from base64 import b64decode
import pickle
import json
import xml.etree.ElementTree as ET

app = Flask(__name__)

@app.route('/upload', methods=['POST'])
def upload_file():
    data = request.get_json()
    serialized_data = b64decode(data.get('file_content'))
    key = data.get('key')

    if not serialized_data:
        return "File content is missing", 400

    if key:
        f = Fernet(key.encode())
        serialized_data = f.decrypt(serialized_data)

    format = data.get('format')
    if format == 'binary':
        data = pickle.loads(serialized_data)
    elif format == 'json':
        data = json.loads(serialized_data.decode())
    elif format == 'xml':
        root = ET.fromstring(serialized_data)
        data = {}
        for child in root:
            data[child.tag] = child.text
    else:
        data = None

    if data:
        # TODO: optionally write to file
        print(data)

    return "File uploaded successfully"

if __name__ == '__main__':
    app.run(debug=True, port=1234)