import logging
import configresolver
import rabbitmq_api_utils

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

config = configresolver.ConfigResolver(logger)
server_config = config.load_server_config()

rmq_utils = rabbitmq_api_utils.RabbitmqAPIUtils(server_config['host'],
                                                server_config['user'],
                                                server_config['password'])

overview = list(rmq_utils.get_overview().json())


def no_consumers_queues_report(queues, conditions):
    queues_no_conumers = list(filter(lambda item: (
                                     item['consumers'] <
                                     conditions['consumers_connected']),
                                     queues.json()))

    print('Queues without consumers: ')
    for item in queues_no_conumers:
        print("Queue {} of vhost {} does not have "
              "any consumer.".format(item['name'], item['vhost']))

    print('{} withou consumers'.format(len(queues_no_conumers)))


def high_ready_messages_queues(queues, conditions):
    high_messages = list(filter(lambda item: (
                                item['messages_ready'] >
                                conditions['messages_ready']),
                                queues.json()))

    for item in high_messages:
        print("Queue {} of vhost {} has a high number of "
              "ready messages: {}.".format(item['name'], item['vhost'],
                                           item['messages_ready']))

    print('{} queues with high number of ready '
          'messages'.format(len(high_messages)))


def high_messages_unacknowledged_queues(queues, conditions):
    messages_unacknowledged = list(filter(lambda item: (
                                          item['messages_unacknowledged'] >
                                          conditions['messages_unacknowledged']),
                                          queues.json()))

    for item in messages_unacknowledged:
        print("Queue {} of vhost {} has a high number of "
              "messages unacknowledged: {}."
              .format(item['name'], item['vhost'],
                      item['messages_unacknowledged']))

    print('{} queues with high number of messages '
          'unacknowledged'.format(len(messages_unacknowledged)))


def check_alert(actual_value, total_value, warn_value,
                          critical_value, message):
    percent_value = (actual_value * 100) / total_value

    if(percent_value > warn_value and
       percent_value < critical_value):
        message += ' Warning: {}'.format(percent_value)
    elif(percent_value > critical_value):
        message += ' Critical: {}'.format(percent_value)
    else:
        message += ' OK: {}'.format(percent_value)

    return message


def alert_file_description(node, conditions):
    fd_used = node['fd_used']
    fd_total = node['fd_total']
    fd_result = 'File Descriptors Alert'

    message = check_alert(fd_used, fd_total,
                          conditions['file_descriptors_used_warn'],
                          conditions['file_descriptors_used_critical'],
                          fd_result)
    print(message)


def alert_files_description_as_sockets(node, conditions):
    sd_used = node['sockets_used']
    sd_total = node['sockets_total']
    sd_result = 'File Descriptors as Sockets Alert'

    message = check_alert(sd_used, sd_total,
                          conditions['file_descriptors_used_as_sockets_warn'],
                          conditions['file_descriptors_used_as_sockets_critical'],
                          sd_result)

    print(message)


def alert_disk_free(node, conditions):
    disk_free = node['disk_free']
    disk_free_limit = node['disk_free_limit']
    df_result = 'Disk Free Alert'

    message = check_alert(disk_free_limit, disk_free,
                          conditions['disk_space_used_warn'],
                          conditions['disk_space_used_critical'],
                          df_result)

    print(message)


def alert_mem_free(node, conditions):
    mem_used = node['mem_used']
    mem_limit = node['mem_limit']
    mem_result = 'Mem Free Alert'

    message = check_alert(mem_used, mem_limit,
                          conditions['memory_used_warn'],
                          conditions['memory_used_critical'],
                          mem_result)

    print(message)


def alert_erlang_process(node, conditions):
    proc_used = node['proc_used']
    proc_total = node['proc_total']
    proc_result = 'Erlang processes used Alert '

    message = check_alert(proc_used, proc_total,
                          conditions['erlang_process_warn'],
                          conditions['erlang_process_critical'],
                          proc_result)

    print(message)


conditions = config.load_conditions_config()

queues = rmq_utils.get_queues()

no_consumers_queues_report(queues, conditions)
high_ready_messages_queues(queues, conditions)
high_messages_unacknowledged_queues(queues, conditions)

nodes = list(rmq_utils.get_nodes().json())

for node in nodes:
    print('Node {} metrics: '.format(node['name']))
    alert_file_description(node, conditions)
    alert_files_description_as_sockets(node, conditions)
    alert_disk_free(node, conditions)
    alert_mem_free(node, conditions)
    alert_erlang_process(node, conditions)
