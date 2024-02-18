# Import package
import paho.mqtt.client as mqtt

try:
	# Publish message to MQTT Topic
	count = 1
	while True:
		mqttc.publish(MQTT_TOPIC,MQTT_MSG+str(count))
		count += 1
except KeyboardInterrupt:
	# Disconnect from MQTT_Broker
	mqttc.disconnect()

