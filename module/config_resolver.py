import yaml

SERVER_CONFIG_PATH = "./config/server-config.yml"
CONDITIONS_CONFIG_PATH = "./config/conditions-config.yml"
REPORTS_CONFIG_PATH = "./config/report-config.yml"


class ConfigResolver:

    def __init__(self, logger):
        self.log = logger

    def log_configurations(self, configurations):
        for key, value in configurations.items():
            self.log.info('{}: {}'.format(key, value))

    def load_server_config(self):
        self.log.info('Loading server configurations....')
        with open(SERVER_CONFIG_PATH, 'r') as ymlfile:
            server_config = yaml.load(ymlfile)

        rabbitmq = server_config['rabbitmq']
        self.log_configurations(rabbitmq)

        return rabbitmq

    def load_metrics_config(self):
        self.log.info('Loading exchanges configurations....')
        with open("./config/conditions-config.yml", 'r') as ymlfile:
            server_config = yaml.load(ymlfile)

        return server_config['conditions']

    def load_exchanges_config(self):
        metrics = self.load_metrics_config()
        self.log.info('Loading exchanges configurations....')
        exchange = metrics['exchange']

        return exchange

    def load_nodes_config(self):
        metrics = self.load_metrics_config()
        self.log.info('Loading nodes configurations....')
        node = metrics['node']

        return node

    def load_connections_config(self):
        metrics = self.load_metrics_config()
        self.log.info('Loading connections configurations....')
        connection = metrics['connection']

        return connection

    def load_queues_config(self):
        metrics = self.load_metrics_config()
        self.log.info('Loading queues configurations....')
        queue = metrics['queue']

        return queue

    def load_report_config(self):
        self.log.info('Loading report configurations....')
        with open(REPORTS_CONFIG_PATH, 'r') as ymlfile:
            server_config = yaml.load(ymlfile)

        report = server_config['report']
        self.log_configurations(report)

        return report

"""    def load_metrics_config(self):
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
        conditions['file_descriptors_used_warn'] = node['file_descriptors_used_percent_warn']
        conditions['file_descriptors_used_as_sockets_warn'] = node['file_descriptors_used_as_sockets_percent_warn']
        conditions['disk_space_used_warn'] = node['disk_space_used_percent_warn']
        conditions['memory_used_warn'] = node['memory_used_percent_warn']
        conditions['erlang_process_warn'] = node['erlang_process_percent_warn']
        conditions['file_descriptors_used_critical'] = node['file_descriptors_used_percent_critical']
        conditions['file_descriptors_used_as_sockets_critical'] = node['file_descriptors_used_as_sockets_percent_critical']
        conditions['disk_space_used_critical'] = node['disk_space_used_percent_critical']
        conditions['memory_used_critical'] = node['memory_used_percent_critical']
        conditions['erlang_process_critical'] = node['erlang_process_percent_critical']

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

        return conditions"""
