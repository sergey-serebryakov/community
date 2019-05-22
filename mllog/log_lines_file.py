"""Utilities for parsing MLPerf log files."""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import json
import re

from mllog import metrics_file

TOKEN = ':::MLL'
LINE_PATTERN = r"""
^
{token} [ ] # token and version
([\d\.]+) [ ] # timestamp
([A-Za-z0-9_]+) [ ]? # key
:\s+(.+) # value
$
""".format(token=TOKEN)

LINE_REGEX = re.compile(LINE_PATTERN, re.X)


class ParsingError(RuntimeError):
  pass


class LogLineFile(object):
  """Represents a log file containing encoded metrics."""

  def __init__(self, filename):
    """Init a LogLineFile by loading from file."""
    with open(filename) as f:
      text = f.read()
    self.lines = []
    for line in text.split('\n'):
      if line.startswith(TOKEN):
        self.lines.append(line)

  def as_benchmark_run(self):
    """Converts this LogLineFile into a BenchmarkRun object."""
    metrics = []
    errors = []
    for line in self.lines:
      try:
        metrics.append(_convert_line_to_metric(line))
      except ParsingError as error:
        errors.append(error)
    return metrics_file.BenchmarkRun(metrics=metrics), errors


def _convert_line_to_metric(line):
  """Converts a single log line into a Metric object."""
  m = LINE_REGEX.match(line)
  if m is None:
    raise ParsingError('Could not parse: {}'.format(line))
  j = json.loads(m.group(3))
  d = metrics_file.Metric(
      float(m.group(1)), m.group(2), j['value'], j['metadata'])
  return d
