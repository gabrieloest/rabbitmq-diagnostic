import logging
import os
from itertools import groupby
import configresolver
import rabbitmq_api_utils
import nodes_diagnostic
import queues_diagnostic

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def write_header(diagnostic, text):
    diagnostic.write("\r\n")
    diagnostic.write(">>>>>>>>>>> {}\r\n".format(text))
    diagnostic.write("\r\n")


def write_item_header(diagnostic, text):
    diagnostic.write("******************************************\r\n")
    diagnostic.write("*******  {}\r\n".format(text))
    diagnostic.write("******************************************\r\n")


# Loading server configuration
config = configresolver.ConfigResolver(logger)
server_config = config.load_server_config()

rmq_utils = rabbitmq_api_utils.RabbitmqAPIUtils(server_config['host'],
                                                server_config['user'],
                                                server_config['password'])

# Loading performance metrics conditions
conditions = config.load_conditions_config()

if not os.path.exists('report'):
    os.makedirs('report')
diagnostic = open('report/diagnostic.txt', 'w+')

write_header(diagnostic, 'CONFIGURED CONDITIONS')
for condition, value in conditions.items():
    diagnostic.write("- {} = {}\r\n".format(condition, value))

# Consulting overview information
overview = list(rmq_utils.get_overview().json())

# Consulting queues information
queues = list(rmq_utils.get_queues().json())

groups = groupby(queues, lambda queue: queue['vhost'])
queues_diagnostic = queues_diagnostic.QueuesDiagnostic(logger)

# Checking queues metrics
write_header(diagnostic, 'QUEUES PERFOMANCE METRICS')
for vhost, queues in groups:
    write_item_header(diagnostic, 'VHOST: {}'.format(vhost))
    queues = list(queues)
    queues_diagnostic.no_consumers_queues_report(queues, conditions,
                                                 diagnostic)
    queues_diagnostic.high_ready_messages_queues(queues, conditions,
                                                 diagnostic)
    queues_diagnostic.high_messages_unacknowledged_queues(queues, conditions,
                                                          diagnostic)

# Consulting nodes information
nodes = list(rmq_utils.get_nodes().json())
nodes_diagnostic = nodes_diagnostic.NodesDiagnostic(logger)

# Checking alert's for each node
write_header(diagnostic, 'NODES PERFOMANCE METRICS')
for node in nodes:
    write_item_header(diagnostic, 'Node: {}'.format(node['name']))
    nodes_diagnostic.alert_file_description(node, conditions, diagnostic)
    nodes_diagnostic.alert_files_description_as_sockets(node, conditions,
                                                        diagnostic)
    nodes_diagnostic.alert_disk_free(node, conditions, diagnostic)
    nodes_diagnostic.alert_mem_free(node, conditions, diagnostic)
    nodes_diagnostic.alert_erlang_process(node, conditions, diagnostic)
    diagnostic.write("\r\n")

diagnostic.close()
