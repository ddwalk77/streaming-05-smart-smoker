"""
    This program listens for work messages contiously.

    !!!!!The smart_smoker_emitter.py must run to start sending the messages first!!!!!

    Name: DeeDee Walker
    Date: 2/19/23

    We want know if (Condition To monitor):
    The smoker temperature decreases by more than 15 degrees F in 2.5 minutes (smoker alert!)
    Any food temperature changes less than 1 degree F in 10 minutes (food stall!)

    Three consumer processes, each one monitoring one of the temperature streams. 
    Perform calculations to determine if a significant event has occurred.

    Time Windows:
    Smoker time window is 2.5 minutes
    Food time window is 10 minutes

    Deque Max Length:
    At one reading every 1/2 minute, the smoker deque max length is 5 (2.5 min * 1 reading/0.5 min)
    At one reading every 1/2 minute, the food deque max length is 20 (10 min * 1 reading/0.5 min) 

    Three listening queues: 01-smoker, 02-food-A, 02-food-B
    Three listening callback functions: smoker_callback, fooda_callback, foodb_callback

    !!!!!Start the emitter first or it closes out the listener since the queue delete is part of the script!!!!!
"""
import pika
import sys
from collections import deque
import smtplib
from email.message import EmailMessage
import tomllib #requires Python 3.11

# limited to 5 items (the 5 most recent readings)
smoker_deque = deque(maxlen=5)
# limited to 20 items (the 20 most recent readings)
foodA_deque = deque(maxlen=20)
# limited to 20 items (the 20 most recent readings)
foodB_deque = deque(maxlen=20)

# define a callback function to be called when a message is received
def smoker_callback(ch, method, properties, body):
    """ Define behavior on getting a message about the smoker temperature."""
    #declare alert messages
    subject_str = ("Smoker Alert from Smoker App")
    content_str = ("Smoker Alert!")
    text_message = ("Smoker Alert from Smoker App! Smoker Alert!")
    #define a list to place smoker temps initializing with 0
    smokertemp = ['0']
    #seperate the temp from the dat/time by using split
    message = body.decode().split(",")
    #assign the temp to a variable making it a float
    smokertemp[0] = round(float(message[-1]),2)
    # add the temp to the deque
    smoker_deque.append(smokertemp[0])
    #check to see that the deque has 5 items before analyzing
    if len(smoker_deque) == 5:
        # read rightmost item in deque and subtract from leftmost item in deque
        #assign difference to a variable as a float rounded to 2
        Smktempcheck = round(float(smoker_deque[-1]-smoker_deque[0]),2)
        #if the temp has changed by 15 degress then an alert is sent
        if Smktempcheck < -15:
            print("Current smoker temp is:", smokertemp[0],";", "Smoker temp change in last 2.5 minutes is:", Smktempcheck)
            print("Smoker Alert!")
            createAndSendEmailTextAlert(subject_str,content_str, text_message)
        #Show work in progress, letting the user know the changes
        else:
            print("Current smoker temp is:", smokertemp[0],";", "Smoker temp change in last 2.5 minutes is:", Smktempcheck)
    else:
        #if the deque has less than 5 items the current temp is printed
        print("Current smoker temp is:", smokertemp[0])
    # acknowledge the message was received and processed 
    # (now it can be deleted from the queue)
    ch.basic_ack(delivery_tag=method.delivery_tag)

def foodA_callback(ch, method, properties, body):
    """ Define behavior on getting a message about FoodA temperature."""
    #declare alert messages
    subject_str = ("Food A Alert from Smoker App")
    content_str = ("Food Stall on Food A!")
    text_message = ("Food A alert from Smoker App! Food Stall on Food A!")
    #define a list to place food A temps initializing with 0
    foodatemp = ['0']
    #seperate the temp from the dat/time by using split
    message = body.decode().split(",")    
    #assign the temp to a variable making it a float
    foodatemp[0] = round(float(message[-1]),2)
    # add the temp to the deque
    foodA_deque.append(foodatemp[0])
    #check to see that the deque has 5 items before analyzing
    if len(foodA_deque) == 20:
        # read rightmost item in deque and subtract from leftmost item in deque
        #assign difference to a variable as a float rounded to 2
        foodatempcheck = round(float(foodA_deque[-1]-foodA_deque[0]),2)
        #if the temp has changed less than 1 degree then an alert is sent
        if foodatempcheck < 1:
            print("Current Food A temp is:", foodatemp[0],";", "Food A temp change in last 10 minutes is:", foodatempcheck)
            print("food stall on food A!")
            createAndSendEmailTextAlert(subject_str,content_str,text_message)
        #Show work in progress, letting the user know the changes
        else:
            print("Current Food A temp is:", foodatemp[0],";","Food A temp change in last 10 minutes is:", foodatempcheck)
    else:
        #if the deque has less than 20 items the current temp is printed
        print("Current Food A temp is:", foodatemp[0])
    # acknowledge the message was received and processed 
    # (now it can be deleted from the queue)
    ch.basic_ack(delivery_tag=method.delivery_tag)

def foodB_callback(ch, method, properties, body):
    """ Define behavior on getting a message about FoodB temperature."""
    #declare alert messages
    subject_str = ("Food B Alert from Smoker App")
    content_str = ("Food Stall on Food B!")
    text_message = ("Food B alert from Smoker App! Food Stall on Food B!")
    #define a list to place food B temps initializing with 0
    foodbtemp = ['0']
    #seperate the temp from the dat/time by using split
    message = body.decode().split(",")    
    #assign the temp to a variable making it a float
    foodbtemp[0] = round(float(message[-1]),2)
    # add the temp to the deque
    foodB_deque.append(foodbtemp[0])
    #check to see that the deque has 5 items before analyzing
    if len(foodB_deque) == 20:
        # read rightmost item in deque and subtract from leftmost item in deque
        #assign difference to a variable as a float rounded to 2
        foodbtempcheck = round(float(foodB_deque[-1]-foodB_deque[0]),2)
        #if the temp has changed less than 1 degree then an alert is sent
        if foodbtempcheck < 1:
            print("Current Food B temp is:", foodbtemp[0],";", "Food B temp change in last 10 minutes is:", foodbtempcheck)
            print("food stall on food B!")
            createAndSendEmailTextAlert(subject_str,content_str,text_message)
        #Show work in progress, letting the user know the changes
        else:
            print("Current Food B temp is:", foodbtemp[0],";","Food B temp change in last 10 minutes is:", foodbtempcheck)
    else:
        #if the deque has less than 20 items the current temp is printed
        print("Current Food B temp is:", foodbtemp[0])
    # acknowledge the message was received and processed 
    # (now it can be deleted from the queue)
    ch.basic_ack(delivery_tag=method.delivery_tag)
    
#Send an email with Python.email for alerts

def createAndSendEmailTextAlert(email_subject: str, email_body: str, text_message: str):

    """Read outgoing email info from a TOML config file"""

    with open(".env.toml", "rb") as file_object:
        secret_dict = tomllib.load(file_object)

    # basic information

    host = secret_dict["outgoing_email_host"]
    port = secret_dict["outgoing_email_port"]
    outemail = secret_dict["outgoing_email_address"]
    outpwd = secret_dict["outgoing_email_password"]

    # Create an instance of an EmailMessage

    msg = EmailMessage()
    tmsg = EmailMessage()
    msg["From"] = secret_dict["outgoing_email_address"]
    msg["To"] = secret_dict["outgoing_email_address"]
    tmsg["To"] = secret_dict["sms_address_for_texts"]
    msg["Reply-to"] = secret_dict["outgoing_email_address"]
    msg["Subject"] = email_subject
    msg.set_content(email_body)
    tmsg.set_content(text_message)
    
    print("========================================")
    print(f"Prepared Email Message: ")
    print("========================================")
    print()
    print(f"{str(msg)}")
    print(f"{str(tmsg)}")
    print("========================================")
    print()

    # Communications can fail, so use:

    # try -   to execute the code
    # except - when you get an Exception, do something else
    # finally - clean up regardless

    # Create an instance of an email server, enable debug messages

    server = smtplib.SMTP(host, port, timeout=120)
    #debug level 2 results in a timestamp
    server.set_debuglevel(2)

    print("========================================")
    print(f"SMTP server created: {str(server)}")
    print("========================================")
    print()

    try:
        print()
        server.connect(host, port)
        print("========================================")
        print(f"Connected: {host, port}")
        print("So far so good - will attempt to start TLS")
        print("========================================")
        print()

        server.starttls()
        print("========================================")
        print(f"TLS started. Will attempt to login.")
        print("========================================")
        print()

        try:
            server.login(outemail, outpwd)
            print("========================================")
            print(f"Successfully logged in as {outemail}.")
            print("========================================")
            print()

        except smtplib.SMTPHeloError:
            print("The server did not reply properly to the HELO greeting.")
            exit()
        except smtplib.SMTPAuthenticationError:
            print("The server did not accept the username/password combination.")
            exit()
        except smtplib.SMTPNotSupportedError:
            print("The AUTH command is not supported by the server.")
            exit()
        except smtplib.SMTPException:
            print("No suitable authentication method was found.")
            exit()
        except Exception as e:
            print(f"Login error. {str(e)}")
            exit()

        try:
            server.send_message(msg)
            server.send_message(tmsg)
            print("========================================")
            print(f"Message sent.")
            print("========================================")
            print()
        except Exception as e:
            print()
            print(f"ERROR: {str(e)}")
        finally:
            server.quit()
            print("========================================")
            print(f"Session terminated.")
            print("========================================")
            print()

    # Except if we get an Exception (we call e)

    except ConnectionRefusedError as e:
        print(f"Error connecting. {str(e)}")
        print()

    except smtplib.SMTPConnectError as e:
        print(f"SMTP connect error. {str(e)}")
        print()

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
        # delete the queues when complete so unprocessed messages are cleared
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