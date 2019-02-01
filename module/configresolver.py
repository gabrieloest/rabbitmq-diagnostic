import yaml

SERVER_CONFIG_PATH = "/config/server-config.yml"
CONDITIONS_CONFIG_PATH = "/config/conditions-config.yml"


class ConfigResolver:

    def __init__(self, logger):
        self.log = logger

    def load_server_config(self):
        self.log.info('Loading server configurations....')
        with open("./config/server-config.yml", 'r') as ymlfile:
            server_config = yaml.load(ymlfile)

        rabbitmq = server_config['rabbitmq']
        host = rabbitmq['host']
        self.log.info('host: {}'.format(host))
        user = rabbitmq['user']
        self.log.info('user: {}'.format(user))
        password = rabbitmq['password']
        self.log.info('password: {}'.format(password))

        server = dict()
        server['host'] = host
        server['user'] = user
        server['password'] = password

        return server

    def load_conditions_config(self):
        self.log.info('Loading conditions configurations....')
        with open("./config/conditions-config.yml", 'r') as ymlfile:
            server_config = yaml.load(ymlfile)

        metrics = server_config['conditions']
        exchange = metrics['exchange']
        node = metrics['node']
        connection = metrics['connection']
        queue = metrics['queue']

        conditions = dict()
        conditions['messages_published_in'] = exchange['messages_published_in']
        conditions['messages_published_out'] = exchange['messages_published_out']
        conditions['messages_unroutable'] = exchange['messages_unroutable']
        conditions['nodes_running'] = node['nodes_running']
        conditions['file_descriptors_used'] = node['file_descriptors_used']
        conditions['file_descriptors_used_as_sockets'] = node['file_descriptors_used_as_sockets']
        conditions['disk_space_used'] = node['disk_space_used']
        conditions['memory_used'] = node['memory_used']
        conditions['consumers_connected'] = connection['consumers_connected']
        conditions['open_connections'] = connection['open_connections']
        conditions['data_rates'] = connection['data_rates']
        conditions['depth'] = queue['depth']
        conditions['messages_unacknowledged'] = queue['messages_unacknowledged']
        conditions['messages_ready'] = queue['messages_ready']
        conditions['messages_rate'] = queue['messages_rate']
        conditions['messages_persistent'] = queue['messages_persistent']
        conditions['messages_bytes_persistent'] = queue['messages_bytes_persistent']
        conditions['messages_bytes_ram'] = queue['messages_bytes_ram']
        conditions['consumers_connected'] = queue['consumers_connected']

        return conditions
