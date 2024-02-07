#!/usr/bin/env python3
""" script doc"""
from typing import List
import re


def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str) -> str:
    """ returning the log message obfuscated"""
    pattern = rf"({'|'.join(fields)})=([^ {separator},\s]+)"
    new_message = re.sub(pattern, rf"\1={redaction}", message)
    return new_message
