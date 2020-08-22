"""
This file contains some utility functions that are used by our tests
"""
import random
from string import ascii_lowercase
from rstr import xeger
from datetime import datetime, timedelta

import pytz

from utils.constants import HttpRequestMethod, HttpProtocolVersion, SUCCESS_STATUS, FAIL_STATUS


def get_clf_log(host, resource, status):
  return """{host} {identity} {user} [{datetime}] "{method} {resource} {protocol}" {status} {size}""" \
    .format(host=host, identity=get_random_id(), user=get_random_id(), datetime=get_random_datetime(),
            method=get_random_req_method(), resource=resource, protocol=get_random_http_protocol(),
            status=status, size=get_random_size())


def get_random_host():
  if get_random_bool:
    # fetch a random ip address
    return ".".join(map(str, (random.randint(0, 255) for _ in range(4))))
  else:
    # fetch a random domain name
    return ".".join(get_random_string(5) for _ in range(3))


def get_random_id():
  if get_random_bool:
    return '-'
  else:
    return get_random_string(4)


def get_random_path(nesting=4, max_len=5):
  random_path = '/'.join(get_random_string(random.randint(1, max_len)) for _ in range(nesting))
  return '/' + random_path


def get_random_query(max_len=5):
  if get_random_bool:
    return ''
  else:
    return '?' + get_random_string(random.randint(1, max_len))


def get_random_status(is_success):
  if is_success:
    return xeger(SUCCESS_STATUS)
  else:
    return xeger(FAIL_STATUS)


def get_random_datetime():
  tz = pytz.all_timezones
  random_tz = pytz.timezone(tz[random.randint(0, len(tz) - 1)])
  start = datetime(1990, 1, 1, tzinfo=random_tz)
  step = timedelta(days=1)  # granularity of selecting random date
  end = datetime.now(random_tz)
  random_date = start + random.randrange((end - start) // step + 1) * step
  return random_date.strftime('%d/%b/%Y:%H:%M:%S %z')


def get_random_http_protocol():
  protocol = random.choice(list(HttpProtocolVersion))
  return protocol.value


def get_random_req_method():
  method = random.choice(list(HttpRequestMethod))
  return method.name


def get_random_size(max_size=16 * 1024):
  return str(random.randint(0, max_size))


def get_random_bool():
  return bool(random.getrandbits(1))


def get_random_string(length):
  letters = ascii_lowercase
  random_str = ''.join(random.choice(letters) for _ in range(length))
  return random_str


def get_random_int(a, b):
  return random.randint(a, b)


def get_random_element(lst):
  return lst[random.randint(0, len(lst) - 1)]


def get_top_requests(dct, n, choice):
  """
  Returns the top n records with most number of requests (successful or unsuccessful or both)

  :param dct: dict containing the records
  :type dct: dict
  :param n: list size to return
  :type n: int
  :param choice: 0-both, 1-successful, 2-unsuccessful
  :type choice: int
  :return:
  """
  top_list = []

  def get_num(k):
    if choice == 0:
      return dct[k]['num_requests_successful'] + dct[k]['num_requests_unsuccessful']
    elif choice == 1:
      return dct[k]['num_requests_successful']
    else:
      return dct[k]['num_requests_unsuccessful']

  for key in dct:
    top_list.append({'name': key, 'num': get_num(key)})

  return sorted(top_list, key=lambda item: (item['num'], item['name']), reverse=True)[:n]
