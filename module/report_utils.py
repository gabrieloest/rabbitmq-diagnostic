import os


class ReportUtils:

    def __init__(self, logger, path, filename):
        self.logger = logger
        if not os.path.exists(path):
            os.makedirs(path)
        full_file_name = '{}/{}'.format(path, filename)
        self.report = open(full_file_name, 'w+')

    def write_header(self, text):
        self.report.write("\r\n")
        self.report.write(">>>>>>>>>>> {}\r\n".format(text))
        self.report.write("\r\n")

    def write_item_header(self, text):
        self.report.write("******************************************\r\n")
        self.report.write("*******  {}\r\n".format(text))
        self.report.write("******************************************\r\n")

    def write_line(self, line):
        self.report.write(line)

    def close(self):
        self.report.close()
