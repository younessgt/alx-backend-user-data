#!/usr/bin/env python3
""" script doc"""
from typing import List
import re
import logging
import mysql.connector
import os

PII_FIELDS = ("email", "phone", "ssn", "password", "name")


def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str) -> str:
    """ returning the log message obfuscated"""
    pattern = rf"({'|'.join(fields)})=([^{separator},]+)"
    new_message = re.sub(pattern, rf"\1={redaction}", message)
    return new_message


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
        """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """ method to format a record """
        record.msg = filter_datum(self.fields, self.REDACTION,
                                  record.msg, self.SEPARATOR)
        formatter = logging.Formatter(self.FORMAT).format(record)
        # fromatter = super(RedactingFormatter, self).format(record)
        return formatter


def get_logger() -> logging.Logger:
    """ returning logger object"""
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    # creating the stream handler
    handler = logging.StreamHandler()
    handler.setFormatter(RedactingFormatter(list(PII_FIELDS)))
    logger.addHandler(handler)
    logger.propagate = False
    return logger


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
            'database': db_name,
            'port': 3306
    }
    connection = mysql.connector.connect(**config)
    return connection


def main():
    """The function will obtain a database connection
    using get_db and retrieve all rows in the users table
    and display each row under a filtered format """
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM users;")

    logger = get_logger()

    for row in cursor:
        name, email, phone, ssn, password, ip, last_login, user_agent = row
        message = f"name={name};email={email};"\
                  f"phone={phone};ssn={ssn};ip={ip};"\
                  f"password={password};last_login={last_login};"\
                  f"user_agent={user_agent}"
        logger.info(message)
    cursor.close()
    db.close()


if __name__ == "__main__":
    main()
