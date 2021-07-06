import paho.mqtt.client as mqtt
import json
import time
import psutil
import subprocess

tam = 600
sleep = 5

client = mqtt.Client()

client.username_pw_set("c8qstroc616m", "yBZStCPCxyvP")
#client.username_pw_set("p2afib024psu", "FCei9AVHzLTp") #test

client.connect("mqtt.demo.konkerlabs.net", 1883)

for i in range(tam):
	cpu_temp =	psutil.sensors_temperatures(fahrenheit=False)
	list_info = list(cpu_temp.keys())
	if list_info[2] in cpu_temp:
		for entry in cpu_temp[list_info[2]]:
			break
	cpu_temp = entry.current

	gpu_temp = subprocess.check_output(["nvidia-settings", "-q", "gpucoretemp", "-t"])
	gpu_temp = gpu_temp.decode("utf-8")
	gpu_temp = gpu_temp.split("\n")
	gpu_temp = float(gpu_temp[0])


	client.publish("data/c8qstroc616m/pub/cpu", json.dumps({"temperature": cpu_temp, "unit": "celsius"}))

	client.publish("data/c8qstroc616m/pub/gpu", json.dumps({"temperature": gpu_temp, "unit": "celsius"}))

	time.sleep(sleep)