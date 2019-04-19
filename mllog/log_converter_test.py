"""Tests for log_converter.py."""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import unittest

from mllog import log_converter
from mllog import metrics_file


class LogConverterTest(unittest.TestCase):
  def test_convert_line_to_metric(self):
    line = ':::MLM 123 foo : { "value": "bar", "metadata": {} }'

    expected = metrics_file.Metric(123, 'foo', 'bar', {})
    self.assertEqual(log_converter.convert_line_to_metric(line)[0], expected)

  def test_parse_lines_as_metrics(self):
    lines = [':::MLM 123 clock : { "value": "START", "metadata": {} }',
      ':::MLM 124 quality : { "value": "77.1", "metadata": {} }',
             ':::MLM 125 clock : { "value": "END", "metadata": {} }']
    expected = [
        metrics_file.Metric(123, 'clock', 'START', {}),
        metrics_file.Metric(124, 'quality', '77.1', {}),
        metrics_file.Metric(125, 'clock', 'END', {})]
    parsed, errors = log_converter.parse_lines_as_metrics(lines)
    self.assertEqual(errors, [])
    self.assertEqual(parsed, expected)


if __name__ == '__main__':
  unittest.main()
