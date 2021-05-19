import paho.mqtt.client as mqtt
import json
import time
import psutil
import subprocess

import mqtt_pass

import warnings

warnings.filterwarnings("ignore")

tam = 600
sleep = 30

client = mqtt.Client()

client.username_pw_set("proj7", mqtt_pass.passw)
#client.username_pw_set("p2afib024psu", "FCei9AVHzLTp") #test

client.connect("142.47.103.158", 1883)

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


	client.publish("PI7", json.dumps({"id": "icaro-cpu_temp", "data": "%d"%cpu_temp}))
	client.publish("PI7", json.dumps({"id": "icaro-gpu_temp", "data": "%d"%gpu_temp}))

	print('"id": "icaro-cpu_temp", "data": "%f"'%cpu_temp)
	print('"id": "icaro-gpu_temp", "data": "%f"'%gpu_temp)

	time.sleep(sleep)