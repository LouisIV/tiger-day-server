import json


class JsonConfig():
    def __init__(self, filename=False, json=False):
        self.filename = filename
        self.working_json = json

    def __get_file(self):
        with open(self.filename, 'r') as f:
            return json.load(f)

    def __get_config(self):
        if self.filename:
            return self.__get_file()
        elif self.working_json:
            return self.working_json
        else:
            raise RuntimeError("You need to specify a file first!")

    def __write(self, json):
        if self.filename:
            with open(self.filename, 'w') as f:
                json.dump(config, f)
        elif working_json:
            working_json = json
        else:
            raise RuntimeError("You need to specify a file first!")

    def dump(self):
        if self.filename:
            return self.__get_file()
        elif self.working_json:
            return self.working_json
        else:
            raise RuntimeError("Nothing to dump!")

    def load(self, json):
        self.filename = False
        self.working_json = json

    def clear(self):
        self.filename = False
        self.working_json = None
        self.working_json = False

    def get(self, key):
        config = self.__get_config()
        if key in config:
            return config[key]
        return False

    def set(self, key, value):
        config = self.__get_config()
        config[key] = value
        self.__write(config)

    def append(self, key, value, asString=False, stringSep=','):
        old = self.get(key, value)
        if old:
            if asString:
                old += stringSep + value
            else:
                old.append(value)
            self.set(key, old)
        else:
            raise KeyError("Key does not exist.")


