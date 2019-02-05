class QueuesDiagnostic:

    def __init__(self, logger):
        self.logger = logger

    def no_consumers_queues_report(self, queues, conditions):
        result = ''
        queues_no_conumers = list(filter(lambda item: (
                                        item['consumers'] <
                                        conditions['consumers_connected']),
                                        queues))

        result += ('{} queue(s) without consumers\r\n'
                   .format(len(queues_no_conumers)))
        for item in queues_no_conumers:
            result += ("Queue {} of vhost {} does not have any consumer.\r\n"
                       .format(item['name'], item['vhost']))
        result += ('\r\n')
        return result

    def high_ready_messages_queues(self, queues, conditions):
        result = ''
        high_messages = list(filter(lambda item: (
                                    item['messages_ready'] >
                                    conditions['messages_ready']),
                                    queues))

        result += ('{} queue(s) with high number of ready '
                   'messages\r\n'.format(len(high_messages)))
        for item in high_messages:
            result += ("Queue {} of vhost {} has a high number of ready "
                       "messages: {}.\r\n".format(item['name'],
                                                  item['vhost'],
                                                  item['messages_ready']))
        result += ('\r\n')
        return result

    def high_messages_unacknowledged_queues(self, queues, conditions):
        result = ''
        messages_unack = list(filter(lambda item: (
                                            item['messages_unacknowledged'] >
                                            conditions['messages_unacknowledged']),
                                     queues))

        result += ('{} queue(s) with high number of messages '
                   'unacknowledged\r\n'.format(len(messages_unack)))
        for item in messages_unack:
            result += ("Queue {} of vhost {} has a high number of "
                       "messages unacknowledged: {}.\r\n"
                       .format(item['name'], item['vhost'],
                               item['messages_unacknowledged']))
        result += ('\r\n')
        return result
