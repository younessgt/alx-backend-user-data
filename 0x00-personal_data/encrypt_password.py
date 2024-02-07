#!/usr/bin/env python3
"""script for encryption passwords"""
import bcrypt


def hash_password(password: str) -> bytes:
    """ function that take  one string argument name password
    and returns a salted, hashed password"""

    str_byte = password.encode('utf-8')
    hashed = bcrypt.hashpw(str_byte, bcrypt.gensalt())
    return hashed


def is_valid(hashed_password: bytes, password: str) -> bool:
    """ checking if the provided password
    matches the hashed password"""

    str_byte = password.encode('utf-8')
    if bcrypt.checkpw(str_byte, hashed_password):
        return True
    else:
        return False
