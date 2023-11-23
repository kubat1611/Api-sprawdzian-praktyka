from flask import Flask, jsonify

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


if __name__ == '__main__':
    app.run(debug=True)
