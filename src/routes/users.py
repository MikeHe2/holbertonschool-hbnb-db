"""
This module contains the routes for the users endpoints.
"""

from flask import Blueprint, app
from src.controllers.users import (
    create_user,
    delete_user,
    get_user_by_id,
    get_users,
    protected,
    update_user,
    login
)

users_bp = Blueprint("users", __name__, url_prefix="/users")
auth_bp = Blueprint("auth", __name__)

users_bp.route("/", methods=["GET"])(get_users)
users_bp.route("/", methods=["POST"])(create_user)

users_bp.route("/<user_id>", methods=["GET"])(get_user_by_id)
users_bp.route("/<user_id>", methods=["PUT"])(update_user)
users_bp.route("/<user_id>", methods=["DELETE"])(delete_user)

auth_bp.route("/login", methods=['POST'])(login)
auth_bp.route("/protected", methods=['GET'])(protected)
