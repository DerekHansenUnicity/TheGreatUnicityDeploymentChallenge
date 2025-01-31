from os import environ
from flask import Flask, jsonify, make_response, request, abort
from flask_cors import CORS
import boto3

app = Flask(__name__)
CORS(app)

# endpoint_url = "http://s3.localhost.localstack.cloud:4566"
endpoint_url = "http://host.docker.internal:4566"

AWS_ACCESS_KEY = environ.get('AWS_ACCESS_KEY') or 'fake-aws-access-key'
AWS_SECRET_ACCESS_KEY = environ.get('AWS_SECRET_ACCESS_KEY') or 'fake-aws-secret-access-key'
BUCKET_NAME = environ.get('S3_BUCKET_NAME') or 'fake-bucket'

s3 = boto3.client('s3', aws_access_key_id=AWS_ACCESS_KEY, aws_secret_access_key=AWS_SECRET_ACCESS_KEY, endpoint_url=endpoint_url)

def upload_to_s3(file):
    try:
        response = s3.upload_fileobj(file, Bucket=BUCKET_NAME, Key=file.filename)
        return 'http://s3.localhost.localstack.cloud:4566/%s/%s'%(BUCKET_NAME, file.filename)
    except Exception as e:
        print(str(e))
        return ''

inventory = [
    {
        'id': 1,
        'name': 'Spoon',
        'description': 'Standard dining spoon',
        'quantity': 123,
        'image_url': '',
    },
    {
        'id': 2,
        'name': 'Fork',
        'description': 'Standard dining fork',
        'quantity': 456,
        'image_url': '',
    },
    {
        'id': 3,
        'name': 'Knife',
        'description': 'Standard dining knife',
        'quantity': 789,
        'image_url': '',
    },
]

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not Found', 'message': error.description}), 404)

@app.route('/healthcheck', methods=['GET'])
def get_healthcheck():
    return jsonify({'status': 'online'})

@app.route('/inventory', methods=['GET'])
@app.route('/inventory/', methods=['GET'])
def get_all_inventory():
    return jsonify(inventory)

@app.route('/inventory', methods=['POST'])
@app.route('/inventory/', methods=['POST'])
def add_item():
    if not request.json:
        abort(400)
    id = int(request.json['id'])
    name = request.json['name']
    description = request.json['description']
    quantity = int(request.json['quantity'])

    item = {
        'id': id,
        'name': name,
        'description': description,
        'quantity': quantity,
        'image_url': '',
        }
    for search_item in inventory[:]:
        if search_item['id'] == id:
            inventory.remove(search_item)
    inventory.append(item)
    return jsonify(item)

@app.route('/inventory/<int:item_id>/image', methods=['POST'])
@app.route('/inventory/<int:item_id>/image/', methods=['POST'])
def post_item_image(item_id):
    found_item = None
    for item in inventory[:]:
        if item['id'] == item_id:
            found_item = item
            inventory.remove(item)

    if found_item is not None:
        file = request.files.get('image_file')
        if file:
            found_item['image_url'] = upload_to_s3(file)
        else:
            inventory.append(found_item)
            return make_response(jsonify({'error': 'No image', 'message': 'No Image File Found'}), 400)
        inventory.append(found_item)
        return jsonify(found_item)
    else:
        inventory.append(found_item)
        return make_response(jsonify({'error': 'Not Found', 'message': 'Item Not Found'}), 404)

@app.route('/inventory/<int:item_id>', methods=['GET'])
def get_item(item_id):
    for item in inventory:
        if item['id'] == item_id:
            return jsonify(item)
    # not found
    return make_response(jsonify({'error': 'Not Found', 'message': 'Item Not Found'}), 404)

@app.route('/inventory/<int:item_id>', methods=['DELETE'])
def delete_item(item_id):
    for item in inventory[:]:
        if item['id'] == item_id:
            inventory.remove(item)
    return jsonify({'status': 'success'})

if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)
