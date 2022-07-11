from mininet.net import Containernet
from mininet.node import Controller
from mininet.cli import CLI
from mininet.log import info, setLogLevel
from os import system
from time import sleep
from sys import argv


setLogLevel('info')

if len(argv) != 6:
    info('Wrong number of parameters!\n')
    info('Schema input: <producers_no> <consumers_no> <consumer_qos> <message_size> <duration>\n')
    exit(-1)


producers_no = int(argv[1])
consumers_no = int(argv[2])
consumer_qos = int(argv[3])
message_size = int(argv[4])
duration = int(argv[5])


info(f'*** Starting test {producers_no=}, {consumers_no=}, {consumer_qos=}, {message_size=}, {duration=}\n')
net = Containernet(controller=Controller)
net.addController('c0')


info('*** Adding RabbitMQ server\n')
server = net.addDocker('server', ip='10.0.0.251',
                       dimage="rabbitmq:3.10-management-alpine",
                       ports=[5672, 15672],
                       port_bindings={5672: 5672, 15672: 15672})
server1 = net.addDocker('server1', ip='10.0.0.253',
                       dimage="rabbitmq:3.10-management-alpine",
                       ports=[5672, 15672],
                       port_bindings={5672: 5671, 15672: 15671})

info('*** Adding perf-test\n')
perf_test = net.addDocker('perf_test', ip='10.0.0.252',
                          dimage="pivotalrabbitmq/perf-test:alpine")


info('*** Setup and start network\n')
s1 = net.addSwitch('s1')
net.addLink(server, s1)
net.addLink(server1, s1)
net.addLink(perf_test, s1)
net.start()


info('*** Starting server\n')
info("*** Waiting 10 sec to start server...\n")
server.start()
server1.start()

sleep(15)
info("*** Printing server IP:PORT to reach UI\n")
info(server.cmd("netstat -an | grep 15672 | grep ESTABLISHED | awk -F ' ' '{print $4}'"))


info('*** Starting perf-test\n')
info(perf_test.cmd(f"bin/runjava com.rabbitmq.perf.PerfTest "
                   f"-x {producers_no} "
                   f"-y {consumers_no} "
                   f"-q {consumer_qos} "
                   f"-s {message_size} "
                   f"-z {duration} "
                   f"-u \"throughput-test-1\" -f mandatory -l -c 10 -o output.csv --id \"test 1\" -uris amqp://10.0.0.251 amqp://10.0.0.253"))


info('*** Copying output from container to host')
system("docker cp mn.perf_test:/perf_test/output.csv .")


info(f'*** Starting CLI\n')
CLI(net)


info(f'*** Finishing test execution\n')
net.stop()
