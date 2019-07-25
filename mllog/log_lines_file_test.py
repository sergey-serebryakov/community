"""Tests for log_converter.py."""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import tempfile

import unittest

from mllog import log_lines_file
from mllog import metrics_file


class LogLinesFileTest(unittest.TestCase):

  def test_convert_line_to_metric(self):
    line = ':::MLL 123 foo : { "value": "bar", "metadata": {} }'

    expected = metrics_file.Metric(123, 'foo', 'bar', {})
    self.assertEqual(log_lines_file._convert_line_to_metric(line), expected)

  def test_convert_line_to_metric_cases(self):
    self._assert_expected_metric(
        (':::MLL 123.456 /c1/c2/c3.key: '
         '{"value": 80.123, "metadata": '
         '{"lineno": 81, "file": "some_dir/some_file.py"}}'),
        metrics_file.Metric(123.456, '/c1/c2/c3.key', 80.123,
                            {'lineno': 81, 'file': 'some_dir/some_file.py'}))

    self._assert_expected_metric(
        ':::MLL 123 custom_metric: {"value": 80.123, "metadata": {}}',
        metrics_file.Metric(123, 'custom_metric', 80.123, {}))

    self._assert_expected_metric(
        ':::MLL 123 c1-c2-c3: {"value": 80.123, "metadata": {}}',
        metrics_file.Metric(123, 'c1-c2-c3', 80.123, {}))

    self._assert_expected_metric(
        ':::MLL 123 c1-c2-c3.c4: {"value": 80.123, "metadata": {}}',
        metrics_file.Metric(123, 'c1-c2-c3.c4', 80.123, {}))

  def _assert_expected_metric(self, input_line, expected_metric):
    converted_metric = log_lines_file._convert_line_to_metric(input_line)
    self.assertDictEqual(converted_metric.to_dict(), expected_metric.to_dict())

  def test_parse_lines_as_metrics(self):
    log_lines = [
        ':::MLL 123 clock : { "value": "START", "metadata": {} }',
        ':::MLL 124 quality : { "value": "77.1", "metadata": {} }',
        ':::MLL 125 clock : { "value": "END", "metadata": {} }',
    ]

    with tempfile.NamedTemporaryFile(mode='w', delete=False) as f:
      f.writelines('%s\n' % l for l in log_lines)

    expected = metrics_file.BenchmarkRun([
        metrics_file.Metric(123, 'clock', 'START', {}),
        metrics_file.Metric(124, 'quality', '77.1', {}),
        metrics_file.Metric(125, 'clock', 'END', {})
    ])

    log_f = log_lines_file.LogLineFile(f.name)
    parsed, errors = log_f.as_benchmark_run()

    self.assertEqual(errors, [])
    self.assertEqual(parsed, expected)


if __name__ == '__main__':
  unittest.main()
