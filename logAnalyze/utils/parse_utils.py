"""
This file contains some utility methods which can be used be our core package
"""
import re

from dateutil import parser

from logAnalyze.utils.custom_exceptions import ParseError
from .constants import LogFormat


def parse(log_format, log):
  """
  This method parses a CLF log string line into a dictionary of objects that can be used for further analysis.

  The parsed dict contains the following fields:
    * :host: the client host that made the request
    * :identity: the client's identity (usually '-')
    * :user: the userid of the person requesting the document (usually '-')
    * :time: the datetime object representing the time when the request was received
    * :request: the request line received from the client
    * :status: the http status code returned to the client
    * :size: size of the object returned to the client (measured in bytes)

  :param log_format: the enum value of the log format to be used
  :type log_format: .constants.LogFormat
  :param log: a string containing a single record of the CLF log type
  :type log: str
  :return: a dictionary of standard fields with well defined meanings
  :rtype: dict
  :raises ParseError: if the log is not in the desired format or the log_format provided was invalid
  """
  if not isinstance(log_format, LogFormat):
    raise ParseError('Please pass a valid log_format of type %s' % LogFormat)

  try:
    log_match = re.match(log_format.value['regex'], log)
    host = log_match.group('host')
    identity = log_match.group('identity')
    user = log_match.group('user')
    time = get_datetime_from_clf_date(log_match.group('time'))
    request = log_match.group('request')
    status = log_match.group('status')
    size = log_match.group('size')
  except (AttributeError, ParseError, ValueError) as ex:
    raise ParseError('Could not parse the log of type [%s]: %s' % (log_format.value['name'], log)) from ex

  parsed_log = {
    'host': host,
    'identity': identity,
    'user': user,
    'time': time,
    'request': request,
    'status': status,
    'size': size
  }
  return parsed_log


def get_datetime_from_clf_date(date):
  """
  This method coverts the CLF time format to a python datetime object

  :param date: a string value of the datetime extracted from the CLF log
  :type date: str
  :return: a python datetime object
  :rtype: datetime.datetime
  """
  return parser.parse(date.replace(':', ' ', 1))
