class ExchangesDiagnostic:

    def __init__(self, logger):
        self.logger = logger

    def alert_without_bindings(self, exchanges):
        result = ''
        exchanges_filtered = list(filter(lambda item: 'message_stats' not in item,
                                         exchanges))

        result += ('{} exchange(s) without bindings\r\n'
                   .format(len(exchanges_filtered)))

        for item in exchanges_filtered:
            result += ('Exchange {} of vhost {} does not have any biding\r\n'
                       .format(item['name'], item['vhost']))

        result += ('\r\n')
        return result

    def check_messages_in_not_out(self, exchanges):
        result = ''
        exchanges_filtered = list(filter(lambda item: 'message_stats' in item and 'publish_out' not in item['message_stats'],
                                         exchanges))
        result += ('{} exchange(s) with messages income but not outcome\r\n'
                   .format(len(exchanges_filtered)))

        for item in exchanges_filtered:
            if 'publish_out' not in item['message_stats']:
                result += ('Exchange {} has messages inconming({}), but does not have '
                           'messages outcoming at vhost {}\r\n'.format(item['name'], item['message_stats']['publish_in'], item['vhost']))
                continue
        result += ('\r\n')
        return result

    def check_messages_in_greater_than_out(self, exchanges):
        result = ''
        exchanges_filtered = list(filter(lambda item: self.veify(item), exchanges))
        result += ('{} exchange(s) with messages income greater than messages outcome\r\n'
                   .format(len(exchanges_filtered)))

        for item in exchanges_filtered:
            message_stats = item['message_stats']
            publish_in = message_stats['publish_in']
            publish_out = message_stats['publish_out']
            result += ('Exchange {} has messages in({}) grater then messages '
                       'out({}) at vhost {}\r\n'
                       .format(item['name'], publish_in, publish_out,
                               item['vhost']))
        result += ('\r\n')
        return result

    def veify(self, item):
        if 'message_stats' not in item:
            return False
        elif('publish_out' not in item['message_stats']):
            return False

        message_stats = item['message_stats']
        publish_in = message_stats['publish_in']
        publish_out = message_stats['publish_out']
        if('message_stats' in item and publish_in > publish_out):
            return True
        else:
            return False
