#!/usr/bin/env python3
"""
Route module for the API
"""
from os import getenv
from api.v1.views import app_views
from flask import Flask, jsonify, abort, request
from flask_cors import CORS
from os import getenv


app = Flask(__name__)
app.register_blueprint(app_views)
CORS(app, resources={r"/api/v1/*": {"origins": "*"}})
auth = None

AUTH = getenv("AUTH_TYPE")
if AUTH == "auth":
    from api.v1.auth.auth import Auth
    auth = Auth()
if AUTH == "basic_auth":
    from api.v1.auth.basic_auth import BasicAuth
    auth = BasicAuth()
if AUTH == "session_auth":
    from api.v1.auth.session_auth import SessionAuth
    auth = SessionAuth()
if AUTH == "session_exp_auth":
    from api.v1.auth.session_exp_auth import SessionExpAuth
    auth = SessionExpAuth()


@app.errorhandler(404)
def not_found(error) -> str:
    """ Not found handler
    """
    return jsonify({"error": "Not found"}), 404


@app.errorhandler(401)
def unauthorized(error) -> str:
    """ unauthorized request"""
    return jsonify({"error": "Unauthorized"}), 401


@app.errorhandler(403)
def no_access_allowed(error) -> str:
    """ not allowed to access request"""
    return jsonify({"error": "Forbidden"}), 403


@app.before_request
def filter_request():
    """ filtering requests"""
    paths = ['/api/v1/status/', '/api/v1/unauthorized/',
             '/api/v1/forbidden/', '/api/v1/auth_session/login/']

    if auth is None:
        return
    if not auth.require_auth(request.path, paths):
        return
    if (
        auth.authorization_header(request) is None and
        auth.session_cookie(request) is None
       ):
        return abort(401)

    # it better to use g variable from flask to store somthing like
    # current_user  g.current_user  instead of request.current_user
    request.current_user = auth.current_user(request)
    if request.current_user is None:
        return abort(403)


if __name__ == "__main__":
    host = getenv("API_HOST", "0.0.0.0")
    port = getenv("API_PORT", "5000")
    app.run(host=host, port=port)
