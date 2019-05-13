"""Summarize one or more log files."""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import sys
import glob

from mllog import log_lines_file


class Stats(object):
  def __init__(self):
    pass


class FileStats(object):
  def __init__(self):
    self.init_start = None
    self.init_stop = None
    self.run_start = None
    self.run_stop = None
    self.benchmark = None
    self.system = None
    self.org = None

  def __str__(self):
    return '{} {} {} {:.2f}s (init={:.2f}m)'.format(self.org, self.system, self.benchmark, self.run_stop - self.run_start, (self.init_stop - self.init_start)/60.0)


def process_metrics(metrics, stats):
  fs = FileStats()
  for metric in metrics:
    if metric.key == 'run_start':
      fs.run_start = metric.timestamp
    if metric.key == 'run_stop':
      fs.run_stop = metric.timestamp
    if metric.key == 'init_start':
      fs.init_start = metric.timestamp
    if metric.key == 'init_stop':
      fs.init_stop = metric.timestamp
    if metric.key == 'submission_benchmark':
      fs.benchmark = metric.value
    if metric.key == 'submission_platform':
      fs.system = metric.value
    if metric.key == 'submission_org':
      fs.org = metric.value
  print(fs)


def read_files(files):
  all_metrics = []
  for file in files:
    log_lines = log_lines_file.LogLineFile(file)
    metrics, errors = log_lines.as_benchmark_run()
    if errors:
      for e in errors:
        print(e)
        raise Exception('Could not parse file: ' + file)
    all_metrics.append(metrics.metrics)
  return all_metrics


def main():
  files = sys.argv[1:]
  globed = []
  for g in files:
    globed.extend(glob.glob(g))
  print(globed)
  stats = Stats()
  for metrics in read_files(globed):
    process_metrics(metrics, stats)

if __name__ == '__main__':
  main()
