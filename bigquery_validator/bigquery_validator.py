import argparse
import importlib.util
import logging
import os
import warnings

from jinja2 import Template
from google.cloud import bigquery
warnings.filterwarnings("ignore", "Your application has authenticated using end user credentials")


class BigQueryValidator:

    def __init__(self):
        self.bq_client = bigquery.Client()
        self.params = self.load_params()
        parser = argparse.ArgumentParser()
        parser.add_argument('dir', nargs=1, default=None)
        args = parser.parse_args()
        print(args)

    def load_params(self):
        from bigquery_validator.config import default_params
        extra_params = {}

        # TODO: future enhancement look for a global config file so that they don't need to be defined in each project
        logging.info(f'Looking for query_validator_config.py in {os.getcwd()}')
        if importlib.util.find_spec('query_validator_config') is not None:
            from example.query_validator_config import params as extra_params
            logging.info('Loading user defined params')

        params = {**default_params, **extra_params}
        return params

    def validate_query(self, file_path):
        try:
            # Convert the Jinja templated SQL to a valid query
            f = open(file_path, "r")
            templated_query = f.read()

            templated_query = templated_query.replace('params.', '')  # need this to get formatting correct
            t = Template(templated_query)

            formatted_query = t.render(self.params)

            # Construct a BigQuery client object.
            job_config = bigquery.QueryJobConfig(dry_run=True, use_query_cache=False)

            # Start the query, passing in the extra configuration.
            # query_job =
            self.bq_client.query(
                formatted_query,
                job_config=job_config,
            )  # Make an API request.

            # A dry run query completes immediately.
            # todo: decide if we should print anything
            # print("This query will process {} bytes.".format(query_job.total_bytes_processed))
            return True
        except Exception as e:
            logging.error(e)
            return False
