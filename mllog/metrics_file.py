"""Definition of metric structure and seiralization/deserialization.

Read and write a metrics structure to/from files and strings.
"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import collections
import json


# A structure for use in python which is nicer to use than
# a raw dictionary.
Metric = collections.namedtuple('Metric', [
    'timestamp', 'key', 'value', 'metadata'
  ])


def parse_metrics_from_string(metrics_string):
  ''' Parses a string of json serialized metrics. '''
  return [dict_to_metric(j) for j in json.loads(metrics_string)]


def encode_metrics_as_string(metrics):
  ''' Encodes a list of Metric structs as a json string. '''
  return json.dumps([metric_to_dict(m) for m in metrics])


def dict_to_metric(j):
  ''' Converts a json dict to a Metric struct. '''
  return Metric(j['ts'], j['key'], j['value'], j['metadata'])


def metric_to_dict(m):
  ''' Converts a metrics struct to a json dict. '''
  return {
      'ts': m.timestamp,
      'key': m.key,
      'value': m.value,
      'metadata': m.metadata,
  }


def read_metrics_from_file(file_name):
  ''' Returns a file as a list of Metric structs. '''
  with open(file_name) as f:
    return parse_metrics_from_string(f.read())


def write_metrics_to_file(metrics, file_name):
  ''' Writes a list of Metric structs to a file. '''
  with open(file_name, 'w') as f:
    f.write(encode_metrics_as_string(metrics))

