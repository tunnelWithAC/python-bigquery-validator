import json
import logging
import os
from pathlib import Path
import warnings

from google.cloud import bigquery
from jinja2 import Template

from bigquery_validator.bigquery_validator_util import get_default_params, print_success, print_failure, \
    read_sql_file, RESET_SEQ

warnings.filterwarnings("ignore", "Your application has authenticated using end user credentials")


class BigQueryValidator:
    """Convert Jinja templated sql query to a regularly formatted query and validate it using BigQuery dry run.
    Queries can be inputted as a string or by passing the file path to a sql file.
    """

    def __init__(self,
                 use_query_cache=False):
        self.bq_client = bigquery.Client()
        self.params = self.load_params()
        self.use_query_cache = use_query_cache


    def load_params(self):
        """Load default params"""
        params = get_default_params()

        # load params from global config
        def load_config_from_file(config_path):
            if os.path.isfile(config_path):
                try:
                    f = open(config_path, "r")
                    config_file_content = f.read()
                    config_params = json.loads(config_file_content)
                    logging.info(f'Loaded params from global config file: {config_path}')
                    return config_params
                except Exception as e:
                    logging.error('Error reading params from global config file. No global params will be loaded.')
                    return {}
            else:
                return {}

        home = str(Path.home())
        global_config_path = os.path.join(home, '.python_bigquery_validator/config.json')
        global_config_params = load_config_from_file(global_config_path)
        params = {**params, **global_config_params}

        # load params from local config
        local_config_path = os.path.join(os.getcwd(), 'bq_validator_config.json')
        local_config_params = load_config_from_file(local_config_path)
        params = {**params, **local_config_params}
        return params

    def render_templated_query(self, templated_query):
        """Convert the Jinja templated SQL to a valid query"""
        templated_query = templated_query.replace('params.', '')  # need this to get formatting correct
        t = Template(templated_query)
        rendered_query = t.render(self.params)
        rendered_query = rendered_query.replace('\n', ' ')
        return rendered_query

    def render_templated_query_from_file(self, file_path):
        """Convert the Jinja templated SQL to a valid query"""
        templated_query = read_sql_file(file_path)
        return self.render_templated_query(templated_query)

    # # todo finish
    # def parameterize_sql(self, query):
    #     default_params = get_default_params()
    #     for k, v in self.params.items():
    #         # default params do not require 'param.' prefix
    #         if k in default_params:
    #             query = query.replace(f'{{{{  {k} }}}}', v)
    #         else:
    #             query = query.replace(f'{{{{ params.{k} }}}}', v)
    #     return query

    def dry_run_query(self, query):
        """Run a BigQuery query with dry_run set to True.
        If the query succeeds it is valid and will return the estimated processing bytes required for the query.
        An exception will be thrown if the query is not valid.
        """
        try:
            job_config = bigquery.QueryJobConfig(dry_run=True, use_query_cache=self.use_query_cache)

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
            terabyte = 1024 * 1024 * 1024 * 1024

            if total_bytes > terabyte:
                rounded_total = round(total_bytes / terabyte, 2)
                byte_type = 'TB'
            elif total_bytes > gigabyte:
                rounded_total = round(total_bytes / gigabyte, 2)
                byte_type = 'GB'
            elif total_bytes > megabyte:
                rounded_total = round(total_bytes / megabyte, 2)
                byte_type = 'MB'
            elif total_bytes > kilobyte:
                rounded_total = round(total_bytes / kilobyte, 2)
                byte_type = 'KB'
            else:
                rounded_total = round(total_bytes / byte, 2)
                byte_type = 'B'

            message = f'This query will process {rounded_total} {byte_type}.'
            return True, message
        except Exception as e:
            error_string = str(e)
            error_minus_job_url = error_string.split('jobs?prettyPrint=false:')
            split_error = error_minus_job_url[1].split('\n\n')
            syntax_error = split_error[0]
            return False, syntax_error


    # TODO: validate output of query
    # Stolen from Apache Beam
    # https://github.com/apache/beam/blob/87e11644c44a4c677ec2faa78f50cdffbb33605a/sdks/python/apache_beam/io/gcp/tests/bigquery_matcher.py
    # @retry.with_exponential_backoff(
    #       num_retries=MAX_RETRIES,
    #       retry_filter=retry_on_http_timeout_and_value_error)
    #   def run_query(self):
    #     """Run Bigquery query with retry if got error http response"""
    #     _LOGGER.info('Attempting to perform query %s to BQ', self.query)
    #     # Create client here since it throws an exception if pickled.
    #     bigquery_client = bigquery.Client(self.project)
    #     query_job = bigquery_client.query(self.query)
    #     rows = query_job.result(timeout=60)
    #     return [row.values() for row in rows]

    def validate_query(self, templated_query):
        """Check if query passed as parameter is valid. If the query contains any Jinja templated params they will
        be converted to the associated param value if one exists.

        Parameters:
        templated_query (str): SQL query to be validated
        """
        try:
            formatted_query = self.render_templated_query(templated_query)
            querv_is_valid, message = self.dry_run_query(formatted_query)
            logging.info(f'Query is { "valid" if querv_is_valid else "invalid"}. {message}')
            return querv_is_valid, message
        except Exception as e:
            logging.error(e)
            return False

    def validate_query_from_file(self, file_path):
        """Same as validate_query() but reads query from a file rather than accepting it as a param

        Parameters:
        file_path (str): Path to the sql file on the file system
        """
        try:
            # todo check if file ends with .sql
            if os.path.isfile(file_path):
                templated_query = read_sql_file(file_path)
                return self.validate_query(templated_query)
            else:
                raise ValueError(f'Error: File does not exist: {file_path}')
        except Exception as e:
            logging.error(e)
            return False


    def auto_validate_query_from_file(self, file_path):
        """Continuously monitor a sql file and automatically validate the sql on every saved change to the file.
        Any Jinja templated params will be automatically parsed on update.

        Parameters:
        file_path (str): Path to the sql file on the file system
       """
        try:
            _cached_stamp = 0
            while True:
                # TODO monitor query validator config for changes too
                stamp = os.stat(file_path).st_mtime
                if stamp != _cached_stamp:
                    print(f'Loading...{RESET_SEQ}', end='                                                          \r')
                    _cached_stamp = stamp
                    templated_query = read_sql_file(file_path)
                    formatted_query = self.render_templated_query(templated_query)
                    querv_is_valid, message = self.dry_run_query(formatted_query)

                    logging.info(f'Query is {"valid" if querv_is_valid else "invalid"}')

                    if querv_is_valid:
                        # Extra white space here is quick workaround to remove all text from last message
                        # when the previous message length exceeds the new message length
                        print_success(f'Valid query. {message}{RESET_SEQ}',
                                      end='                                                                         \r')
                    else:
                        print_failure(f'Invalid query. {message}{RESET_SEQ}',
                                      end='                                                                         \r')
        except Exception as e:
            logging.error(e)
            return False
