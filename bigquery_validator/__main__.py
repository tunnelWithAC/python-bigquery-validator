import argparse


def main():
    from bigquery_validator import BigQueryValidator
    from config import Config

    parser = argparse.ArgumentParser()
    parser.add_argument('params', nargs='*')

    args = parser.parse_args()
    function = args.params[0]
    param = args.params[1]

    bq_config = Config()
    bigquery_validator = BigQueryValidator(bq_config)
    if function == 'render_templated_query':
        bigquery_validator.render_templated_query(param)
    elif function == 'dry_run_query':
        bigquery_validator.dry_run_query(param)
    elif function == 'validate_query':
        print('vw')
        bigquery_validator.validate_query(param)
    elif function == 'validate_query_from_file':
        bigquery_validator.validate_query_from_file(param)
    else:
        raise ValueError('Invalid argument passed for function')


if __name__ == '__main__':
    main()
