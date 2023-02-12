"""
    This program listens for work messages contiously.
    The smart_smoker_emitter.py must run to send the messages

    Name: DeeDee Walker
    Date: 2/12/23

    We want know if (Condition To monitor):
    The smoker temperature decreases by more than 15 degrees F in 2.5 minutes (smoker alert!)
    Any food temperature changes less than 1 degree F in 10 minutes (food stall!)

    Create three consumer processes, each one monitoring one of the temperature streams. 
    Perform calculations to determine if a significant event has occurred.

    Optional: Alert Notifications
    Optionally, we can have our consumers send us an email or a text when a significant event occurs. 
    You'll need some way to send outgoing emails. I use my main Gmail account - other options are possible. 

    Time Windows:
    Smoker time window is 2.5 minutes
    Food time window is 10 minutes

    Deque Max Length:
    At one reading every 1/2 minute, the smoker deque max length is 5 (2.5 min * 1 reading/0.5 min)
    At one reading every 1/2 minute, the food deque max length is 20 (10 min * 1 reading/0.5 min) 

    Three listeneing queues: 01-smoker, 02-food-A, 02-food-B
    Three listening callback functions
"""
import pika
import sys
import time
from collections import deque

# limited to 5 items (the 5 most recent readings)
smoker_deque = deque(maxlen=5)
# limited to 20 items (the 20 most recent readings)
foodA_deque = deque(maxlen=20)
# limited to 20 items (the 20 most recent readings)
foodB_deque = deque(maxlen=20)


# define a callback function to be called when a message is received
def smoker_callback(ch, method, properties, body):
    """ Define behavior on getting a message about the smoker temperature."""
    if {body.decode(1)} == 0:
        pass
    else:
        # decode the binary message body adding the temp to the deque
        smoker_deque.append({body.decode(1)})
        # print the deque items
        list(smoker_deque)
    #check to see that deque has 5 items
    if smoker_deque.maxlen == 5:
        # read rightmost item in deque and subtract from leftmost item in deque
        #assign difference to a variable
        Smktempcheck = smoker_deque[-1]-smoker_deque[0]
        if Smktempcheck < -15:
            print("smoker alert!")
        else:
            print("Temp change in last 2.5 minutes is:"), Smktempcheck
    else:
        pass
    # acknowledge the message was received and processed 
    # (now it can be deleted from the queue)
    ch.basic_ack(delivery_tag=method.delivery_tag)

def foodA_callback(ch, method, properties, body):
    """ Define behavior on getting a message about FoodA temperature."""
    # decode the binary message body to a string
    print(f" [x] Received {body.decode()}")
    # when done with task, tell the user
    print(" [x] Done.")
    # acknowledge the message was received and processed 
    # (now it can be deleted from the queue)
    ch.basic_ack(delivery_tag=method.delivery_tag)

def foodB_callback(ch, method, properties, body):
    """ Define behavior on getting a message about FoodB temperature."""
    # decode the binary message body to a string
    print(f" [x] Received {body.decode()}")
    # when done with task, tell the user
    print(" [x] Done.")
    # acknowledge the message was received and processed 
    # (now it can be deleted from the queue)
    ch.basic_ack(delivery_tag=method.delivery_tag)

# define a main function to run the program
def main(hn: str, queue1: str, queue2: str, queue3: str):
    """ Continuously listen for task messages on a named queue."""

    # when a statement can go wrong, use a try-except block
    try:
        # try this code, if it works, keep going
        # create a blocking connection to the RabbitMQ server
        connection = pika.BlockingConnection(pika.ConnectionParameters(host=hn))

    # except, if there's an error, do this
    except Exception as e:
        print()
        print("ERROR: connection to RabbitMQ server failed.")
        print(f"Verify the server is running on host={hn}.")
        print(f"The error says: {e}")
        print()
        sys.exit(1)

    try:
        # use the connection to create a communication channel
        channel = connection.channel()

        # use the channel to declare a durable queue
        # a durable queue will survive a RabbitMQ server restart
        # and help ensure messages are processed in order
        # messages will not be deleted until the consumer acknowledges
        channel.queue_declare(queue=queue1, durable=True)
        channel.queue_declare(queue=queue2, durable=True)
        channel.queue_declare(queue=queue3, durable=True)

        # The QoS level controls the # of messages
        # that can be in-flight (unacknowledged by the consumer)
        # at any given time.
        # Set the prefetch count to one to limit the number of messages
        # being consumed and processed concurrently.
        # This helps prevent a worker from becoming overwhelmed
        # and improve the overall system performance. 
        # prefetch_count = Per consumer limit of unaknowledged messages      
        channel.basic_qos(prefetch_count=1) 

        # configure the channel to listen on a specific queue,  
        # use the callback function named callback,
        # and do not auto-acknowledge the message (let the callback handle it)
        channel.basic_consume(queue=queue1, auto_ack = False, on_message_callback=smoker_callback)
        channel.basic_consume(queue=queue2, auto_ack = False, on_message_callback=foodA_callback)
        channel.basic_consume(queue=queue3, auto_ack = False, on_message_callback=foodB_callback)

        # print a message to the console for the user
        print(" [*] Ready for work. To exit press CTRL+C")

        # start consuming messages via the communication channel
        channel.start_consuming()

    # except, in the event of an error OR user stops the process, do this
    except Exception as e:
        print()
        print("ERROR: something went wrong.")
        print(f"The error says: {e}")
        sys.exit(1)
    except KeyboardInterrupt:
        print()
        print(" User interrupted continuous listening process.")
        sys.exit(0)
    finally:
        print("\nClosing connection. Goodbye.\n")
        # delete the queues when complete so messages are cleared
        channel.queue_delete(queue1)
        channel.queue_delete(queue2)
        channel.queue_delete(queue3)
        connection.close()

# Standard Python idiom to indicate main program entry point
# This allows us to import this module and use its functions
# without executing the code below.
# If this is the program being run, then execute the code below
if __name__ == "__main__":
    # call the main function with the information needed
    main('localhost','01-smoker','02-food-A','02-food-B')
