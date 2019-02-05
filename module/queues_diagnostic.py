

class QueuesDiagnostic:

    def __init__(self, logger):
        self.logger = logger

    def no_consumers_queues_report(self, queues, conditions, diagnostic):
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

    def high_ready_messages_queues(self, queues, conditions, diagnostic):
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

    def high_messages_unacknowledged_queues(self, queues, conditions, diagnostic):
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