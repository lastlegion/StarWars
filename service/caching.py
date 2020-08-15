from threading import Thread
import time
import requests
import logging


class CachingService(Thread):
    def __init__(self, api_root_url, repository, ttl=3600):
        Thread.__init__(self)
        self._api_root_url = api_root_url
        self._repository = repository
        self._ttl = ttl

    def cache_films(self):
        try:
            response = requests.get(f'{self._api_root_url}/films')
            response = response.json()
            self._repository.update_films(response['results'])
        except Exception as e:
            logging.error(f'Failed to cache films {e}')
            print(f'Failed to cache films {e}')
        logging.info('Cached films')

    def cache_actors(self):
        try:
            response = requests.get(f'{self._api_root_url}/people')
            response = response.json()
            self._repository.update_actors(response['results'])
        except Exception as e:
            logging.error(f'Failed to cache actors {e}')
        logging.info('Cached actors')

    def clear_cache(self):
        try:
            self._repository.purge_db()
        except Exception as e:
            logging.error(f'Failed to clear cache {e}')
        logging.info('Cleared cache')

    def run(self):
        while True:
            self.clear_cache()
            self.cache_films()
            self.cache_actors()
            time.sleep(self._ttl)
