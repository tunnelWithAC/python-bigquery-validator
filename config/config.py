from datetime import datetime, timedelta


class Config:

    def __init__(self):
        self.today = datetime.now()
        self.yesterday = self.today - timedelta(days=1)

    def toJSON(self):
        import json
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)

    def datetime_to_ds(self, dt):
        return dt.strftime('%Y-%m-%d')

    def datetime_to_ds_nodash(self, dt):
        return dt.strftime('%Y-%m-%d')

    def get_default_params(self):
        return {
            'ds': self.datetime_to_ds(self.yesterday),
            'ds_nodash': self.datetime_to_ds_nodash(self.yesterday),
            'tomorrow_ds_nodash': self.datetime_to_ds_nodash(self.today),
            'tomorrow_ds': self.datetime_to_ds(self.today)
        }
