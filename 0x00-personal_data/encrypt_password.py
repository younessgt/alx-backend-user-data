#!/usr/bin/python3
"""script for encryption passwords"""
import bcrypt


def hash_password(password: str) -> bytes:
    """ function that take  one string argument name password
    and returns a salted, hashed password"""

    str_byte = password.encode('utf-8')
    hashed = bcrypt.hashpw(str_byte, bcrypt.gensalt())
    return hashed
