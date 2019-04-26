"""Definition of metric structure and serialization/deserialization.

Read and write a metrics structure to/from files and strings.
"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import collections
import json


class Metric(
    collections.namedtuple('Metric',
                           ['timestamp', 'key', 'value', 'metadata'])):
  """A Metric is a discrete observation of a model."""

  @staticmethod
  def from_dict(d):
    """Converts a json dict to a Metric struct."""
    return Metric(d['ts'], d['key'], d['value'], d['metadata'])

  def to_dict(self):
    """Converts a metrics struct to a json dict."""
    return {
        'ts': self.timestamp,
        'key': self.key,
        'value': self.value,
        'metadata': self.metadata,
    }


class BenchmarkRun(collections.namedtuple('BenchmarkRun', ['metrics'])):
  """A BenchmarkRun is a set of Metric objects from a single execution."""

  @staticmethod
  def from_string(metrics_json):
    """Parses a string of json serialized metrics."""
    return BenchmarkRun([Metric.from_dict(j) for j in json.loads(metrics_json)])

  def to_string(self):
    """Encodes a list of Metric structs as a json string."""
    return json.dumps([m.to_dict() for m in self.metrics])

  @staticmethod
  def from_file(filename):
    """Returns a file as a list of Metric structs."""
    with open(filename) as f:
      return BenchmarkRun.from_string(f.read())

  def to_file(self, filename):
    """Writes a list of Metric structs to a file."""
    with open(filename, 'w') as f:
      f.write(self.to_string())
