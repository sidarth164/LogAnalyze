import unittest
from core.report_aggregator import ReportAggregator
from utils.constants import LogFormat
from utils.custom_exceptions import StatusError
from utils.parse_utils import parse
from test_utils.utils import get_random_int, get_random_host, get_random_path, get_random_query, get_random_status, \
  get_random_element, get_clf_log, get_top_requests


class TestReportAggregator(unittest.TestCase):
  def test_report(self):
    logs, expected_report = logs_and_report()

    reporter = ReportAggregator()
    # send the logs to the reporter
    for log in logs:
      reporter.receive_log(parse(LogFormat.CLF, log))

    num_requests_successful = expected_report['num_requests_successful']
    num_requests_unsuccessful = expected_report['num_requests_unsuccessful']
    num_requests = num_requests_successful + num_requests_unsuccessful

    # Validate percentage successful/unsuccessful requests
    self.assertLessEqual(abs(reporter.get_success_pct() - num_requests_successful / num_requests * 100), 1e-9)
    self.assertLessEqual(abs(reporter.get_failed_pct() - num_requests_unsuccessful / num_requests * 100), 1e-9)

    # Validate the top 'x' resources requested
    x = get_random_int(5, 15)
    expected_top_resources = get_top_requests(expected_report['resource_dict'], x, 0)
    top_resources = reporter.get_top_requests(x)
    for i, resource in enumerate(top_resources):
      self.assertEqual(expected_top_resources[i]['name'], resource.resource_name)
      self.assertEqual(expected_top_resources[i]['num'], resource.get_num_requests())

    # Validate the top 'x' hosts requested
    x = get_random_int(5,15)
    expected_top_hosts = get_top_requests(expected_report['host_dict'], x, 0)
    top_hosts = reporter.get_top_hosts(x)
    for i, host in enumerate(top_hosts):
      self.assertEqual(expected_top_hosts[i]['name'], host.host_name)
      self.assertEqual(expected_top_hosts[i]['num'], host.get_num_requests())

    # Validate the top 'x' resources requested by each host
    x = get_random_int(3,10)
    for host in expected_report['host_dict']:
      expected_top_resources_per_host = get_top_requests(expected_report['host_dict'][host]['resource_dict'], x, 0)
      top_requests_per_host = reporter.host_dict[host].get_top_requests(x)
      for i, req in enumerate(top_requests_per_host):
        self.assertEqual(expected_top_resources_per_host[i]['name'], req.resource_name)
        self.assertEqual(expected_top_resources_per_host[i]['num'], req.get_num_requests())

  def test_status_error(self):
    log = get_clf_log(get_random_host, get_random_path() + get_random_query(), '888')  # pass an invalid status
    reporter = ReportAggregator()
    log_dict = parse(LogFormat.CLF, log)
    self.assertRaises(StatusError, reporter.receive_log, log_dict)


def logs_and_report():
  host_num = get_random_int(25, 50)
  hosts = []  # list of hosts that would fire request
  for _ in range(host_num):
    hosts.append(get_random_host())

  resources_num = get_random_int(100, 150)
  resources = []  # list of available resources
  for _ in range(resources_num):
    resources.append(get_random_path() + get_random_query())

  num_requests_successful = get_random_int(500, 1000)
  num_requests_unsuccessful = get_random_int(500, 1000)

  host_dict = {}  # a dict containing mapping from host_name to the number of requests made on it and all the pages
  # the host requested for

  resource_dict = {}  # a dict containing mapping from the resource to the number of requests

  logs = []  # the list of all the request logs

  # function to update the dicts
  def update_dicts(is_success, resource_name, host_name):
    x_success = x_fail = 0
    if is_success:
      x_success = 1
    else:
      x_fail = 1

    if resource_name in resource_dict:
      resource_dict[resource_name]['num_requests_successful'] += x_success
      resource_dict[resource_name]['num_requests_unsuccessful'] += x_fail
    else:
      resource_dict[resource_name] = {}
      resource_dict[resource_name]['num_requests_successful'] = x_success
      resource_dict[resource_name]['num_requests_unsuccessful'] = x_fail

    if host_name in host_dict:
      host_dict[host_name]['num_requests_successful'] += x_success
      host_dict[host_name]['num_requests_unsuccessful'] += x_fail
      if resource_name in host_dict[host_name]['resource_dict']:
        host_dict[host_name]['resource_dict'][resource_name]['num_requests_successful'] += x_success
        host_dict[host_name]['resource_dict'][resource_name]['num_requests_unsuccessful'] += x_fail
      else:
        host_dict[host_name]['resource_dict'][resource_name] = {}
        host_dict[host_name]['resource_dict'][resource_name]['num_requests_successful'] = x_success
        host_dict[host_name]['resource_dict'][resource_name]['num_requests_unsuccessful'] = x_fail
    else:
      host_dict[host_name] = {}
      host_dict[host_name]['num_requests_successful'] = x_success
      host_dict[host_name]['num_requests_unsuccessful'] = x_fail
      host_dict[host_name]['resource_dict'] = {}
      host_dict[host_name]['resource_dict'][resource_name] = {}
      host_dict[host_name]['resource_dict'][resource_name]['num_requests_successful'] = x_success
      host_dict[host_name]['resource_dict'][resource_name]['num_requests_unsuccessful'] = x_fail

  # Now randomly generate the http logs (in clf format)
  for _ in range(num_requests_successful):
    # Create logs for successful requests
    status = get_random_status(True)
    resource_ = get_random_element(resources)
    host_ = get_random_element(hosts)
    logs.append(get_clf_log(host_, resource_, status))
    update_dicts(True, resource_, host_)

  for _ in range(num_requests_unsuccessful):
    # Create logs for unsuccessful requests
    status = get_random_status(False)
    resource_ = get_random_element(resources)
    host_ = get_random_element(hosts)
    logs.append(get_clf_log(host_, resource_, status))
    update_dicts(False, resource_, host_)

  report = {'host_dict': host_dict,
            'resource_dict': resource_dict,
            'num_requests_successful': num_requests_successful,
            'num_requests_unsuccessful': num_requests_unsuccessful}
  return logs, report
