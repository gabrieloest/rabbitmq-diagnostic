# RabbitMQ Diagnostic Report

## About the project
The objective of this project is generate a "Diagnostic Report" based on performance metrics. You can choose between two types of reports: 
  * General Report - This will generate a report with information's about all the vhost's and nodes
  * Report per vhost - That one, will create a report file for each vhost
  
## Performance metrics

### Exchange metrics
  Exchanges tell your messages where to go. Monitoring exchanges lets you see whether messages are being routed as expected.
  1. Messages published in
  2. Messages published out
  3. Messages unroutable
  
### Node metrics
  RabbitMQ runs inside an Erlang runtime system called a node. For this reason the node is the primary reference point for observing the resource use of your RabbitMQ setup.
  When use of certain resources reaches a threshold, RabbitMQ triggers an alarm and blocks connections. For this reason, monitoring resource use across your RabbitMQ system is necessary for ensuring availability.
  1. File descriptors used
  2. File descriptors used as sockets
  3. Disk space used
  4. Memory used
  
### Connection metrics
  Any traffic in RabbitMQ flows through a TCP connection. Messages in RabbitMQ implement the structure of the AMQP frame: a set of headers for attributes like content type and routing key, as well as a binary payload that contains the content of the message. RabbitMQ is well suited for a distributed network, and even single-machine setups work through local TCP connections. Like monitoring exchanges, monitoring your connections helps you understand your application’s messaging traffic. While exchange-level metrics are observable in terms of RabbitMQ-specific abstractions such as message rates, connection-level metrics are reported in terms of computational resources.
  1. Data rates
  
### Queue metrics
  Queues receive, push, and store messages. After the exchange, the queue is a message’s final stop within the RabbitMQ server before it reaches your application. In addition to observing your exchanges, then, you will want to monitor your queues. Since the message is the top-level unit of work in RabbitMQ, monitoring queue traffic is one way of measuring your application’s throughput and performance.
  1. Queue depth
  2. Messages unacknowledged
  3. Messages ready
  4. Message rates
  5. Messages persistent
  6. Message bytes persistent
  7. Message bytes RAM
  8. Number of consumers

## Configuration
1. Create file `config/server-config.yml` with the following content:
```
rabbitmq:
  host:
  user:
  password:
```
2. Fill the fields with the values to access your RabbitmMQ server
3. The perfomance metrics configuration file `config/conditions-config.yml`, is filled with default values, but you can change it to adapt to your reality.
```
conditions:
    exchange:
        messages_published_in: 0
        messages_published_out: 0
        messages_unroutable: 0
    node:
        nodes_running: 1
        file_descriptors_used_percent_warn: 90
        file_descriptors_used_percent_critical: 98
        file_descriptors_used_as_sockets_percent_warn: 90
        file_descriptors_used_as_sockets_percent_critical: 98
        disk_space_used_percent_warn: 90
        disk_space_used_percent_critical: 98
        memory_used_percent_warn: 90
        memory_used_percent_critical: 98
        erlang_process_percent_warn: 90
        erlang_process_percent_critical: 98
    connection:
        consumers_connected: 1
        open_connections: 1
        data_rates: 0
    queue:
        depth: 0
        messages_unacknowledged: 0
        messages_ready: 0
        messages_rate: 0
        messages_persistent: 0
        messages_bytes_persistent: 0
        messages_bytes_ram: 0
        consumers_connected: 1

```
4. Change values of the fields of the `config/report-config.yml` to generate the reports in a different location and/or with a different name. 
* For the "general report", file generated will be `{report.location}/{report.general-report}.txt`
* For the "report per vhost", files generated will be `{report.location}/{report.vhost-report}{vhost name}.txt`, replacing the slash("/") to hyphen("-") in the vhost name
```
repoort:
    location: report
    general-report: diagnostic
    vhost-report: diagnostic
```

## Usage
```
git clone https://github.com/gabrieloest/rabbitmq-diagnostic
```
```
cd rabbitmq-diagnostic
```
```
python -m pip install -r requirements.txt
```
### To run the general diagnostic report:
```
python module/diagnostic.py
```

### To run the per vhost dianostic report:
```
python module/diagnostic_per_vhost.py
```
