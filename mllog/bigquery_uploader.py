"""Uploads a JSON formatted file to BigQuery."""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import argparse
import datetime
import json
import sys

from google.cloud import bigquery


def upload_file(metrics_file, project, dataset, table, model_name=None):
  """Uploads an MLLog JSON metrics file to BigQuery.

  Args:
    metrics_file: Path to JSON file.
    project: Name of BigQuery project.
    dataset: Dataset within project.
    table: Table within dataset.
    model_name: Unique name of this model benchmark.

  Returns:
    List of errors, if any.
  """
  with open(metrics_file) as fp:
    metrics = json.load(fp)

  metrics = convert_format_in_metrics_list(metrics)

  benchmark_run = [{
      'metrics': metrics,
      'upload_ts': _current_epoch_secs(),
      'model_name': model_name,
  }]

  return upload_metrics(benchmark_run, project, dataset, table)


def upload_metrics(metrics_dict, project, dataset, table):
  """Uploads a list of BigQuery-compliant metrics.

  Uses credentials loaded from envvars.

  Args:
    metrics_dict: List of metrics dicts.
    project: Name of BigQuery project.
    dataset: Dataset within project.
    table: Table within dataset.

  Returns:
    List of errors, if any.

  """
  # Credentials will be loaded from envvar $GOOGLE_APPLICATION_CREDENTIALS.
  bq_client = bigquery.Client(project=project)
  table_ref = bq_client.dataset(dataset).table(table)
  errors = bq_client.insert_rows_json(table_ref, metrics_dict)
  return errors


def convert_format_in_metrics_list(metrics):
  """Converts from human-friendly metadata format to BigQuery friendly format.

  Before:
    'metadata': {'file': 'example.py'}

  After:
    'metadata': [{'key': 'file', 'value': '"example.py"'}]

  Args:
    metrics: A list of metrics dicts.

  Returns:
    A list of metrics dicts with metadata fields reformatted.
  """

  def _convert_metadata_dict(metadatum):
    return [{'key': k, 'value': json.dumps(v)} for (k, v) in metadatum.items()]

  def _handle_special_keys(k, v):
    if k == 'metadata':
      return _convert_metadata_dict(v)
    if k == 'value':
      return json.dumps(v)
    return v

  def _convert_metrics_dict(metric):
    return {k: _handle_special_keys(k, v) for (k, v) in metric.items()}

  return [_convert_metrics_dict(m) for m in metrics]


def _current_epoch_secs():
  """Get epoch time, as .timestamp() was only added in Python 3.3."""
  now = datetime.datetime.utcnow()
  epoch = datetime.datetime(1970, 1, 1)
  return (now - epoch).total_seconds()


def main():
  parser = argparse.ArgumentParser(
      description='Uploads a JSON formatted file to BigQuery.')
  parser.add_argument(
      '--bigquery_project', type=str, help='The target BigQuery Project.')
  parser.add_argument(
      '--bigquery_dataset', type=str, help='The target BigQuery Dataset.')
  parser.add_argument(
      '--bigquery_table', type=str, help='The target BigQuery table.')
  parser.add_argument(
      '--metrics_file', type=str, help='The structured metrics file to upload.')
  parser.add_argument(
      '--model_name', type=str, help='The unique name of this model benchmark.')
  args = parser.parse_args()

  errors = upload_file(
      metrics_file=args.metrics_file,
      project=args.bigquery_project,
      dataset=args.bigquery_dataset,
      table=args.bigquery_table,
      model_name=args.model_name,
  )

  if errors:
    print(errors)
    sys.exit(1)


if __name__ == '__main__':
  main()
