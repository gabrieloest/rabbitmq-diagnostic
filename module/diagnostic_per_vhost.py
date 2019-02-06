import logging
from itertools import groupby
import config_resolver
import rabbitmq_api_utils
import exchanges_diagnostic
import queues_diagnostic
import report_utils

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Loading server configuration
config = config_resolver.ConfigResolver(logger)
server_config = config.load_server_config()

rmq_utils = rabbitmq_api_utils.RabbitmqAPIUtils(server_config['host'],
                                                server_config['user'],
                                                server_config['password'])

# Loading performance metrics conditions
conditions = config.load_conditions_config()


def create_report(file_name):
    report = report_utils.ReportUtils(logger, 'report', file_name)
    report.write_header('CONFIGURED CONDITIONS')
    for condition, value in conditions.items():
        report.write_line("- {} = {}\r\n".format(condition, value))
    return report


# Consulting exchange information
exchanges = list(rmq_utils.get_exchanges().json())

exchanges_diagnostic = exchanges_diagnostic.ExchangesDiagnostic(logger)
vhost_exchanges = dict((k, list(g)) for k, g in groupby(exchanges, lambda exchange: exchange['vhost']))

# Consulting queues information
queues = list(rmq_utils.get_queues().json())

vhost_queues = dict((k, list(g)) for k, g in groupby(queues, lambda queue: queue['vhost']))
queues_diagnostic = queues_diagnostic.QueuesDiagnostic(logger)

# Checking queues metrics
for vhost, queues in vhost_queues.items():
    report = create_report('diagnostic{}.txt'.format(vhost.replace('/', '-')))
    report.write_item_header('VHOST: {}'.format(vhost))

    report.write_header('EXCHANGES PERFOMANCE METRICS')
    exchanges = list(vhost_exchanges.get(vhost))

    report.write_line(exchanges_diagnostic.alert_without_bindings(exchanges))
    report.write_line(exchanges_diagnostic.check_messages_in_not_out(exchanges))
    report.write_line(exchanges_diagnostic.check_messages_in_greater_than_out(exchanges))

    report.write_header('PERFOMANCE METRICS')
    queues = list(queues)
    report.write_line(queues_diagnostic.no_consumers_queues_report(queues, conditions))
    report.write_line(queues_diagnostic.high_ready_messages_queues(queues, conditions))
    report.write_line(queues_diagnostic.high_messages_unacknowledged_queues(queues, conditions))
    report.close()
