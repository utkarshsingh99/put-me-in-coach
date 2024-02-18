# Import package
import paho.mqtt.client as mqtt

# Define Variables
MQTT_HOST = "192.168.137.183"
MQTT_PORT = 1883
MQTT_KEEPALIVE_INTERVAL = 5
MQTT_TOPIC = "mqtt/rpi"
MQTT_MSG = "Hello MQTT"

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

try:
	# Publish message to MQTT Topic
	count = 1
	while True:
		mqttc.publish(MQTT_TOPIC,MQTT_MSG+str(count))
		count += 1
except KeyboardInterrupt:
	# Disconnect from MQTT_Broker
	mqttc.disconnect()

