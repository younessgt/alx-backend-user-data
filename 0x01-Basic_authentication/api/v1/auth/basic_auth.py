#!/usr/bin/env python3
""" script containig BasicAuth class"""
from api.v1.auth.auth import Auth
from models.user import User
import base64
from typing import TypeVar


class BasicAuth(Auth):
    """ empty class"""

    def extract_base64_authorization_header(self,
                                            authorization_header: str) -> str:
        """ returns the Base64 part
        of the Authorization header for a Basic Authentication"""

        if (
            authorization_header is None or
            not isinstance(authorization_header, str)
           ):
            return None

        if not authorization_header.startswith("Basic "):
            return None
        return authorization_header[6:]

    def decode_base64_authorization_header(
        self,
        base64_authorization_header: str
    ) -> str:
        """returns the decoded value of a
        Base64 string base64_authorization_header """

        if (
            base64_authorization_header is None or
            not isinstance(base64_authorization_header, str)
           ):
            return None

        try:
            decoded64 = base64.b64decode(base64_authorization_header)

            return decoded64.decode("utf-8")
        except Exception:
            return None

    def extract_user_credentials(
        self,
        decoded_base64_authorization_header: str
    ) -> (str, str):
        """ returns the user email and password
        from the Base64 decoded value"""

        if (
            decoded_base64_authorization_header is None or
            not isinstance(decoded_base64_authorization_header, str)
           ):
            return (None, None)

        if ":" not in decoded_base64_authorization_header:
            return (None, None)

        email, password = decoded_base64_authorization_header.split(":")
        return (email, password)

    def user_object_from_credentials(
        self,
        user_email: str,
        user_pwd: str
    ) -> TypeVar('User'):
        """ returns the User instance based on his email and password"""

        if user_email is None or not isinstance(user_email, str):
            return None
        if user_pwd is None or not isinstance(user_pwd, str):
            return None

        try:
            users = User.search({"email": user_email})
        except Exception:
            return None

        if len(users) == 0:
            return None
        for user in users:
            if user.is_valid_password(user_pwd):
                return user
        return None
