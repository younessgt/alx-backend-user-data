#!/usr/bin/env python3
""" script to manage api authentication """

from flask import request
from typing import List, TypeVar
from fnmatch import fnmatch
from os import getenv


class Auth:
    """class for managing Api authentication """

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """documentation needed"""
        if path is None or not excluded_paths:
            return True
        if not path.endswith("/"):
            path += "/"
        if path in excluded_paths:
            return False
        for p in excluded_paths:
            if fnmatch(path, p):
                return False
        return True

    def authorization_header(self, request=None) -> str:
        """documentation needed"""
        if request is None:
            return None
        return request.headers.get("Authorization", None)

    def current_user(self, request=None) -> TypeVar('User'):
        """documentation needed"""
        return None

    def session_cookie(self, request=None):
        """ method that return a cookie value from a rquest"""

        if request is None:
            return None
        session_name = getenv("SESSION_NAME")
        value = request.cookies.get(session_name)
        return value
