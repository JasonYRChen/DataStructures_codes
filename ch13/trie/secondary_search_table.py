# 'get', 'add' method should be included

class Dictionary(dict):
    def __bool__(self):
        for key in self.keys():
            return True
        return False

    def add(self, key, value):
        self[key] = value
