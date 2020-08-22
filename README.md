[![Build Status](https://travis-ci.com/sidarth164/LogAnalyze.svg?token=FYjCvjqVwECRHReK3ysP&branch=master)](https://travis-ci.com/sidarth164/LogAnalyze)
[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Python Versions](https://img.shields.io/pypi/pyversions/Markdown.svg)](https://pypi.org/project/Markdown/)

# LogAnalyze
This tool aims to provide a simple implementation for reading http log files, parsing it and methods to obtain some
simple aggregate reports.

## Getting Started
This section will help installing all the packages and binaries into the class path and make them available for use.

### Prerequisites
Install the dependencies required for this project using the `requirements.txt` file:
```
pip install -r requirements.txt
```
### Installation
To install the python packages provided by this package, follow the steps:
```
python setup.py install
```

## Usage
The user has the option to either use our custom provided script or to use the packages available.

### Script
We have exposed script named `log_reader` which could be used to generate the aggregate report for a
log file. Note that the script assumes that the logs are of *Common Log Format*.
```
usage: log_reader [-h] [-H H] [-R R] [-U U] [-N N] [-S] [-F] --file FILE
                  [--encoding ENCODING]

Generate a report for an HTTP log file.

optional arguments:
  -h, --help            show this help message and exit
  -H H, --top_hosts H   Display a report for the top H requesting hosts
  -R R, --top_resources R
                        Display a report for the top R resources requested
  -U U, --top_failed_resources U
                        Display a report for the top U resources requested
                        unsuccessfully
  -N N, --top_resources_per_host N
                        For each host, display the top N requested resources
  -S, --success_pct     Display the percentage of successful requests (of the
                        form 2xx, 3xx)
  -F, --fail_pct        Display the percentage of unsuccessful requests (of
                        the form 1xx, 4xx, 5xx)
  --file FILE           The absolute path of the log file whose report is to
                        be generated
  --encoding ENCODING   The file encoding to be used while reading it
```

### Python Packages
The following packages are available for use
- `logAnalyze.core`
- `logAnalyze.utils`

The enum class `LogFormat` provides a list of supported log formats. The user is expected to provide this enum for
correctly parsing the log line.
Use the utility method `parse()` present inside package `logAnalyze.utils` to parse the string log line. 
The function would parse the string `log` using the CLF format into tokens and return a dictionary
of these tokens.
```
pprint(parse(LogFormat.CLF, 'www-d4.proxy.aol.com - - [01/Aug/1995:00:01:49 -0400] "GET /images/rollout.gif HTTP/1.0" 200 258839'))
{'host': 'www-d4.proxy.aol.com',
 'identity': '-',
 'request': 'GET /images/rollout.gif HTTP/1.0',
 'size': '258839',
 'status': '200',
 'time': datetime.datetime(1995, 8, 1, 0, 1, 49, tzinfo=tzoffset(None, -14400)),
 'user': '-'}
```

The class `ReportAggregator` from package `logAnalyze.core` can be used to collect and aggregate the tokenized log
dictionaries. The below example illustrates how to use this class:
```python
from logAnalyze.core.report_aggregator import ReportAggregator
reporter = ReportAggregator()
log_dicts = []
# Add a list of tokenized dictionaries formed by parsing valid CLF logs

# After the list has been filled, use it to generate aggregate reports
for log_dict in log_dicts:
    reporter.receive_log(log_dict)
print(reporter.get_success_pct())  # Percentage of successful requests
print(reporter.get_failed_pct())  # Percentage of unsuccessful requests
top_requests = reporter.get_top_requests(10)  # top 10 resources with most requests
top_unsuccessful_requests = reporter.get_top_unsuccessful_requests(10)  # top 10 resources with most unsucessful requests
top_hosts = reporter.get_top_hosts(10)  # top 10 hosts with most requests 
```

## Supported Log Formats
### Common Log Format
A typical configuration for the http log of this format might look as follows:
```
host identity authuser date request status bytes
```
The log file records produced in CLF will look something like this:
```
127.0.0.1 - frank [10/Oct/2000:13:55:36 -0700] "GET /apache_pb.gif HTTP/1.0" 200 2326
```

