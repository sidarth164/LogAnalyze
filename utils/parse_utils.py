"""
This file contains some utility methods which can be used be our core scripts
"""
from dateutil import parser
import re

from .constants import REQUEST_REGEX, HttpRequestMethod, HttpProtocolVersion


def parse(log_regex, log):
  """
  This method parses a CLF log string line into a dictionary of objects that can be used for further analysis.

  The parsed dict contains the following fields:
    * :host: the client host that made the request
    * :identity: the client's identity (usually '-')
    * :user: the userid of the person requesting the document (usually '-')
    * :time: the datetime when the request was received
    * :request: the request dict containing parsed request line received from the client
    * :status: the http status code returned to the client

  :param log_regex: the regex string to be used to parse the log record
  :type log_regex: str
  :param log: a string containing a single record of the CLF log type
  :type log: str
  :return: a dictionary of standard fields with well defined meanings
  :rtype: dict
  """
  log_match = re.match(log_regex, log)
  host = log_match.group('host')
  identity = log_match.group('identity')
  user = log_match.group('user')
  time = log_match.group('time')
  request = get_request(log_match.group('request'))
  status = log_match.group('status')

  parsed_log = {
    'host': host,
    'identity': identity,
    'user': user,
    'time': time,
    'request': request,
    'status': status
  }
  return parsed_log


def get_request(req):
  """
  This method takes the string request line extracted from the log and parses it into a dict.

  The parsed dict contains the following fields:
    * :method: the http request method enum
    * :path: the path string
    * :query: the query dict
    * :protocol: the HTTP protocol enum

  :param req: the request string extracted from the log in raw form
  :type req: str
  :return: a well parsed dictionary with well defined meanings
  :rtype: dict
  """
  req_match = re.match(REQUEST_REGEX, req)
  method = HttpRequestMethod[req_match.group('method')]
  path = req_match.group('path')
  query = req_match.group('query')
  protocol = HttpProtocolVersion(req_match.group('protocol'))
  parsed_req = {
    'method': method,
    'path': path,
    'query': query,
    'protocol': protocol
  }
  return parsed_req


def get_datetime_from_clf_date(date):
  """
  This method coverts the CLF time format to a python datetime object

  :param date: a string value of the datetime extracted from the CLF log
  :type date: str
  :return: a python datetime object
  :rtype: datetime.datetime
  """
  return parser.parse(date.replace(':', ' ', 1))
