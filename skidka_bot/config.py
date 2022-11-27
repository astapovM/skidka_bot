import os
from dotenv import load_dotenv
dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

class Config(object):
    def __init__(self):
        self._endpoint = os.getenv("YDB_ENDPOINT")
        self._database = os.getenv("YDB_DATABASE")
        self._path = os.getenv("YDB_TABLE")
        self._token = os.getenv("TOKEN")

    @property
    def endpoint(self):
        return self._endpoint

    @property
    def database(self):
        return self._database

    @property
    def path(self):
        return self._path

    @property
    def full_path(self):
        return os.path.join(self.database, self._path)

    @property
    def token(self):
        return self._token


configuration = Config()