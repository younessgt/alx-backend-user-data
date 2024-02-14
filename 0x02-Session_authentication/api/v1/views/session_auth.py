#!/usr/bin/env python3
"""module of session views"""

from api.v1.views import app_views
from flask import abort, request, jsonify
from models.user import User
from os import getenv


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def session_login():
    """doc doc doc"""

    email = request.form.get("email")
    password = request.form.get("password")
    if not email or email == "":
        return jsonify({"error": "email missing"}), 400
    if not password or password == "":
        return jsonify({"error": "password missing"}), 400

    try:
        users = User.search({"email": email})
        if not users:
            return jsonify({"error": "no user found for this email"}), 404
    except Exception:
        return jsonify({"error": "no user found for this email"}), 404

    for user in users:
        if user.is_valid_password(password):
            from api.v1.app import auth
            user = users[0]
            new_session_id = auth.create_session(user.id)
            res = jsonify(user.to_json())
            session_name = getenv("SESSION_NAME")
            res.set_cookie(session_name, new_session_id)
            return res
    return jsonify({"error": "wrong password"}), 401


@app_views.route('/auth_session/logout',
                 methods=['DELETE'],
                 strict_slashes=False)
def session_logout():
    """DOC DOC DOC"""

    from api.v1.app import auth
    resp = auth.destroy_session(request)
    if resp:
        return jsonify({}), 200
    abort(404)
