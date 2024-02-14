#!/usr/bin/env python3
"""module of session views"""

from api.v1.views import app_views
from flask import request, jsonify
from models.user import User
from os import getenv


@app_views.route('/auth_session/login', method=['POST'], strict_slashes=False)
def session():
    """doc doc doc"""

    email = request.form.get("email")
    password = request.form.get("password")
    if not email or email == "":
        return jsonify({"error": "email missing"}), 400
    if not password or password == "":
        return jsonify({"error": "password missing"}), 400

    try:
        users = User.search({"email": email})
    except Exception:
        return jsonify({"error": "no user found for this email"}), 404

    for user in users:
        if not user.is_valid_password(password):
            return jsonify({"error": "wrong password"}), 401

    from api.v1.app import auth
    user = users[0]
    new_session_id = auth.create_session(user.id)
    res = jsonify(user.to_json())
    res.set_cookie(getenv("SESSION_NAME", new_session_id))
    return res
