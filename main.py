import logging

from absl import app, flags
from flask import Flask
from gevent.pywsgi import WSGIServer

from repository import StarWarsRepository
from service import StarWarsService, CachingService
from controller import StarWarsController

logging.basicConfig(format='%(asctime)s,%(msecs)d %(levelname)-8s\
                    [%(filename)s:%(lineno)d] %(message)s',
                    datefmt='%Y-%m-%d:%H:%M:%S',
                    level=logging.INFO)

FLAGS = flags.FLAGS

flags.DEFINE_string('db_info',
                    './star_wars.db',
                    'Name and Path of the cache')
flags.DEFINE_string('api_root_url',
                    'https://swapi.dev/api',
                    'API root url')
flags.DEFINE_integer('port',
                     8080,
                     'Port to run proxy on')
flags.DEFINE_integer('cache_ttl',
                     3600,
                     'Cache Time to Live')


def main(argv):
    logging.info('Starting star wars proxy service...')
    repository = StarWarsRepository(db=FLAGS.db_info)
    service = StarWarsService(repository=repository)
    controller = StarWarsController(service=service)

    caching_service = CachingService(api_root_url=FLAGS.api_root_url,
                                     repository=repository,
                                     ttl=FLAGS.cache_ttl)
    app = Flask(__name__)
    app.register_blueprint(controller.get_bluprint())

    caching_service.daemon = True
    caching_service.start()
    http_server = WSGIServer(('', FLAGS.port), app)
    http_server.serve_forever()


if __name__ == '__main__':
    app.run(main)
