import importlib.util
import logging
import os
import warnings

from google.cloud import bigquery
from jinja2 import Template

from config.config import get_default_params  # Config

logging.basicConfig(level=os.environ.get("LOGLEVEL", "WARNING"))
warnings.filterwarnings("ignore", "Your application has authenticated using end user credentials")

GREEN = '\033[92m'
RED = '\x1b[31;21m'
RESET_SEQ = "\033[0m"


def print_success(msg, end=''):
    if end != '' and end != '\n':
        print("                      ", end=end)
    print(f'{GREEN}{msg}{RESET_SEQ}', end=end)


def print_failure(msg, end=''):
    if end != '':
        print("                      ", end=end)
    print(f'{RED}{msg}{RESET_SEQ}', end=end)


class BigQueryValidator(object):

    def __init__(self,
                 dry_run=True,
                 use_query_cache=False):
        self.bq_client = bigquery.Client()
        self.dry_run = dry_run
        self.params = self.load_params()
        self.use_query_cache = use_query_cache

    def load_params(self):
        extra_params = {}

        # TODO: future enhancement look for a global config file so that they don't need to be defined in each project
        logging.info(f'Looking for query_validator_config.py in {os.getcwd()}')
        if importlib.util.find_spec('query_validator_config') is not None:
            from query_validator_config import params as extra_params
            logging.info('Loading user defined params')

        params = {**get_default_params(), **extra_params}
        return params

    def render_templated_query(self, templated_query):
        # Convert the Jinja templated SQL to a valid query
        templated_query = templated_query.replace('params.', '')  # need this to get formatting correct
        t = Template(templated_query)
        return t.render(self.params)

    # todo finish
    def parameterize_sql(self, query):
        for k, v in self.params.items():
            query = query.replace(k, f'{{ params.v }}'
        return query

    def dry_run_query(self, query):
        try:
            job_config = bigquery.QueryJobConfig(dry_run=self.dry_run, use_query_cache=self.use_query_cache)

            # Start the query, passing in the extra configuration.
            query_job = self.bq_client.query(
                query,
                job_config=job_config,
            )  # Make an API request.

            # A dry run query completes immediately.
            total_bytes = query_job.total_bytes_processed
            logging.info("This query will process {} bytes.".format(total_bytes))

            byte = 1
            kilobyte = 1024
            megabyte = 1024 * 1024
            gigabyte = 1024 * 1024 * 1024
            terabyte = 1024 * 1024 * 1024

            if total_bytes > terabyte:
                rounded_total = round(total_bytes / terabyte, 2)
                byte_type = 'terabytes'
            elif total_bytes > gigabyte:
                rounded_total = round(total_bytes / terabyte, 2)
                byte_type = 'gigabytes'
            elif total_bytes > megabyte:
                rounded_total = round(total_bytes / terabyte, 2)
                byte_type = 'megabytes'
            elif total_bytes > kilobyte:
                rounded_total = round(total_bytes / terabyte, 2)
                byte_type = 'kilobytes'
            else:
                rounded_total = round(total_bytes / byte, 2)
                byte_type = 'bytes'

            message = f'This query will process {rounded_total} {byte_type}.'
            return True, message
        except Exception as e:
            error_string = str(e)
            error_minus_job_url = error_string.split('jobs?prettyPrint=false:')
            split_error = error_minus_job_url[1].split('\n\n')
            syntax_error = split_error[0]
            return False, syntax_error

    def validate_query(self, templated_query):
        try:
            formatted_query = self.render_templated_query(templated_query)
            querv_is_valid, message = self.dry_run_query(formatted_query)
            logging.info(f'Query is { "valid" if querv_is_valid else "invalid"}. {message}')
            return querv_is_valid, message
        except Exception as e:
            logging.error(e)
            return False

    def validate_query_from_file(self, file_path):
        try:
            # todo check if file exists
            if os.path.isfile(file_path):
                f = open(file_path, "r")
                templated_query = f.read()
                formatted_query = self.render_templated_query(templated_query)

                querv_is_valid, message = self.dry_run_query(formatted_query)
                logging.info(f'Query is {"valid" if querv_is_valid else "invalid"}. {message}')
                return querv_is_valid, message
            else:
                raise ValueError(f'Error: File does not exist: {file_path}')
        except Exception as e:
            logging.error(e)
            return False

    def auto_validate_query_from_file(self, file_path):
        try:
            _cached_stamp = 0
            while True:
                stamp = os.stat(file_path).st_mtime
                if stamp != _cached_stamp:
                    print(f'Loading...{RESET_SEQ}', end='                                                          \r')
                    _cached_stamp = stamp
                    f = open(file_path, "r")
                    templated_query = f.read()
                    formatted_query = self.render_templated_query(templated_query)
                    querv_is_valid, message = self.dry_run_query(formatted_query)

                    logging.info(f'Query is {"valid" if querv_is_valid else "invalid"}')

                    if querv_is_valid:
                        print_success(f'Valid query. {message}{RESET_SEQ}',
                                      end='                                                                         \r')
                    else:
                        print_failure(f'Invalid query. {message}{RESET_SEQ}',
                                      end='                                                                         \r')
        except Exception as e:
            logging.error(e)
            return False
