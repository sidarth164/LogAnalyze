import re

from src.utils import constants
from src.utils.custom_exceptions import StatusError


class ReportAggregator:
  """
  This class receives incoming parsed log records (in a dict format), and generates aggregate reports
  like top 10 requesting hosts, percentage of unsuccessful requests etc.

  :ivar num_requests_successful: number of successful requests received
  :ivar num_requests_unsuccessful: number of unsuccessful requests received
  :ivar host_dict: a dictionary of hosts which have made any requests
  :ivar resource_dict: a dictionary of resources requested any time
  """

  def __init__(self):
    self.num_requests_successful = 0
    self.num_requests_unsuccessful = 0
    self.host_dict = {}
    self.resource_dict = {}

  def receive_log(self, log_dict):
    """
    This method is to be used to add a log to the report aggregator.

    :param log_dict: The dictionary object which has been parsed from the log string
    :type log_dict: dict
    """
    host_name = log_dict['host']
    resource_name = log_dict['request']
    status = log_dict['status']
    is_success = self.is_success(status)
    if is_success:
      self.num_requests_successful += 1
    else:
      self.num_requests_unsuccessful += 1

    if host_name in self.host_dict:
      host = self.host_dict[host_name]
    else:
      host = Host(host_name)
      self.host_dict[host_name] = host
    host.add_resource(resource_name, is_success)

    if resource_name in self.resource_dict:
      resource = self.resource_dict[resource_name]
    else:
      resource = Resource(resource_name)
      self.resource_dict[resource_name] = resource
    resource.add_request(is_success)

  @staticmethod
  def is_success(status):
    """
    Checks if a received status represents a successful request (2xx or 3xx)

    :param status: A string status code
    :type status: str
    :return: True if it's a 2xx or 3xx format, otherwise False
    :rtype: bool
    :raises StatusError: If the received http status is not of the form xxx (where x is a decimal)
    """
    if re.match(constants.SUCCESS_STATUS, status):
      return True
    elif re.match(constants.FAIL_STATUS, status):
      return False
    raise StatusError('Unidentifiable http status code: %s' % status)

  def get_top_hosts(self, n=10):
    """
    Get a list of the top n hosts making the most requests

    :param n: the number of hosts to return
    :type n: int
    :return: the list of top n hosts making the most requests
    :rtype: list
    """
    # sort the dictionary in reverse order, first using the number of requests made by each host and then using the
    # host name
    sorted_host_list = sorted(self.host_dict.items(),
                              key=lambda item: (item[1].get_num_requests(), item[1].host_name), reverse=True)
    return [v for k, v in sorted_host_list[:n]]

  def get_top_requests(self, n=10):
    """
    Get a list of the top n requested resources

    :param n: the number of resources to return
    :type n: int
    :return: the list of top n requested resources
    :rtype: list
    """
    # sort the dictionary in reverse order, first using the number of requests for each resource and then using the
    # resource name
    sorted_resource_list = sorted(self.resource_dict.items(),
                                  key=lambda item: (item[1].get_num_requests(), item[1].resource_name), reverse=True)
    return [v for k, v in sorted_resource_list[:n]]

  def get_success_pct(self):
    """
    Percentage of successful requests received.

    :rtype: float
    """
    return self.num_requests_successful / (self.num_requests_successful + self.num_requests_unsuccessful) * 100

  def get_failed_pct(self):
    """
    Percentage of unsuccessful requests received.

    :rtype: float
    """
    return 100 - self.get_success_pct()


class Host(object):
  """
  A class representing a host which might have made a request on the server. It also has the capability
  of aggregating some basic information, such as the top requested resources from this host, etc.

  :ivar host_name: the domain name or the ip address of the host
  :ivar num_requests_successful: the number of successful requests made by this host
  :ivar num_requests unsuccessful: the number of unsuccessful requests made by this host
  :ivar resource_dict: a dictionary of resources requested by this host
  """

  def __init__(self, host_name):
    self.host_name = host_name
    self.num_requests_successful = 0
    self.num_requests_unsuccessful = 0
    self.resource_dict = {}

  def add_resource(self, resource_name, is_success):
    """
    Add a resource to the list of resources requested by the host

    :param resource_name: the name of the resource
    :type resource_name: str
    :param is_success: True if the request to this resource succeeded
    :type is_success: bool
    """
    if is_success:
      self.num_requests_successful += 1
    else:
      self.num_requests_unsuccessful += 1

    if resource_name in self.resource_dict:
      resource = self.resource_dict[resource_name]
    else:
      resource = Resource(resource_name)
      self.resource_dict[resource_name] = resource
    resource.add_request(is_success)

  def get_num_requests(self):
    return self.num_requests_successful + self.num_requests_unsuccessful

  def get_top_requests(self, n=5):
    """
    Get a list of the top n resources requested by this host

    :param n: The number of resources to return
    :type n: int
    :return: list of the top n requested resources
    :rtype: list
    """
    sorted_resource_list = sorted(self.resource_dict.items(),
                                  key=lambda item: (item[1].get_num_requests(), item[1].resource_name), reverse=True)
    return [v for k, v in sorted_resource_list[:n]]


class Resource(object):
  """
  A class representing a resource on the server that might have been requested at any time.

  :ivar resource_name: the name of the resource, generally represented by a path like /sample/resource
  :ivar num_requests_successful: the number of successful requests made on this resource
  :ivar num_requests_unsuccessful: the number of unsuccessful requests made on this resource
  """

  def __init__(self, resource_name):
    self.resource_name = resource_name
    self.num_requests_successful = 0
    self.num_requests_unsuccessful = 0

  def add_request(self, is_success):
    """
    Modify the counters of this resource. Increment num_requests_successful if the request was successful,
    otherwise increment num_requests_unsuccessful

    :param is_success: True if the request was successful
    :type is_success: bool
    """
    if is_success:
      self.num_requests_successful += 1
    else:
      self.num_requests_unsuccessful += 1

  def get_num_requests(self):
    return self.num_requests_successful + self.num_requests_unsuccessful
