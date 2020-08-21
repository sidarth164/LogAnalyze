"""
This file contains some constants to be used commonly in our project.
"""
from enum import Enum

# Regex patterns for the identifiable entities inside the logs
HOST = r'^(?P<host>.*?)'
SPACE = r'\s'
IDENTITY = r'(?P<identity>\S+)'
USER = r'(?P<user>\S+)'
TIME = r'(?P<time>\[.*?\])'
REQUEST = r'\"(?P<request>.*?)\"'
STATUS = r'(?P<status>\d{3})'
METHOD = r'(?P<method>[A-Z]+)'
PATH_QUERY = r'(?P<path>[^?]+)(\?(?P<query>\S+))?'
PROTOCOL = r'(?P<protocol>\S+)'

# Regex formats
CLF_REGEX = HOST + SPACE + IDENTITY + SPACE + USER + SPACE + TIME + SPACE + REQUEST + SPACE + STATUS
REQUEST_REGEX = METHOD + SPACE + PATH_QUERY + SPACE + PROTOCOL


class HttpRequestMethod(Enum):
  GET = 1
  POST = 2
  PUT = 3
  DELETE = 4
  HEAD = 5
  PATCH = 6


class HttpProtocolVersion(Enum):
  V0_9 = 'HTTP/0.9'
  V1_0 = 'HTTP/1.0'
  V1_1 = 'HTTP/1.1'
  V2_0 = 'HTTP/2.0'
  V3_0 = 'HTTP/3.0'
