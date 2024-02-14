#!/usr/bin/env python3
""" script that contain SessionAuth class"""

from api.v1.auth.auth import Auth
from models.user import User
import uuid


class SessionAuth(Auth):
    """ empty for now"""
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """method that create a session id"""

        if user_id is None or not isinstance(user_id, str):
            return None

        session_id = str(uuid.uuid4())
        SessionAuth.user_id_by_session_id[session_id] = user_id
        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """ method returning the user id based on session id"""

        if session_id is None or not isinstance(session_id, str):
            return None

        return SessionAuth.user_id_by_session_id.get(session_id)

    def current_user(self, request=None):
        """ identifing a user
        method returns a user instance based on a cookie value"""

        sess_id = self.session_cookie(request)
        if sess_id is None:
            return None

        user_id = self.user_id_for_session_id(sess_id)
        user = User.get(user_id)
        return user

    def destroy_session(self, request=None):
        """ method delete the user session/logout"""

        if request is None or self.session_cookie(request) is None:
            return False

        session_id = self.session_cookie(request)
        user_id = self.user_id_for_session_id(session_id)
        if not user_id:
            return False

        del SessionAuth.user_id_by_session_id[session_id]
        return True
