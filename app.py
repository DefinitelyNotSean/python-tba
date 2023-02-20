from flask import Flask, request, jsonify
import jwt

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key'

# Mock user database for example purposes
users = {
    'user1': 'password1',
    'user2': 'password2'
}

# Login route for generating access tokens
@app.route('/login', methods=['POST'])
def login():
    username = request.json.get('username')
    password = request.json.get('password')
    if username not in users or password != users[username]:
        return jsonify({'error': 'Invalid username or password'}), 401
    token = jwt.encode({'username': username}, app.config['SECRET_KEY'], algorithm='HS256')
    return jsonify({'token': token.decode('utf-8')})

# Protected route that requires a valid access token
@app.route('/protected', methods=['GET'])
def protected():
    token = request.headers.get('Authorization').split()[1]
    try:
        data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
        return jsonify({'message': f'Hello {data["username"]}!'})
    except jwt.ExpiredSignatureError:
        return jsonify({'error': 'Token has expired'}), 401
    except jwt.InvalidTokenError:
        return jsonify({'error': 'Invalid token'}), 401

if __name__ == '__main__':
    app.run()
