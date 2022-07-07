# RabbitMQ in ContainerNet

This is a basic test case prepare with a usage of perf-test docker image for creating consumers and producers. With two rabbitMQ brokers

## To run 

General command:

```bash
sudo python3 demo.py <producers_no> <consumers_no> <consumer_qos> <message_size> <duration>
```

### Example runs:

Default command to see in Web UI that queue has messages:

```bash
sudo python3 demo.py 5 1 1 10000 120
```


## Web UI

Find IP of brokes by running command:

```bash
sudo docker inspect mn.server | grep IPAddress
```

```bash
sudo docker inspect mn.server1 | grep IPAddress
```

Example printed line should be: 

```
IPAddress: "172.17.0.2"
```

Or you can run a command in ContainerNet CLI after all producer 
executions:

```bash
server netstat -an | grep 15672 | grep ESTABLISHED | awk -F ' ' '{print $4}'
```

You should have printed IP:PORT in console.

Then you just enter this IP:PORT in your web explorer and login with
these credentials:

```angular2html
login: guest
password: guest
```
