import requests
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class RabbitmqAPIUtils:

    headers = {'Content-type': 'application/json'}

    def __init__(self, protocol, host, port, user, password):
        self.user = user
        self.password = password
        self.url = '{}://{}:{}/api/'.format(protocol, host, port)

    def get_nodes(self):
        url_method = self.url
        url_method += 'nodes'
        logger.info("Call RabbitMQ api... {}".format(url_method))
        response = requests.get(url_method, auth=(self.user, self.password),
                                headers=self.headers, verify=False)
        return response

    def get_overview(self):
        url_method = self.url
        url_method += 'overview'
        logger.info("Call RabbitMQ api... {}".format(url_method))
        response = requests.get(url_method, auth=(self.user, self.password))
        return response

    def get_connections(self):
        url_method = self.url
        url_method += 'connections'
        logger.info("Call RabbitMQ api... {}".format(url_method))
        response = requests.get(url_method, auth=(self.user, self.password))
        return response

    def get_queues(self):
        url_method = self.url
        url_method += 'queues'
        logger.info("Call RabbitMQ api... {}".format(url_method))
        response = requests.get(url_method, auth=(self.user, self.password))
        return response

    def get_queues_per_vhost(self, vhost):
        url_method = self.url
        url_method += 'queues/{}'.format(vhost)
        logger.info("Call RabbitMQ api... {}".format(url_method))
        response = requests.get(url_method, auth=(self.user, self.password))
        return response

    def get_exchanges(self):
        url_method = self.url
        url_method += 'exchanges'
        logger.info("Call RabbitMQ api... {}".format(url_method))
        response = requests.get(url_method, auth=(self.user, self.password))
        return response

    def get_exchanges_per_vhost(self, vhost):
        url_method = self.url
        url_method += 'exchanges/{}'.format(vhost)
        logger.info("Call RabbitMQ api... {}".format(url_method))
        response = requests.get(url_method, auth=(self.user, self.password))
        return response
