class JsonObject:
    json = {}

    def put(self, key, value):
        self.json[key] = value

    def get(self, key):
        return self.json.get(key)

    def to_string(self):
        return str(self.json)
