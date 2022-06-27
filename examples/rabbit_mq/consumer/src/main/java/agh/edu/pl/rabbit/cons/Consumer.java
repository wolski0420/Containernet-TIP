package agh.edu.pl.rabbit.cons;

import com.rabbitmq.client.AMQP;
import com.rabbitmq.client.BuiltinExchangeType;
import com.rabbitmq.client.Channel;
import com.rabbitmq.client.Connection;
import com.rabbitmq.client.ConnectionFactory;
import com.rabbitmq.client.DefaultConsumer;
import com.rabbitmq.client.Envelope;

import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.util.concurrent.TimeoutException;

public class Consumer {
    public static void main(String[] args) throws IOException, TimeoutException {
        // validation
        if (args.length < 1) {
            System.out.println("Wrong number of arguments!");
            System.out.println("Schema input : <max_nack_no_at_consumer>");
            System.exit(-1);
        }

        System.out.println("CREATED CONSUMER");

        // connection & channel creation
        ConnectionFactory factory = new ConnectionFactory();
        factory.setHost("10.0.0.251");
        Connection connection = factory.newConnection();
        Channel channel = connection.createChannel();

        // exchange creation
        String EXCHANGE_NAME = "exchange";
        channel.exchangeDeclare(EXCHANGE_NAME, BuiltinExchangeType.FANOUT);

        // queue creation & bind
        String queueName = channel.queueDeclare().getQueue();
        channel.queueBind(queueName, EXCHANGE_NAME, "");
        System.out.println("Created queue: " + queueName);

        // consuming received messages from producer (handler)
        DefaultConsumer consumer = new DefaultConsumer(channel) {
            @Override
            public void handleDelivery(String consumerTag, Envelope envelope, AMQP.BasicProperties properties, byte[] body) {

                String message = new String(body, StandardCharsets.UTF_8);
                System.out.println("Received: " + message);
            }
        };

        // start listening
        System.out.println("Waiting for messages...");
        channel.basicQos(Integer.parseInt(args[0]));
        channel.basicConsume(queueName, true, consumer);
    }
}