"""A simple utility to return the MLPerf score of a file

"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import sys

from mllog import log_lines_file


def get_start_and_stop_from_file(filename):
  log_lines = log_lines_file.LogLineFile(filename)
  metrics, errors = log_lines.as_benchmark_run()
  start_ts = None
  end_ts = None
  for m in metrics.metrics:
    if m.key == 'run_start':
      if start_ts is None:
        start_ts = m.timestamp
      start_ts = min(m.timestamp, start_ts)
    if m.key == 'run_stop':
      if end_ts is None:
        end_ts = m.timestamp
      end_ts = max(m.timestamp, end_ts)
  return start_ts, end_ts


def main():
  print(get_mlperf_score_from_file(sys.argv[1]))


if __name__ == '__main__':
  main()
