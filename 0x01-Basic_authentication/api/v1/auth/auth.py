#!/usr/bin/env python3
""" script to manage api authentication """

from flask import request
from typing import List, TypeVar


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
        return True

    def authorization_header(self, request=None) -> str:
        """documentation needed"""
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """documentation needed"""
        return None
