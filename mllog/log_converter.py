"""Converts log-line format files to JSON format files."""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import argparse
import sys

from mllog import log_lines_file


def convert_file(input_log, output_metrics):
  """Converts log-line format file to json format file."""
  log_lines = log_lines_file.LogLineFile(input_log)
  metrics, errors = log_lines.as_benchmark_run()
  if errors:
    for e in errors:
      print(e)
  metrics.to_file(output_metrics)
  return errors


def main():
  parser = argparse.ArgumentParser(
      description='Convert log file to structured metrics file.')
  parser.add_argument('log_file', metavar='LOG_FILE', type=str,
                      help='the log file to convert.')
  parser.add_argument('metrics_file', metavar='METRICS_FILE', type=str,
                      help='the structured metrics file to create/overwrite.')
  args = parser.parse_args()
  if convert_file(args.log_file, args.metrics_file):
    sys.exit(1)


if __name__ == '__main__':
  main()
