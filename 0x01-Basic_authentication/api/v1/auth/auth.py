#!/usr/bin/env python3
""" script to manage api authentication """

from flask import request
from typing import List, TypeVar


class Auth:
    """class for managing Api authentication """

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """documentation needed"""
        return False

    def authorization_header(self, request=None) -> str:
        """documentation needed"""
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """documentation needed"""
        return None
