"""Encodes a key-vlaue pair as either a json or string log line.

"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import argparse
import json
import re
import sys

from mllog import metrics_file


LINE_PATTERN = '''
^
:::MLM [ ] # token and version
([\d\.]+) [ ] # timestamp
([A-Za-z0-9_]+) [ ]? # key
:\s+(.+) # value
$
'''

LINE_REGEX = re.compile(LINE_PATTERN, re.X)


def convert_line_to_metric(line):
  m = LINE_REGEX.match(line)
  if m is None:
    return None, 'Could not parse: {}'.format(line)
  j = json.loads(m.group(3))
  d = metrics_file.Metric(
      float(m.group(1)),
      m.group(2),
      j['value'],
      j['metadata'])
  return d, None


def parse_lines_as_metrics(lines):
  metrics = []
  errors = []
  for line in lines:
    metric, error = convert_line_to_metric(line)
    if metric is not None:
      metrics.append(metric)
    if error is not None:
      errors.append(error)
  return metrics, errors


def read_log_file(log_file_name):
  with open(log_file_name) as f:
    text = f.read()
  lines = []
  for line in text.split('\n'):
    if line.startswith(':::MLM'):
      lines.append(line)
  return lines


def convert_files(input_log, output_metrics):
  lines = read_log_file(input_log)
  metrics, errors = parse_lines_as_metrics(lines)
  if errors:
    for e in errors:
      print(e)
  metrics_file.write_metrics_to_file(metrics, output_metrics)
  return errors 


def main():
  parser = argparse.ArgumentParser(description='Covnert log file to structured metrics file.')
  parser.add_argument('log_file', metavar='LOG_FILE', type=str,
                      help='the log file to convert.')
  parser.add_argument('metrics_file', metavar='METRICS_FILE', type=str,
                      help='the structured metrics file to create/overwrite.')
  args = parser.parse_args()
  if not convert_files(args.log_file, args.metrics_file):
    sys.exit(1)


if __name__ == '__main__':
  main()

