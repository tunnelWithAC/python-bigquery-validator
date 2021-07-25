from datetime import datetime, timedelta

today = datetime.now()
yesterday = datetime.now() - timedelta(days=1)


def datetime_to_ds(dt):
    return dt.strftime('%Y-%m-%d')


def datetime_to_ds_nodash(dt):
    return dt.strftime('%Y%m%d')


def get_default_params():
    return {
        'ds': datetime_to_ds(yesterday),
        'ds_nodash': datetime_to_ds_nodash(yesterday),
        'tomorrow_ds_nodash': datetime_to_ds_nodash(today),
        'tomorrow_ds': datetime_to_ds(today)
    }
