import unittest

from bigquery_validator.bigquery_result import BigQueryResult

query = '''
select *
  from `bigquery-public-data.baseball.schedules` 
 where year = 2016
 order by startTime
'''

def test_game_id_is_always_unique():
  bqr = BigQueryResult(query)
  result_metadata = bqr.metadata()
  unique_rows = len(result_metadata['unique_values']['gameId'])
  total_rows = result_metadata['nrows']
  assert unique_rows == total_rows

def test_season_id_is_never_null():
  bqr = BigQueryResult(query)
  result_metadata = bqr.metadata()
  null_values = result_metadata['null_values']['seasonId']
  assert 0 == null_values


def test_query_results_contain_expected_columns():
  bqr = BigQueryResult(query)
  result_metadata = bqr.metadata()
  columns = result_metadata['columns']
  expected_columns = ['gameId', 'seasonId', 'homeTeamId', 'awayTeamId']
  
  for col in expected_columns:
    assert col in expected_columns
