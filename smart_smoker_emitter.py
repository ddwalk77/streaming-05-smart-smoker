"""
    This program sends a message to a queue on the RabbitMQ server.
    We are sending the time and temp from the smoker and two food
    items.

    Name: DeeDee Walker
    Date: 2/7/23

"""
import pika
import sys
import webbrowser
import csv
import time

def offer_rabbitmq_admin_site(show_offer):
    """Pass true or false to offer the RabbitMQ Admin website to open automatically or prompt"""
    if show_offer == True :
        ans = input("Would you like to monitor RabbitMQ queues? y or n ")
        print()
        if ans.lower() == "y":
            webbrowser.open_new("http://localhost:15672/#/queues")
            print()
    else:
        webbrowser.open_new("http://localhost:15672/#/queues")
        
def send_message(host: str):
    """
    Reads csv file as a message to the queue each execution.
    This process runs and finishes.

    Parameters:
        host (str): the host name or IP address of the RabbitMQ server
        queue1 (str): the name of the smoker queue
        queue2 (str): the name of the FoodA queue
        queue3 (str): the name of the FoodB queue
        file_name: name of the csv we are reading
        nulltemp: when no temp enter 0

    """
    #declare the variables
    file_name = 'smoker-temps.csv'
    queue1 = '01-smoker'
    queue2 = '02-food-A'
    queue3 = '02-food-B'
    nulltemp = 0

    # read from a file to get the messages (aka data) to be sent - declaring variable file_name
    with open(file_name, 'r') as file:
        # Create a csv reader to read per row each new line
        reader = csv.reader(file, delimiter= ',')

        # Our file has a header row, move to next to get to data
        header = next(reader)

        try:
            # create a blocking connection to the RabbitMQ server
            conn = pika.BlockingConnection(pika.ConnectionParameters(host))
            # use the connection to create a communication channel
            ch = conn.channel()
            # delete the queue on startup to clear them before redeclaring
            ch.queue_delete(queue1)
            ch.queue_delete(queue2)
            ch.queue_delete(queue3)
            # use the channel to declare a durable queue
            # a durable queue will survive a RabbitMQ server restart
            # and help ensure messages are processed in order
            # messages will not be deleted until the consumer acknowledges
            ch.queue_declare(queue=queue1, durable=True)
            ch.queue_declare(queue=queue2, durable=True)
            ch.queue_declare(queue=queue3, durable=True)
    
            for row in reader:
                # set local variables for each column in the row
                # note: the order of the columns is important
                # and must match the order in the input file
                # We really only care about the temperature column
                Time,Channel1,Channel2,Channel3 = row

                try:
                    # use the built-in round() function to round to 2 decimal places
                    # use the built-in float() function to 
                    # convert the string (as read) 
                    # to a float (a floating point number) or decimal
                    SmokerTemp = round(float(Channel1),2)
                    # use an fstring to create a message from our data
                    Smokerstring = f"[{Time},{SmokerTemp}]"
                    # prepare a binary (1s and 0s) message to stream
                    Smokerstring = Smokerstring.encode()
                    # use the channel to publish a message to the queue
                    # every message passes through an exchange
                    ch.basic_publish(exchange="", routing_key=queue1, body=Smokerstring)
                    # print a message to the console for the user
                    print(f" [x] Sent {Smokerstring}")
                except ValueError:
                    # no temp to print so just print the time and a zero
                    Smokerstring = f"[{Time},{nulltemp}]"
                    Smokerstring = Smokerstring.encode()
                    ch.basic_publish(exchange="", routing_key=queue1, body=Smokerstring)
                    print(f" [x] Sent {Smokerstring}")

                try:
                    # use the built-in round() function to round to 2 decimal places
                    # use the built-in float() function to 
                    # convert the string (as read) 
                    # to a float (a floating point number) or decimal
                    FoodATemp = round(float(Channel2),2)
                    # use an fstring to create a message from our data
                    Astring = f"[{Time},{FoodATemp}]"
                    # prepare a binary (1s and 0s) message to stream
                    Astring = Astring.encode()
                    # use the channel to publish a message to the queue
                    # every message passes through an exchange
                    ch.basic_publish(exchange="", routing_key=queue2, body=Astring)
                    # print a message to the console for the user
                    print(f" [x] Sent {Astring}")
                except ValueError:
                    # no temp to print so just print the time and a zero
                    Astring = f"[{Time},{nulltemp}]"
                    Astring = Astring.encode()
                    ch.basic_publish(exchange="", routing_key=queue2, body=Astring)
                    print(f" [x] Sent {Astring}")

                try:
                    # use the built-in round() function to round to 2 decimal places
                    # use the built-in float() function to 
                    # convert the string (as read) 
                    # to a float (a floating point number) or decimal
                    FoodBTemp = round(float(Channel3),2)
                    # use an fstring to create a message from our data
                    Bstring = f"[{Time},{FoodBTemp}]"
                    # prepare a binary (1s and 0s) message to stream
                    Bstring = Bstring.encode()
                    # use the channel to publish a message to the queue
                    # every message passes through an exchange
                    ch.basic_publish(exchange="", routing_key=queue3, body=Bstring)
                    # print a message to the console for the user
                    print(f" [x] Sent {Bstring}")
                except ValueError:
                    # no temp to print so just print the time and a zero
                    Bstring = f"[{Time},{nulltemp}]"
                    Bstring = Bstring.encode()
                    ch.basic_publish(exchange="", routing_key=queue3, body=Bstring)
                    print(f" [x] Sent {Bstring}")

        except pika.exceptions.AMQPConnectionError as e:
            print(f"Error: Connection to RabbitMQ server failed: {e}")
            sys.exit(1)
        finally:
            # close the connection to the server
            conn.close()
            
        #sleep for 30 seconds
        time.sleep(1)

# Standard Python idiom to indicate main program entry point
# This allows us to import this module and use its functions
# without executing the code below.
# If this is the program being run, then execute the code below
if __name__ == "__main__":  
    # ask the user if they'd like to open the RabbitMQ Admin site or just open it by passing True or False
    offer_rabbitmq_admin_site(True)

    # send the message to the queue
    send_message('localhost')