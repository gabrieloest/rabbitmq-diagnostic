
class NodesDiagnostic:

    def __init__(self, logger):
        self.logger = logger

    def check_alert(self, actual_value, total_value, warn_value,
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

    def alert_file_description(self, node, conditions, diagnostic_file):
        fd_used = node['fd_used']
        fd_total = node['fd_total']
        fd_result = 'File Descriptors Alert'

        message = self.check_alert(fd_used, fd_total,
                                   conditions['file_descriptors_used_warn'],
                                   conditions['file_descriptors_used_critical'],
                                   fd_result)
        diagnostic_file.write(message)

    def alert_files_description_as_sockets(self, node, conditions, diagnostic_file):
        sd_used = node['sockets_used']
        sd_total = node['sockets_total']
        sd_result = 'File Descriptors as Sockets Alert'

        message = self.check_alert(sd_used, sd_total,
                                   conditions['file_descriptors_used_as_sockets_warn'],
                                   conditions['file_descriptors_used_as_sockets_critical'],
                                   sd_result)

        diagnostic_file.write(message)

    def alert_disk_free(self, node, conditions, diagnostic_file):
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

        diagnostic_file.write(message)

    def alert_mem_free(self, node, conditions, diagnostic_file):
        mem_used = node['mem_used']
        mem_limit = node['mem_limit']
        mem_result = 'Mem Free Alert'

        message = self.check_alert(mem_used, mem_limit,
                                   conditions['memory_used_warn'],
                                   conditions['memory_used_critical'],
                                   mem_result)

        diagnostic_file.write(message)

    def alert_erlang_process(self, node, conditions, diagnostic_file):
        proc_used = node['proc_used']
        proc_total = node['proc_total']
        proc_result = 'Erlang processes used Alert '

        message = self.check_alert(proc_used, proc_total,
                                   conditions['erlang_process_warn'],
                                   conditions['erlang_process_critical'],
                                   proc_result)

        diagnostic_file.write(message)