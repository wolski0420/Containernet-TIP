from mininet.net import Containernet
from mininet.node import Controller
from mininet.cli import CLI
from mininet.log import info, setLogLevel
from time import sleep
from sys import  argv 

cycles = int(argv[1])
interval = int(argv[2])
no_producer = int(argv[3])

setLogLevel('info')
info(f'***starting test no cycles: {cycles}, interval: {interval}, no_producers: {no_producer} \n')

net = Containernet(controller=Controller)
net.addController('c0')

info('*** Adding RabbitMQ server\n')
server = net.addDocker('server', ip='10.0.0.251',
                       dimage="rabbitmq:3.10-management-alpine",
                       ports=[5672, 15672],
                       port_bindings={5672: 5672, 15672: 15672})

info('*** Adding producer and consumer\n')
consumer = net.addDocker('consumer', ip='10.0.0.252',
                         dimage="rabbit_consumer")

producer_list = []
for i in range(0,no_producer):
    producer_list.append(net.addDocker(f'producer{i}', ip=f'10.0.0.{250-i}',
                         dimage="rabbit_producer"))


info('*** Setup network\n')
s1 = net.addSwitch('s1')
net.addLink(server, s1)
for producer in producer_list:
    net.addLink(producer, s1)


net.addLink(consumer, s1)
net.start()

info('*** Starting to execute commands\n')

server.start()
sleep(50)


info('Execute: consumer.cmd("nohup java -jar app.jar &")\n')
info(consumer.cmd("nohup java -jar app.jar &") + "\n")


for i in range(0,cycles):
    info('Execute: producer.cmd("java -jar app.jar Hello World!")\n')
    for producer in producer_list:
        producer.cmd("java -jar app.jar Hello World! &")



    # sleep(interval)
CLI(net)

net.stop()
