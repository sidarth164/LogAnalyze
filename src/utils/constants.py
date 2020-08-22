"""
This file contains some constants to be used commonly in our project.
"""
from enum import Enum

# Regex patterns for the identifiable entities inside the logs
HOST = r'^(?P<host>.*?)'
SPACE = r'\s'
IDENTITY = r'(?P<identity>\S+)'
USER = r'(?P<user>\S+)'
TIME = r'\[(?P<time>.*?)\]'
REQUEST = r'\"(?P<request>.*?)\"'
STATUS = r'(?P<status>\d{3})'
SIZE = r'(?P<size>\S+)'
FAIL_STATUS = r'[145]\d\d'
SUCCESS_STATUS = r'[23]\d\d'


class LogFormat(Enum):
  CLF = {
    'regex': HOST + SPACE + IDENTITY + SPACE + USER + SPACE + TIME + SPACE + REQUEST + SPACE + STATUS + SPACE + SIZE,
    'name': 'Common Log Format'
  }
