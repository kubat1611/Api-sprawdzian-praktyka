from flask import Flask, jsonify, request

app = Flask(__name__)

users = [
    {"id": 1, "name": "Wojciech", "lastname": "Oczkowski"},
    {"id": 2, "name": "Mateusz", "lastname": "Kozlowski"},
]


def get_user_by_id(user_id):
    for user in users:
        if user['id'] == user_id:
            return user
    return None


@app.route('/')
def start():
    return 'Welcome to my API!'


@app.route('/users', methods=['GET'])
def get_users():
    return jsonify(users), 200


@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = get_user_by_id(user_id)
    if user:
        return jsonify(user), 200
    else:
        return jsonify({'error': 'User not found'}), 404


@app.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    if 'name' not in data or 'lastname' not in data:
        return jsonify({'error': 'Name and lastname are required'}), 400

    new_user = {
        'id': len(users) + 1,
        'name': data['name'],
        'lastname': data['lastname']
    }
    users.append(new_user)

    return jsonify({'id': new_user['id']}), 201


@app.route('/users/<int:user_id>', methods=['PATCH'])
def update_user(user_id):
    user = get_user_by_id(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404

    data = request.get_json()
    if not data or not any(key in data for key in ['name', 'lastname']):
        return jsonify({'error': 'Invalid request body'}), 400

    if 'name' in data:
        user['name'] = data['name']
    if 'lastname' in data:
        user['lastname'] = data['lastname']

    return jsonify({}), 204


@app.route('/users/<int:user_id>', methods=['PUT'])
def create_or_update_user(user_id):
    user = get_user_by_id(user_id)

    data = request.get_json()
    if 'name' not in data or 'lastname' not in data:
        return jsonify({'error': 'Name and lastname are required'}), 400

    if user:
        user['name'] = data['name']
        user['lastname'] = data['lastname']
    else:
        new_user = {
            'id': user_id,
            'name': data['name'],
            'lastname': data['lastname']
        }
        users.append(new_user)

    return jsonify({}), 204


@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = get_user_by_id(user_id)
    if user:
        users.remove(user)
        return jsonify({}), 204
    else:
        return jsonify({'error': 'User not found'}), 404


if __name__ == '__main__':
    app.run(debug=True)
