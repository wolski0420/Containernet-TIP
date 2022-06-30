# RabbitMQ in ContainerNet

This is a basic producer-consumer case for ContainerNet implemented 
with RabbitMQ use as communication protocol. We are here testing 
this protocol and its bounds.

Important notes:
- only one exchange,
- only one queue with one topic
- only one consumer,
- multiple producers.

All these parameters are set due to bound limits testing, where a basic
example is required. The most simple case is directed messaging without
confirmation for sender and without dividing messages across queues.

## To build

At first, you need to prepare two images. The first one is consumer image:

```bash
sudo docker build . -f Dockerfile.consumer -t rabbit_consumer
```

And the second one is producer:

```bash
sudo docker builld . -f Dockerfile.producer -t rabbit_producer
```

Now, you have two images in your local repository, so you can
run our demo.

## To run 

General command:

```bash
sudo python3 demo.py <cycles_no> <cycle_sleep_interval> <producers_no> <producer_publishes_no> <consumer_qos>
```

### Example runs:

Default command to see in Web UI that queue has messages:

```bash
sudo python3 demo.py 20 5 4 60000 1
```

If you're running it on VM, we advise you to increase cycle delay:

```bash
sudo python3 demo.py 20 10 4 60000 1
```

Important NOTE : the fact you're observing messages in queues is
dependent on your hardware specification. You may increase some
values to observe anything in UI.

## Web UI

Find IP of docker by running command:

```bash
sudo docker inspect mn.server | grep IPAddress
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
