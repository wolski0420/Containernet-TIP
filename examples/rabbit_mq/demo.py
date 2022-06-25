from mininet.net import Containernet
from mininet.node import Controller
from mininet.cli import CLI
from mininet.log import info, setLogLevel
from time import sleep
from sys import argv

setLogLevel('info')

if len(argv) != 6:
    info('Wrong number of parameters!\n')
    info('Schema input: <cycles_no> <cycle_sleep_interval> '
         '<producers_no> <producer_publishes_no> <consumer_qos>\n')
    exit(-1)

cycles_no = int(argv[1])
cycle_sleep_interval = int(argv[2])
producers_no = int(argv[3])
producer_publishes_no = int(argv[4])
consumer_qos = int(argv[5])


info(f'*** Starting test {cycles_no=}, {cycle_sleep_interval=}, '
     f'{producers_no=}, {producer_publishes_no=}, {consumer_qos=}\n')
net = Containernet(controller=Controller)
net.addController('c0')


info('*** Adding RabbitMQ server\n')
server = net.addDocker('server', ip='10.0.0.251',
                       dimage="rabbitmq:3.10-management-alpine",
                       ports=[5672, 15672],
                       port_bindings={5672: 5672, 15672: 15672})


info('*** Adding consumer\n')
consumer = net.addDocker('consumer', ip='10.0.0.252',
                         dimage="rabbit_consumer")


info('*** Adding producers\n')
producer_list = []
for i in range(0, producers_no):
    producer_list.append(
        net.addDocker(f'producer{i}', ip=f'10.0.0.{250-i}',
                      dimage="rabbit_producer")
    )


info('*** Setup network\n')
s1 = net.addSwitch('s1')
net.addLink(server, s1)
for producer in producer_list:
    net.addLink(producer, s1)

net.addLink(consumer, s1)
net.start()


info('*** Starting server\n')
info("*** Waiting 10 sec to start server...\n")
server.start()
sleep(10)
info("*** Printing server IP:PORT to reach UI\n")
info(server.cmd("netstat -an | grep 15672 | grep ESTABLISHED | awk -F ' ' '{print $4}'"))
info("*** Waiting 10 sec to start consumer and producers...\n")
sleep(10)


info('*** Starting consumer\n')
info(f'Execute: consumer.cmd("nohup java -jar app.jar {consumer_qos} &")\n')
info(consumer.cmd(f"nohup java -jar app.jar {consumer_qos} &") + "\n")


info('*** Starting producers\n')
for i in range(0, cycles_no):
    info(f'Execute: producer.cmd("java -jar app.jar {producer_publishes_no} Hello World!")\n')
    for producer in producer_list:
        producer.cmd(f"java -jar app.jar {producer_publishes_no} Hello World! &")

    sleep(cycle_sleep_interval)


info(f'*** Starting CLI\n')
CLI(net)


info(f'*** Finishing test execution\n')
net.stop()
