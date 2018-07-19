from pymongo import MongoClient


class MongoDatabase:
    """Borg Pattern to ensure that all instances will share the same state"""
    __shared_state = {}

    def __init__(self):
        self.__dict__ = self.__shared_state
        self._database = MongoClient()

    def instance(self):
        return self._database.photo_gallery
