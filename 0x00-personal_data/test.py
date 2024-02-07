#!/usr/bin/env python3

from typing import List
import re
import logging
import os
import mysql.connector


def get_db() -> mysql.connector.connection.MySQLConnection:
    """returns a connector to the database"""
    username = os.environ.get("PERSONAL_DATA_DB_USERNAME", "root")
    password = os.environ.get("PERSONAL_DATA_DB_PASSWORD", "")
    host = os.environ.get("PERSONAL_DATA_DB_HOST", "localhost")
    db_name = os.environ.get("PERSONAL_DATA_DB_NAME")

    config = {
            'user': username,
            'password': password,
            'host': host,
            'database': db_name
    }
    connection = mysql.connector.connection.MySQLConnection(**config)
    # the connection is closed in the 3-main.py file
    return connection


def main():

    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM users;")
    
    for row in cursor:
        print(type(row))
        name, email, phone, ssn, password, ip, last_login, user_agent = row
        message = f"name={name};email={email};"\
                  f"phone={phone};ssn={ssn};ip={ip};"\
                  f"password={password};last_login={last_login};"\
                  f"user_agent={user_agent}"


if __name__ == "__main__":
    main()
