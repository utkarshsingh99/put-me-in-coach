import paho.mqtt.client as mqtt

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print(f"Connected with result code {rc}")

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("mqtt/rpi")

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    print(f"Received message '{msg.payload.decode()}' on topic '{msg.topic}' with QoS {msg.qos}")

broker_address = "192.168.137.183"  # Replace with your MQTT broker's address
port = 1883  # Default MQTT port (use 8883 for SSL connections)

client = mqtt.Client()  # Create new instance
client.on_connect = on_connect
client.on_message = on_message

client.connect(broker_address, port, 60)  # Connect to the MQTT broker

# Blocking call that processes network traffic, dispatches callbacks, and
# handles reconnecting.
client.loop_forever()
