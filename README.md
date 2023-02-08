# streaming-05-smart-smoker
Design and Implement a producer for the Smart Smoker App

# Name: DeeDee Walker
# Date: 2/7/23

### Using a Barbeque Smoker
When running a barbeque smoker, we monitor the temperatures of the smoker and the food to ensure everything turns out tasty. Over long cooks, the following events can happen:

The smoker temperature can suddenly decline.
The food temperature doesn't change. At some point, the food will hit a temperature where moisture evaporates. It will stay close to this temperature for an extended period of time while the moisture evaporates (much like humans sweat to regulate temperature). We say the temperature has stalled.

### Sensors
We have temperature sensors track temperatures and record them to generate a history of both (a) the smoker and (b) the food over time. These readings are an example of time-series data, and are considered streaming data or data in motion.

### Streaming Data
Our thermometer records three temperatures every thirty seconds (two readings every minute). The three temperatures are:

- the temperature of the smoker itself.
- the temperature of the first of two foods, Food A.
- the temperature for the second of two foods, Food B.

### Smart System
We will use Python to:

Simulate a streaming series of temperature readings from our smart smoker and two foods.
Create a producer to send these temperature readings to RabbitMQ.

We want to stream information from a smart smoker. Read one value every half minute. (sleep_secs = 30)

smoker-temps.csv has 4 columns:

[0] Time = Date-time stamp for the sensor reading
[1] Channel1 = Smoker Temp --> send to message queue "01-smoker"
[2] Channe2 = Food A Temp --> send to message queue "02-food-A"
[3] Channe3 = Food B Temp --> send to message queue "02-food-B"

### Producer (smart_smoker_emitter.py)
The producer, smart_smoker_emitter.py, opens the csv file, smoker-temps.csv, and reads each row. For each row, a connection is made to Rabbit MQ, queues are declared, each columns is read and submitted. For each column, the time is captured, then the temp, sending both to the queue as a row.

producing:
![producing script](https://github.com/ddwalk77/streaming-05-smart-smoker/blob/main/producing.png "producing script")