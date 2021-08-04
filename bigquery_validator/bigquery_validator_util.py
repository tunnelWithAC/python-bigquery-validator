from datetime import datetime, timedelta

GREEN = '\033[92m'
RED = '\x1b[31;21m'
RESET_SEQ = "\033[0m"


def print_success(msg, end=''):
    """Print a message to the console with green colored text"""
    if end != '' and end != '\n':
        print("                      ", end=end)
    print(f'{GREEN}{msg}{RESET_SEQ}', end=end)


def print_failure(msg, end=''):
    """Print a message to the console with red colored text"""
    if end != '':
        print("                      ", end=end)
    print(f'{RED}{msg}{RESET_SEQ}', end=end)


today = datetime.now()
yesterday = datetime.now() - timedelta(days=1)

# https://airflow.apache.org/docs/apache-airflow/stable/macros-ref.html
def datetime_to_ds(dt):
    """Convert a Python datetime object to a string with the format YYYY-MM-DD"""
    return dt.strftime('%Y-%m-%d')


def datetime_to_ds_nodash(dt):
    """Convert a Python datetime object to a string with the format YYYYMMDD"""
    return dt.strftime('%Y%m%d')


def get_default_params():
    """Return dict object containing keys/values that mimic Apache Airflow default macros"""
    return {
        'ds': datetime_to_ds(yesterday),
        'ds_nodash': datetime_to_ds_nodash(yesterday),
        'tomorrow_ds_nodash': datetime_to_ds_nodash(today),
        'tomorrow_ds': datetime_to_ds(today)
    }


# @retry.with_exponential_backoff(
#       num_retries=MAX_RETRIES,
#       retry_filter=retry_on_http_timeout_and_value_error)
#   def _query_with_retry(self):
#     """Run Bigquery query with retry if got error http response"""
#     _LOGGER.info('Attempting to perform query %s to BQ', self.query)
#     # Create client here since it throws an exception if pickled.
#     bigquery_client = bigquery.Client(self.project)
#     query_job = bigquery_client.query(self.query)
#     rows = query_job.result(timeout=60)
#     return [row.values() for row in rows]