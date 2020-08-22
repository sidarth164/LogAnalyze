import unittest
from datetime import datetime

from dateutil.tz import tzoffset

from logAnalyze.utils.constants import LogFormat
from logAnalyze.utils.custom_exceptions import ParseError
from logAnalyze.utils.parse_utils import parse


class TestParseUtils(unittest.TestCase):
  def test_parse_valid(self):
    log, expected_log_dict = get_test_log_record()
    log_dict = parse(LogFormat.CLF, log)
    self.assertEqual(log_dict, expected_log_dict)

  def test_parse_invalid(self):
    logs = get_invalid_test_log_records()
    # Perform test with invalid CLF records
    for log in logs:
      self.assertRaises(ParseError, parse, LogFormat.CLF, log)

    # Perform test with invalid log_format passed
    valid_log, _ = get_test_log_record()
    self.assertRaises(ParseError, parse, 'invalid log format', valid_log)

    # Perform test by passing non-string log
    self.assertRaises(TypeError, parse, LogFormat.CLF, 123)


def get_test_log_record():
  log = '127.0.0.1 user-identifier frank [10/Nov/2000:13:55:36 -0700] "GET /apache_pb.gif HTTP/1.0" 200 2326'
  expected_log_dict = {
    'host': '127.0.0.1',
    'identity': 'user-identifier',
    'user': 'frank',
    'time': datetime(2000, 11, 10, 13, 55, 36, tzinfo=tzoffset(None, -25200)),
    'request': 'GET /apache_pb.gif HTTP/1.0',
    'status': '200',
    'size': '2326'
  }
  return log, expected_log_dict


def get_invalid_test_log_records():
  return [
    # invalid regex (date should be enclosed inside [])
    '127.0.0.1 - - 10/Nov/2000:13:55:36 -0700 "GET /apache_pb.gif HTTP/1.0" 200 2326',
    # invalid request method
    '127.0.0.1 - - [10/Nov/2000:13:55:36] -0700 "GETS /apache_pb.gif HTTP/1.0" 200 2326',
    # invalid request regex (method should be in all capitals)
    '127.0.0.1 - - [10/Nov/2000:13:55:36] -0700 "get /apache_pb.gif HTTP/1.0" 200 2326'
  ]
