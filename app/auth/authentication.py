import jwt
from datetime import datetime, timedelta
from flask import request, jsonify
from functools import wraps
from werkzeug.security import check_password_hash

SECRET_KEY = "your_secret_key"


def encode_auth_token(user_id, role):
    """
    Generates the Auth Token
    :param user_id: ID of the user
    :param role: Role of the user

    :return: string
    """
    try:
        payload = {
            'exp': datetime.utcnow() + timedelta(days=1),
            'iat': datetime.utcnow(),
            'sub': user_id,
            'role': role  # Include role in the payload


        }
        return jwt.encode(payload, SECRET_KEY, algorithm='HS256')
    except Exception as e:
        return e


def decode_auth_token(auth_token):
    """
    Decodes the Auth Token
    :param auth_token: JWT token
    :return: integer or string
    """
    try:
        payload = jwt.decode(auth_token, SECRET_KEY, algorithms=['HS256'])
        return payload  # Return the entire payload, which includes 'sub' (user_id) and 'role'
    except jwt.ExpiredSignatureError:
        return 'Token expired. Please log in again.'
    except jwt.InvalidTokenError:
        return 'Invalid token. Please log in again.'

def token_required(f):
    """
    Decorator to check for valid token in the request headers
    :param f: function
    :return: response
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = None
        if 'Authorization' in request.headers:
            token = request.headers['Authorization']
        if not token:
            return jsonify({'message': 'Token is missing!'}), 403
        try:
            decoded_data = decode_auth_token(token)
            if isinstance(decoded_data, str):  # If an error message was returned
                return jsonify({'message': decoded_data}), 403
            user_id = decoded_data['user_id']
            role = decoded_data['role']
        except:
            return jsonify({'message': 'Token is invalid!'}), 403
        # Pass user_id and role to the wrapped function
        return f(user_id, role, *args, **kwargs)
    return decorated_function
