package agh.edu.pl.rabbit.prod;

import com.rabbitmq.client.*;

import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.util.Arrays;
import java.util.concurrent.TimeoutException;
import java.util.stream.Collectors;

public class Producer {
    public static void main(String[] args) throws IOException, TimeoutException {
        // validation
        if (args.length < 1) {
            System.out.println("Wrong number of arguments!");
            System.exit(-1);
        }

        System.out.println("CREATING PRODUCER");

        // connection & channel creation
        ConnectionFactory factory = new ConnectionFactory();
        factory.setHost("10.0.0.251");
        Connection connection = factory.newConnection();
        Channel channel = connection.createChannel();

        // exchange creation
        String EXCHANGE_NAME = "exchange";
        channel.exchangeDeclare(EXCHANGE_NAME, BuiltinExchangeType.FANOUT);

        // taking message from console
        String message = String.join(" ", args);

        // send message to consumer
        for (int i = 0; i < 500; i++) {

            channel.basicPublish(EXCHANGE_NAME, "", null, message.getBytes(StandardCharsets.UTF_8));
            System.out.println("Sent: " + message);
        }
        // close channel and connection
        channel.close();
        connection.close();
    }
}