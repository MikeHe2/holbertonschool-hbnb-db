"""
Users controller module
"""

from sys import audit
import bcrypt
from flask import abort, jsonify, request
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required
from src.models.user import User
from src import bcrypt


def get_users():
    """Returns all users"""
    users: list[User] = User.get_all()

    return [user.to_dict() for user in users]


def create_user():
    """Creates a new user"""
    data = request.get_json()

    try:
        user = User.create(data)
    except KeyError as e:
        abort(400, f"Missing field: {e}")
    except ValueError as e:
        abort(400, str(e))

    if user is None:
        abort(400, "User already exists")

    return user.to_dict(), 201


def get_user_by_id(user_id: str):
    """Returns a user by ID"""
    user: User | None = User.get(user_id)

    if not user:
        abort(404, f"User with ID {user_id} not found")

    return user.to_dict(), 200


def update_user(user_id: str):
    """Updates a user by ID"""
    data = request.get_json()

    try:
        user = User.update(user_id, data)
    except ValueError as e:
        abort(400, str(e))

    if user is None:
        abort(404, f"User with ID {user_id} not found")

    return user.to_dict(), 200


def delete_user(user_id: str):
    """Deletes a user by ID"""
    if not User.delete(user_id):
        abort(404, f"User with ID {user_id} not found")

    return "", 204

def login():
    email = request.json.get('email', None)
    password_hash = request.json.get('password', None)
    user = User.query.filter_by(email=email).first()
    if user and bcrypt.check_password_hash(user.password_hash, password_hash):
        additional_claims = {"is_admin": user.is_admin}
        access_token = create_access_token(identity=email, additional_claims=additional_claims)
        return jsonify(access_token=access_token), 200
    return 'Wrong username or password', 401

@jwt_required()
def protected():
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user), 200