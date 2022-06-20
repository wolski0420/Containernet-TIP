from mininet.net import Containernet
from mininet.node import Controller
from mininet.cli import CLI
from mininet.link import TCLink
from mininet.log import info, setLogLevel

setLogLevel('info')

net = Containernet(controller=Controller)
net.addController('c0')

info('*** Adding RabbitMQ server\n')
server = net.addDocker('server', ip='10.0.0.251',
                       dimage="rabbitmq:3.10-management-alpine",
                       ports=[5672, 15672],
                       port_bindings={5672: 5672, 15672: 15672})

info('*** Adding producer and consumer\n')
consumer = net.addDocker('consumer', ip='10.0.0.253',
                         dimage="rabbit_consumer")
producer = net.addDocker('producer', ip='10.0.0.252',
                         dimage="rabbit_producer")

info('*** Setup network\n')
s1 = net.addSwitch('s1')
net.addLink(server, s1)
net.addLink(producer, s1)
net.addLink(consumer, s1)
net.start()

info('*** Starting to execute commands\n')

# info(server.cmd("/bin/bash /usr/local/bin/docker-entrypoint.sh rabbitmq-server"))

info('Execute: consumer.cmd("nohup java -jar app.jar &")\n')
info(consumer.cmd("nohup java -jar app.jar &") + "\n")

info('Execute: producer.cmd("java -jar app.jar Hello World!")\n')
info(producer.cmd("java -jar app.jar Hello World!") + "\n")

info('Execute: producer.cmd("java -jar app.jar Hello World Again!")\n')
info(producer.cmd("java -jar app.jar Hello World Again!") + "\n")

CLI(net)

net.stop()
