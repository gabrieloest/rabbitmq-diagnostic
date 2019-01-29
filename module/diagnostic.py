import logging
import yaml
import rabbitmq_api_utils

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

logger.info('Loading configurations....')
with open("./config/config.yml", 'r') as ymlfile:
    cfg = yaml.load(ymlfile)

rabbitmq = cfg['rabbitmq']
host = rabbitmq['host']
user = rabbitmq['user']
password = rabbitmq['password']

logger.info('host: {}'.format(host))
logger.info('user: {}'.format(user))
logger.info('password: {}'.format(password))

rmq_utils = rabbitmq_api_utils.RabbitmqAPIUtils(host, user, password)


overview = list(rmq_utils.get_overview().json())


def no_consumers_queues_report(queues):
    queues_no_conumers = list(filter(lambda item: (item['consumers'] == 0),
                                     queues.json()))

    print('Queues without consumers: ')
    for item in queues_no_conumers:
        print("Queue {} of vhost {} don't have"
              "any consumer.".format(item['name'], item['vhost']))

    print('{} withou consumers'.format(len(queues_no_conumers)))


def high_ready_messages_queues(queues):
    high_messages = list(filter(lambda item: (item['messages_ready'] > 50),
                                queues.json()))

    for item in high_messages:
        print("Queue {} of vhost {} have a high number of "
              "ready messages: {}.".format(item['name'], item['vhost'],
                                           item['messages_ready']))

    print('{} queues with high number of ready '
          'messages'.format(len(high_messages)))


def high_messages_unacknowledged_queues(queues):
    messages_unacknowledged = list(filter(lambda item: (
                                          item['messages_unacknowledged'] > 0),
                                          queues.json()))

    for item in messages_unacknowledged:
        print("Queue {} of vhost {} have a high number of "
              "messages unacknowledged: {}."
              .format(item['name'], item['vhost'],
                      item['messages_unacknowledged']))

    print('{} queues with high number of messages '
          'unacknowledged'.format(len(messages_unacknowledged)))


queues = rmq_utils.get_queues()

no_consumers_queues_report(queues)
high_ready_messages_queues(queues)
high_messages_unacknowledged_queues(queues)

nodes = list(rmq_utils.get_nodes().json())


def alert_file_description(node):
    fd_used = node['fd_used']
    fd_total = node['fd_total']
    fd_percent = (fd_used * 100) / fd_total
    fd_result = 'File Descriptors Alert '
    if(fd_percent > 90 and fd_percent < 98):
        fd_result += 'Warning: {}'.format(fd_percent)
    elif(fd_percent > 98):
        fd_result += 'Critical: {}'.format(fd_percent)
    else:
        fd_result += 'OK: {}'.format(fd_percent)

    print(fd_result)


def alert_files_description_as_sockets(node):
    sd_used = node['sockets_used']
    sd_total = node['sockets_total']
    sd_percent = (sd_used * 100) / sd_total
    sd_result = 'File Descriptors as Sockets Alert '
    if(sd_percent > 90 and sd_percent < 98):
        sd_result += 'Warning: {}'.format(sd_percent)
    elif(sd_percent > 98):
        sd_result += 'Critical: {}'.format(sd_percent)
    else:
        sd_result += 'OK: {}'.format(sd_percent)

    print(sd_result)


def alert_disk_free(node):
    disk_free = node['disk_free']
    disk_free_limit = node['disk_free_limit']
    disk_usage_percent = (disk_free_limit * 100) / disk_free
    sd_result = 'Disk Free Alert '
    if(disk_usage_percent > 90 and disk_usage_percent < 98):
        sd_result += 'Warning: {}'.format(disk_usage_percent)
    elif(disk_usage_percent > 98):
        sd_result += 'Critical: {}'.format(disk_usage_percent)
    else:
        sd_result += 'OK: {}'.format(disk_usage_percent)

    print(sd_result)


def alert_mem_free(node):
    mem_used = node['mem_used']
    mem_limit = node['mem_limit']
    mem_usage_percent = (mem_used * 100) / mem_limit
    mem_result = 'Mem Free Alert '
    if(mem_usage_percent > 90 and mem_usage_percent < 98):
        mem_result += 'Warning: {}'.format(mem_usage_percent)
    elif(mem_usage_percent > 98):
        mem_result += 'Critical: {}'.format(mem_usage_percent)
    else:
        mem_result += 'OK: {}'.format(mem_usage_percent)

    print(mem_result)


def alert_erlang_process(node):
    proc_used = node['proc_used']
    proc_total = node['proc_total']
    proc_usage_percent = (proc_used * 100) / proc_total
    proc_result = 'Erlang processes used Alert '
    if(proc_usage_percent > 90 and proc_usage_percent < 98):
        proc_result += 'Warning: {}'.format(proc_usage_percent)
    elif(proc_usage_percent > 98):
        proc_result += 'Critical: {}'.format(proc_usage_percent)
    else:
        proc_result += 'OK: {}'.format(proc_usage_percent)

    print(proc_result)


for node in nodes:
    print('Node {} metrics: '.format(node['name']))
    alert_file_description(node)
    alert_files_description_as_sockets(node)
    alert_disk_free(node)
    alert_mem_free(node)
    alert_erlang_process(node)
