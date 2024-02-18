# Import package

import board
import os
import csv
import adafruit_tca9548a
import adafruit_mpu6050
import time as timesleep
from time import time
import paho.mqtt.client as mqtt

# Define Variables
MQTT_HOST = "192.168.137.183"
MQTT_PORT = 1883
MQTT_KEEPALIVE_INTERVAL = 5
MQTT_TOPIC = "mqtt/rpi"

# Define on_connect event Handler
def on_connect(mosq, obj, rc):
	print ("Connected to MQTT Broker")

# Define on_publish event Handler
def on_publish(client, userdata, mid):
	print ("Message Published...")

# Initiate MQTT Client
mqttc = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1)

# Register Event Handlers
mqttc.on_publish = on_publish
mqttc.on_connect = on_connect

# Connect with MQTT Broker
mqttc.connect(MQTT_HOST, MQTT_PORT, MQTT_KEEPALIVE_INTERVAL)


def save_csv_with_unique_name(base_filename, data, directory="."):
    """
    Saves data to a CSV file, appending a number to the filename if it already exists.

    :param base_filename: The base name of the file (e.g., 'example.csv')
    :param data: The data to be saved in the file, a list of rows, with each row being a list of values.
    :param directory: The directory where the file will be saved. Defaults to the current directory.
    :return: The path to the saved file.
    """
    # Ensure the directory ends with a separator if it's not empty
    if directory and not directory.endswith(os.path.sep):
        directory += os.path.sep

    filename, file_extension = os.path.splitext(base_filename)
    counter = 0  # Start with no number appended
    unique_filename = f"{directory}{filename}{file_extension}"

    # Check if the file exists and update the filename until it's unique
    while os.path.exists(unique_filename):
        counter += 1
        unique_filename = f"{directory}{filename}({counter}){file_extension}"

    # Save the data to the CSV file
    with open(unique_filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(data)

    print(f"CSV file saved as {unique_filename}")
    return unique_filename

# Define a function to read the sensor data
def read_sensor_data(mpu):

    # Read the accelerometer values
    accelerometer_data = mpu.get_accel_data()

    # Read the gyroscope values
    gyroscope_data = mpu.get_gyro_data()

    # Read temp
    temperature = mpu.get_temp()

    return accelerometer_data, gyroscope_data, temperature

# Create I2C bus as normal
i2c = board.I2C()  # uses board.SCL and board.SDA
# i2c = board.STEMMA_I2C()  # For using the built-in STEMMA QT connector on a microcontroller

# Create the TCA9548A object and give it the I2C bus
tca = adafruit_tca9548a.TCA9548A(i2c)

mpu1 = adafruit_mpu6050.MPU6050(tca[2])
mpu2 = adafruit_mpu6050.MPU6050(tca[3])
mpu3 = adafruit_mpu6050.MPU6050(tca[4])

data = []

try:
	# Publish message to MQTT Topic
	while True:
		send_list = [time()] + list(mpu1.acceleration) + list(mpu1.gyro) +list(mpu2.acceleration) + list(mpu2.gyro) +list(mpu3.acceleration) + list(mpu3.gyro)
		send_list = [str(value) for value in send_list]
		send_str = ",".join(send_list)
		mqttc.publish(MQTT_TOPIC,send_str)
except KeyboardInterrupt:
	# Disconnect from MQTT_Broker
	mqttc.publish(MQTT_TOPIC,"ENDENDEND")
	mqttc.disconnect()

