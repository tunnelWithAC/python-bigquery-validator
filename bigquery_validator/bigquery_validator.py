import argparse
import importlib.util
import logging
import os
import warnings

from google.cloud import bigquery
from jinja2 import Template

logging.basicConfig(level=os.environ.get("LOGLEVEL", "INFO"))
warnings.filterwarnings("ignore", "Your application has authenticated using end user credentials")


class BigQueryValidator:

    def __init__(self,
                 dry_run=True,
                 use_query_cache=False):
        self.bq_client = bigquery.Client()
        self.params = self.load_params()
        self.dry_run = dry_run
        self.use_query_cache = use_query_cache

    def load_params(self):
        from bigquery_validator.config import default_params

        extra_params = {}

        # TODO: future enhancement look for a global config file so that they don't need to be defined in each project
        logging.info(f'Looking for query_validator_config.py in {os.getcwd()}')
        if importlib.util.find_spec('query_validator_config') is not None:
            from query_validator_config import params as extra_params
            logging.info('Loading user defined params')

        params = {**default_params, **extra_params}
        return params

    def render_templated_query(self, templated_query):
        # Convert the Jinja templated SQL to a valid query
        templated_query = templated_query.replace('params.', '')  # need this to get formatting correct
        t = Template(templated_query)
        return t.render(self.params)

    # def parameterize_sql(self, query)

    def dry_run_query(self, query):
        # Construct a BigQuery client object.
        job_config = bigquery.QueryJobConfig(dry_run=self.dry_run, use_query_cache=self.use_query_cache)

        # Start the query, passing in the extra configuration.
        query_job = self.bq_client.query(
            query,
            job_config=job_config,
        )  # Make an API request.

        # A dry run query completes immediately.
        logging.info("This query will process {} bytes.".format(query_job.total_bytes_processed))
        return True

    def validate_query(self, templated_query):
        try:
            formatted_query = self.render_templated_query(templated_query)
            querv_is_valid = self.dry_run_query(formatted_query)
            logging.info(f'Query is { "valid" if querv_is_valid else "invalid"}')
            return querv_is_valid
        except Exception as e:
            logging.error(e)
            return False

    def validate_query_from_file(self, file_path):
        try:
            f = open(file_path, "r")
            templated_query = f.read()
            formatted_query = self.render_templated_query(templated_query)
            return self.dry_run_query(formatted_query)
        except Exception as e:
            logging.error(e)
            return False


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--function', type=str, help='Function to be called', required=True)
    parser.add_argument('-p', '--param', type=str, help='Parameter for function', required=True)
    args = parser.parse_args()
    function = args.function
    param = args.param

    bigquery_validator = BigQueryValidator()
    if function == 'render_templated_query':
        bigquery_validator.render_templated_query('select date("{{ params.date }}") as date')
    elif function == 'dry_run_query':
        bigquery_validator.dry_run_query('select true')
    elif function == 'validate_query':
        print('vw')
        bigquery_validator.validate_query('select true')
    elif function == 'validate_query_from_file':
        bigquery_validator.validate_query('./valid_query.sql')
    else:
        raise ValueError('Invalid argument passed for function')
