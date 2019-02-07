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

        return conditions

    def load_report_config(self):
        self.log.info('Loading report configurations....')
        with open("./config/report-config.yml", 'r') as ymlfile:
            server_config = yaml.load(ymlfile)

        report = server_config['report']
        location = report['location']
        self.log.info('location: {}'.format(location))
        general_report = report['general-report']
        self.log.info('general-report: {}'.format(general_report))
        vhost_report = report['vhost-report']
        self.log.info('vhost-report: {}'.format(vhost_report))

        report_config = dict()
        report_config['location'] = location
        report_config['general-report'] = general_report
        report_config['vhost-report'] = vhost_report

        return report_config
