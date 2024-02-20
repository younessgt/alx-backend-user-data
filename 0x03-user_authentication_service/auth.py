#!/usr/bin/env python3
""" script contain auth method"""
from user import User
from bcrypt import hashpw, gensalt, checkpw
from db import DB
from sqlalchemy.orm.exc import NoResultFound
from uuid import uuid4
from typing import Union


def _hash_password(password: str) -> bytes:
    """ method that encrypt passwords """

    hashed_pass = hashpw(password.encode('utf-8'), gensalt())
    return hashed_pass


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        """ constructor """
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """ method for registring a user """
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            hashed_pass = _hash_password(password)
            user = self._db.add_user(email, hashed_pass)
            return user

        raise ValueError(f"User {email} already exists")

    def valid_login(self, email: str, password: str) -> bool:
        """ checking the loging validation"""
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            return False

        if checkpw(password.encode('utf-8'), user.hashed_password):
            return True
        return False

    def create_session(self, email: str) -> str:
        """ creating a session and returnig
        the session id as string"""

        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            return None
        session_id = _generate_uuid()
        self._db.update_user(user.id, session_id=session_id)
        return session_id

    def get_user_from_session_id(self, session_id: str) -> Union[User, None]:
        """ getting user from seesion_id"""
        if session_id is None:
            return None
        try:
            user = self._db.find_user_by(session_id=session_id)
            return user
        except NoResultFound:
            return None

    def destroy_session(self, user_id: int) -> None:
        """ destroying the session associated with this user"""
        if user_id is None:
            return None
        try:
            self._db.find_user_by(id=user_id)
            self._db.update_user(user_id, session_id=None)

        except NoResultFound:
            return None

    def get_reset_password_token(self, email: str) -> str:
        """ generationg the reset_passord_token """
        try:
            user = self._db.find_user_by(email=email)
            uu_id = _generate_uuid()
            self._db.update_user(user.id, reset_token=uu_id)
            return uu_id
        except NoResultFound:
            raise ValueError

    def update_password(self, reset_token: str, password: str) -> None:
        """ updating the user password """

        if reset_token is None or password is None:
            return None
        try:
            user = self._db.find_user_by(reset_token=reset_token)
        except NoResultFound:
            raise ValueError

        hashed_pass = _hash_password(password)
        self._db.update_user(user.id, hashed_password=hashed_pass,
                             reset_token=None)


def _generate_uuid() -> str:
    """ generating a uuid"""
    return str(uuid4())
