import logging
from itertools import groupby
import configresolver
import rabbitmq_api_utils
import nodes_diagnostic
import queues_diagnostic
import report_utils

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Loading server configuration
config = configresolver.ConfigResolver(logger)
server_config = config.load_server_config()

rmq_utils = rabbitmq_api_utils.RabbitmqAPIUtils(server_config['host'],
                                                server_config['user'],
                                                server_config['password'])

report = report_utils.ReportUtils(logger, 'report', 'diagnostic.txt')

# Loading performance metrics conditions
conditions = config.load_conditions_config()

report.write_header('CONFIGURED CONDITIONS')
for condition, value in conditions.items():
    report.write_line("- {} = {}\r\n".format(condition, value))

# Consulting overview information
overview = list(rmq_utils.get_overview().json())

# Consulting queues information
queues = list(rmq_utils.get_queues().json())

groups = groupby(queues, lambda queue: queue['vhost'])
queues_diagnostic = queues_diagnostic.QueuesDiagnostic(logger)

# Checking queues metrics
report.write_header('QUEUES PERFOMANCE METRICS')
for vhost, queues in groups:
    report.write_item_header('VHOST: {}'.format(vhost))
    queues = list(queues)
    report.write_line(queues_diagnostic.no_consumers_queues_report(queues, conditions))
    report.write_line(queues_diagnostic.high_ready_messages_queues(queues, conditions))
    report.write_line(queues_diagnostic.high_messages_unacknowledged_queues(queues, conditions))

# Consulting nodes information
nodes = list(rmq_utils.get_nodes().json())
nodes_diagnostic = nodes_diagnostic.NodesDiagnostic(logger)

# Checking alert's for each node
report.write_header('NODES PERFOMANCE METRICS')
for node in nodes:
    report.write_item_header('Node: {}'.format(node['name']))
    report.write_line(nodes_diagnostic.alert_file_description(node, conditions))
    report.write_line(nodes_diagnostic.alert_files_description_as_sockets(node, conditions))
    report.write_line(nodes_diagnostic.alert_disk_free(node, conditions))
    report.write_line(nodes_diagnostic.alert_mem_free(node, conditions))
    report.write_line(nodes_diagnostic.alert_erlang_process(node, conditions))
    report.write_line("\r\n")

report.close()
