import argparse
import logging


def main():
    from bigquery_validator import BigQueryValidator, print_failure, print_success

    parser = argparse.ArgumentParser()
    parser.add_argument('params', nargs='*')

    args = parser.parse_args()
    function = args.params[0]
    param = args.params[1]

    bigquery_validator = BigQueryValidator()
    if function == 'render_templated_query':
        result = bigquery_validator.render_templated_query(param)
        print(result)
    # elif function == 'dry_run_query':
    #     valid_query = bigquery_validator.dry_run_query(param)
    #     result = f'Query is {valid_query}'
    elif function == 'validate_query':
        valid_query, message = bigquery_validator.validate_query(param)
        if valid_query:
            print_success(f'Valid query. {message}', end='\n')
        else:
            print_failure(f'Invalid query. {message}', end='\n')
    elif function == 'validate_query_from_file':
        valid_query = bigquery_validator.validate_query_from_file(param)
        if valid_query:
            print_success('Valid query')
        else:
            print_failure('Invalid query')
    elif function == 'auto_validate_query_from_file':
        bigquery_validator.auto_validate_query_from_file(param)
    else:
        raise ValueError('Invalid argument passed for function')
    # TODO: Accept arg for print to console or print to file


if __name__ == '__main__':
    logging.getLogger().setLevel(logging.WARNING)
    main()
