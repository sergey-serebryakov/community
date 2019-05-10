"""Tests for bigquery_uploader.py."""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import datetime
import mock

import unittest

from mllog import bigquery_uploader


class BigQueryUploaderTest(unittest.TestCase):

  def test_convert_metadata(self):
    human_friendly = [{
        'key': 'k',
        'value': True,
        'ts': 4,
        'metadata': {
            'metakey': 'metaval'
        }
    }]

    biquery_friendly = [{
        'key': 'k',
        'value': 'true',
        'ts': 4,
        'metadata': [{
            'key': 'metakey',
            'value': '"metaval"'
        }]
    }]

    self.assertEqual(
        bigquery_uploader.convert_format_in_metrics_list(human_friendly),
        biquery_friendly)

  def test_current_epochs_secs(self):
    fake_now = datetime.datetime(1970, 1, 1, 0, 0, 42)

    # We can't patch datetime.datetime.utcnow directly as it's immutable.
    class FakeDatetime(datetime.datetime):

      @classmethod
      def utcnow(cls):
        return fake_now

    with mock.patch.object(bigquery_uploader, 'datetime') as mock_datetime:
      mock_datetime.datetime = FakeDatetime

      self.assertEqual(bigquery_uploader._current_epoch_secs(), 42)


if __name__ == '__main__':
  unittest.main()
