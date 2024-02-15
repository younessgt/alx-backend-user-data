#!/usr/bin/env python3
""" script contain SessionExpAuth class"""
from os import getenv
from api.v1.auth.session_auth import SessionAuth
from datetime import datetime, timedelta


class SessionExpAuth(SessionAuth):
    """doc doc doc"""

    def __init__(self):
        """constructor method"""
        try:
            self.session_duration = int(getenv("SESSION_DURATION", 0))
        except ValueError:
            self.session_duration = 0

    def create_session(self, user_id: str = None) -> str:
        """ method to create a session"""
        session_id = super().create_session(user_id)

        if session_id is None:
            return None
        session_dictionary = {}
        session_dictionary["user_id"] = user_id
        session_dictionary["created_at"] = datetime.now()
        SessionAuth.user_id_by_session_id[session_id] = session_dictionary
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """ method returning the user id based on session id"""
        if session_id is None:
            return None
        if session_id not in SessionAuth.user_id_by_session_id:
            return None
        session_dictionary = SessionAuth.user_id_by_session_id.get(session_id)

        if self.session_duration <= 0:
            return session_dictionary.get("user_id")

        if "created_at" not in session_dictionary:
            return None

        session_len = timedelta(seconds=self.session_duration)
        exp_duration = session_dictionary.get("created_at") + session_len
        if exp_duration < datetime.now():
            return None
        return session_dictionary.get("user_id")
