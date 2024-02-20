#!/usr/bin/env python3
"""
Main file
"""
import requests


def register_user(email: str, password: str) -> None:
    """ register a user"""
    resp = requests.post("http://localhost:5000/users",
                         data={"email": email, "password": password})

    expected_resp = {"email": email, "message": "user created"}
    assert resp.status_code == 200
    assert resp.json() == expected_resp


def log_in_wrong_password(email: str, password: str) -> None:
    """ testing to login with wrong password"""
    resp = requests.post("http://localhost:5000/sessions",
                         data={"email": email, "password": password})
    assert resp.status_code == 401


def log_in(email: str, password: str) -> str:
    """user login """
    resp = requests.post("http://localhost:5000/sessions",
                         data={"email": email, "password": password})
    assert resp.status_code == 200
    expected_resp = {"email": email, "message": "logged in"}
    assert resp.json() == expected_resp
    return resp.cookies.get("session_id")


def profile_unlogged() -> None:
    """ profile unlogged"""
    resp = requests.get("http://localhost:5000/profile")
    assert resp.status_code == 403


def profile_logged(session_id: str) -> None:
    """ user profile"""
    resp = requests.get("http://localhost:5000/profile",
                        cookies={"session_id": session_id})
    expected_resp = {"email": "guillaume@holberton.io"}
    assert resp.status_code == 200
    assert resp.json() == expected_resp


def log_out(session_id: str) -> None:
    """user logout"""
    resp = requests.delete("http://localhost:5000/profile",
                           cookies={"session_id": session_id})
    assert resp.status_code == 200 or resp.status_code == 302


def reset_password_token(email: str) -> str:
    """ reset password"""
    resp = requests.post("http://localhost:5000/reset_password",
                         data={"email": email})
    assert resp.status_code == 200
    return resp.json().get('reset_token')


def update_password(email: str, reset_token: str, new_password: str) -> None:
    """updating user password"""
    resp = requests.put('http://localhost:5000/reset_password', data={
        'email': email,
        'reset_token': reset_token,
        'new_password': new_password
    })
    assert resp.status_code == 200
    assert resp.json() == {'email': email, 'message': "Password updated"}


EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"


if __name__ == "__main__":

    register_user(EMAIL, PASSWD)
    log_in_wrong_password(EMAIL, NEW_PASSWD)
    profile_unlogged()
    session_id = log_in(EMAIL, PASSWD)
    profile_logged(session_id)
    log_out(session_id)
    reset_token = reset_password_token(EMAIL)
    update_password(EMAIL, reset_token, NEW_PASSWD)
    log_in(EMAIL, NEW_PASSWD)
