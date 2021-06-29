from config import Config
import json


import time
GREEN = '\033[92m'
RED = '\x1b[31;21m'
RESET_SEQ = "\033[0m"


# todo clear all output not just print to current line
def print_success(msg, end='\r'):
    print("", end=end, flush=True)
    print(f'{GREEN}{msg}{RESET_SEQ}', end=end, flush=True)
#
# for x in range(3):
#    time.sleep(2)
#
#    print_success(f'{x}')

# c = Config()
# json.dumps(c)
#

#
from bigquery_validator import BigQueryValidator

bigquery_validator = BigQueryValidator()
#
# bigquery_validator.validate_query( "SELECT count(*) FROM `bigquery-public-data.samples.github_timeline`")
#
# bigquery_validator.validate_query( "SELECT count(* FROM `bigquery-public-data.samples.github_timeline`")
#
# print('hello')

bigquery_validator.auto_validate_query_from_file('./bigquery_validator/tests/valid_query.sql')