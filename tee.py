import sys

class Tee(object):
    def __init__(self, name, mode):
        self.file = open(name, mode)
        self.stdout = sys.stdout
        self.stderr = sys.stderr
        sys.stdout = self
        sys.stderr = self

    def __del__(self):
        sys.stdout = self.stdout
        sys.stderr = self.stderr
        self.file.close()

    def write(self, data):
        self.stdout.write(data)
        self.stdout.flush()
        self.file.write(data)
        self.file.flush()

    def flush(*args):
        pass
