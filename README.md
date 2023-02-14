# streaming-05-06 smart-smoker
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

- Simulate a streaming series of temperature readings from our smart smoker and two foods.
- Create a producer to send these temperature readings to RabbitMQ.
- Create three consumer processes, each one monitoring one of the temperature streams. 
- Perform calculations to determine if a significant event has occurred.

We want to stream information from a smart smoker. Read one value every half minute. (sleep_secs = 30)

smoker-temps.csv has 4 columns:

[0] Time = Date-time stamp for the sensor reading
[1] Channel1 = Smoker Temp --> send to message queue "01-smoker"
[2] Channe2 = Food A Temp --> send to message queue "02-food-A"
[3] Channe3 = Food B Temp --> send to message queue "02-food-B"

### Significant Events
We want know if:

1. The smoker temperature decreases by more than 15 degrees F in 2.5 minutes (smoker alert!)
2. Any food temperature changes less than 1 degree F in 10 minutes (food stall!)

### Smart Smoker Consumer Data Challenges
If you look at the data carefully, you'll notice that we don't get our temperature readings on a regular basis. 

The timestamps are offset, and many intervals have missing data. 
For school, we will make some simplifying assumptions and focus on the overall process. 

### Simplifying assumptions
For class, assume each data point with a value occurs on a regular basis and add it to the deque. 

That is: 
- IGNORE the real timestamps
- evaluate the deque of readings (either 5 or 20) as though the real timestamps were not so terrible.
It's more complex if we try to use real timestamps. Adjusting for the non-regular timestamps is an interesting problem, but not the point. Know that you will likely have to address issues like that in the "real world". 

### Optional: Alert Notifications
- Optionally, we can have our consumers send us an email or a text when a significant event occurs. 
- You'll need some way to send outgoing emails. I use my main Gmail account - other options are possible. 

### Producer (smart_smoker_emitter.py)
The producer, smart_smoker_emitter.py, opens the csv file, smoker-temps.csv, and reads each row. For each row, a connection is made to Rabbit MQ, queues are declared, each columns is read and submitted. For each column, the time is captured, then the temp, sending both to the queue as a row. If there is no temp provided it sends a null value of 0

producing:
![producing script](https://github.com/ddwalk77/streaming-05-smart-smoker/blob/main/producing.png "producing script")

### Consumer (smart_smoker_listener.py)
