import paho.mqtt.client as mqtt
import json

def on_connect(client, userdata, flags, rc):
    print("Conectado!")
    client.subscribe("sub/7s4feif0qrvp/cpu")

def on_message(client, data, msg):
    print(msg.topic + " " + str(msg.payload))

client = mqtt.Client()
client.on_message = on_message
client.on_connect = on_connect
client.username_pw_set("7s4feif0qrvp", "Pk5bJfr8qwxm")
client.connect("mqtt.demo.konkerlabs.net", 1883)
client.loop_forever()


