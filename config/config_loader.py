import json


class UnknownConfigException(Exception):
    def __init__(self, msg):
        super.__init__(msg)


class ConfigLoader:
    def __init__(self, config_file):
        self.config_file = config_file
        self.config = dict()

    def load_config(self):
        with open(self.config_file, 'r') as f:
            self.config = json.loads(f.read())

    def get_config(self, key):
        if key in self.config.keys():
            return self.config[key]
        else:
            raise UnknownConfigException(f'Configuration value with a key of {key} not found')
