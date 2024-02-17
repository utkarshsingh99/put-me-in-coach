import paho.mqtt.client as mqtt
import time

broker_address = "2d443cd40787437f8e61362a26ccfa86.s1.eu.hivemq.cloud"  # Or your broker's address if local
port = 8883  # Default MQTT port
topic = "your/topic"

client = mqtt.Client("RaspberryPiPublisher")
client.connect(broker_address, port=port)

count = 0
while True:
    # Read data from MPU6050
    # accelerometer_data = "x,y,z"  # Replace with actual data reading code
    client.publish(topic, (count, count, count))
    count += 1
    time.sleep(0.1)  # Adjust based on your requirements