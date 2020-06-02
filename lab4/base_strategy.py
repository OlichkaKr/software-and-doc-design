import abc
import redis
import read_config


class BaseStrategy:
    __metaclass__ = abc.ABCMeta

    def __init__(self, url=None, filename=None):
        self.dataset_url = url
        self.dataset_filename = filename

        self.redis_client = redis.StrictRedis(host='nulplabs.redis.cache.windows.net', port=6380,
                                              password='cu+R0fTVjSqJxwI3YRCoH4AFK2AkfU0bJmkR3sVcUy4=', ssl=True)

    @abc.abstractmethod
    def execute(self):
        pass