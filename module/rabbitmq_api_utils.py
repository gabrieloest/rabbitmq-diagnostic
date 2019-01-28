import requests
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class RabbitmqAPIUtils:

    headers = {'Content-type': 'application/json'}

    def __init__(self, host, user, password):
        self.user = user
        self.password = password
        self.url = 'http://{}/api/'.format(host)

    def get_nodes(self):
        url_method = self.url
        url_method += 'nodes'
        logger.info("Call RabbitMQ api... {}".format(url_method))
        r = requests.get(url_method, auth=(self.user, self.password))
        return r

    def get_overview(self):
        logger.info("Call RabbitMQ api... {}".format(self.url))
        url_method = self.url
        url_method += 'overview'
        r = requests.get(url_method, auth=(self.user, self.password))
        return r

    def get_connections(self):
        logger.info("Call RabbitMQ api... {}".format(self.url))
        url_method = self.url
        url_method += 'connections'
        r = requests.get(url_method, auth=(self.user, self.password))
        return r

    def get_queues(self):
        logger.info("Call RabbitMQ api... {}".format(self.url))
        url_method = self.url
        url_method += 'queues'
        r = requests.get(url_method, auth=(self.user, self.password))
        return r