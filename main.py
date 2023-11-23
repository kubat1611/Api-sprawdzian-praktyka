from flask import Flask, jsonify, request

app = Flask(__name__)

users = [
    {"id": 1, "name": "Wojciech", "lastname": "Oczkowski"},
    {"id": 2, "name": "Mateusz", "lastname": "Kozlowski"},
]



@app.route('/')
def start():
    return 'Welcome to my API!'


@app.route('/users', methods=['GET'])
def get_users():
    return jsonify(users), 200


@app.route('/users/<int:id>', methods=['GET'])
def get_user_of_id(id):
    if id not in [user['id'] for user in users]:
        return jsonify({"message": "User not found"}), 404
    user = [user for user in users if user['id'] == id]
    return jsonify(user), 200


@app.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()

    if not data or 'name' not in data or 'lastname' not in data:
        return jsonify({"error": "Invalid request format"}), 400

    new_user = {
        "id": len(users) + 1,
        "name": data['name'],
        "lastname": data['lastname']
    }

    users.append(new_user)

    return jsonify(new_user), 201


if __name__ == '__main__':
    app.run(debug=True)
