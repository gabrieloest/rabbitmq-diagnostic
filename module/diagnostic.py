import logging
import os
from itertools import groupby
import configresolver
import rabbitmq_api_utils

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def no_consumers_queues_report(queues, conditions, diagnostic):
    temp_queues = queues
    queues_no_conumers = list(filter(lambda item: (
                                     item['consumers'] <
                                     conditions['consumers_connected']),
                                     temp_queues))

    diagnostic.write('{} queue(s) without consumers\r\n'
                     .format(len(queues_no_conumers)))
    for item in queues_no_conumers:
        diagnostic.write("Queue {} of vhost {} does not have "
                         "any consumer.\r\n"
                         .format(item['name'], item['vhost']))
    diagnostic.write('\r\n')


def high_ready_messages_queues(queues, conditions, diagnostic):
    high_messages = list(filter(lambda item: (
                                item['messages_ready'] >
                                conditions['messages_ready']),
                                queues))

    diagnostic.write('{} queue(s) with high number of ready '
                     'messages\r\n'.format(len(high_messages)))
    for item in high_messages:
        diagnostic.write("Queue {} of vhost {} has a high number of "
                         "ready messages: {}.\r\n".format(item['name'],
                                                      item['vhost'],
                                                      item['messages_ready']))
    diagnostic.write('\r\n')


def high_messages_unacknowledged_queues(queues, conditions, diagnostic):
    messages_unacknowledged = list(filter(lambda item: (
                                          item['messages_unacknowledged'] >
                                          conditions['messages_unacknowledged']),
                                          queues))

    diagnostic.write('{} queue(s) with high number of messages '
                     'unacknowledged\r\n'.format(len(messages_unacknowledged)))
    for item in messages_unacknowledged:
        diagnostic.write("Queue {} of vhost {} has a high number of "
                         "messages unacknowledged: {}.\r\n"
                         .format(item['name'], item['vhost'],
                                 item['messages_unacknowledged']))
    diagnostic.write('\r\n')


def check_alert(actual_value, total_value, warn_value,
                critical_value, message):
    percent_value = round((actual_value * 100) / total_value, 2)

    if(percent_value > warn_value and
       percent_value < critical_value):
        message += ' : {}% - Warning\r\n'.format(percent_value)
    elif(percent_value > critical_value):
        message += ' : {}% - Critical\r\n'.format(percent_value)
    else:
        message += ' : {}% - OK\r\n'.format(percent_value)

    return message


def alert_file_description(node, conditions, diagnostic):
    fd_used = node['fd_used']
    fd_total = node['fd_total']
    fd_result = 'File Descriptors Alert'

    message = check_alert(fd_used, fd_total,
                          conditions['file_descriptors_used_warn'],
                          conditions['file_descriptors_used_critical'],
                          fd_result)
    diagnostic.write(message)


def alert_files_description_as_sockets(node, conditions, diagnostic):
    sd_used = node['sockets_used']
    sd_total = node['sockets_total']
    sd_result = 'File Descriptors as Sockets Alert'

    message = check_alert(sd_used, sd_total,
                          conditions['file_descriptors_used_as_sockets_warn'],
                          conditions['file_descriptors_used_as_sockets_critical'],
                          sd_result)

    diagnostic.write(message)


def alert_disk_free(node, conditions, diagnostic):
    disk_free = node['disk_free']
    disk_free_limit = node['disk_free_limit']
    message = 'Disk Free Limit is {} actual value is {}: ' .format(disk_free_limit, disk_free)

    disk_free_limit_critical = disk_free_limit / 2

    if(disk_free < disk_free_limit and disk_free > disk_free_limit_critical):
        message += ' Warning\r\n'
    elif(disk_free < disk_free_limit_critical):
        message += ' Critial\r\n'
    else:
        message += ' OK\r\n'

    diagnostic.write(message)


def alert_mem_free(node, conditions, diagnostic):
    mem_used = node['mem_used']
    mem_limit = node['mem_limit']
    mem_result = 'Mem Free Alert'

    message = check_alert(mem_used, mem_limit,
                          conditions['memory_used_warn'],
                          conditions['memory_used_critical'],
                          mem_result)

    diagnostic.write(message)


def alert_erlang_process(node, conditions, diagnostic):
    proc_used = node['proc_used']
    proc_total = node['proc_total']
    proc_result = 'Erlang processes used Alert '

    message = check_alert(proc_used, proc_total,
                          conditions['erlang_process_warn'],
                          conditions['erlang_process_critical'],
                          proc_result)

    diagnostic.write(message)


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

# Checking queues metrics
write_header(diagnostic, 'QUEUES PERFOMANCE METRICS')
for vhost, queues in groups:
    write_item_header(diagnostic, 'VHOST: {}'.format(vhost))
    queues = list(queues)
    no_consumers_queues_report(queues, conditions, diagnostic)
    high_ready_messages_queues(queues, conditions, diagnostic)
    high_messages_unacknowledged_queues(queues, conditions, diagnostic)

# Consulting nodes information
nodes = list(rmq_utils.get_nodes().json())

# Checking alert's for each node
write_header(diagnostic, 'NODES PERFOMANCE METRICS')
for node in nodes:
    write_item_header(diagnostic, 'Node: {}'.format(node['name']))
    alert_file_description(node, conditions, diagnostic)
    alert_files_description_as_sockets(node, conditions, diagnostic)
    alert_disk_free(node, conditions, diagnostic)
    alert_mem_free(node, conditions, diagnostic)
    alert_erlang_process(node, conditions, diagnostic)
    diagnostic.write("\r\n")

diagnostic.close()
