import warnings
import datetime

import paho.mqtt.client as mqtt
import json
import time
import psutil
import subprocess

import mqtt_pass

import requests

id_sls = "4318804"

warnings.filterwarnings("ignore")

tam = 600
sleep = 30

client = mqtt.Client()

client.username_pw_set("proj7", mqtt_pass.passw)
#client.username_pw_set("p2afib024psu", "FCei9AVHzLTp") #test

client.connect("142.47.103.158", 1883)

def buscar_dados(id):
	request = requests.get(f"https://apiprevmet3.inmet.gov.br/previsao/{id}")
	todo = json.loads(request.content)
	
	x = datetime.datetime.now().strftime("%d/%m/%Y-%H")
	date = x.split("-")[0]
	hour = int(x.split("-")[1])

	if (hour > 4 and hour <= 12):
		preiod = 'manha'
	elif (hour > 12 and hour <= 20):
		preiod = 'tarde'
	else:
		preiod = 'noite'

	temp_max = todo['%s'%id]['%s'%date]['%s'%preiod]['temp_max']
	temp_min = todo['%s'%id]['%s'%date]['%s'%preiod]['temp_min']

	return(temp_max, temp_min)

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

	temp_max, temp_min = buscar_dados(id_sls)

	client.publish("PI7", json.dumps({"id": "icaro-cpu_temp", "data": "%d"%cpu_temp}))
	client.publish("PI7", json.dumps({"id": "icaro-gpu_temp", "data": "%d"%gpu_temp}))

	client.publish("PI7", json.dumps({"id": "icaro-temp_max_cidade", "data": "%d"%temp_max}))
	client.publish("PI7", json.dumps({"id": "icaro-temp_min_cidade", "data": "%d"%temp_min}))

	print('"id": "icaro-cpu_temp", "data": "%f"'%cpu_temp)
	print('"id": "icaro-gpu_temp", "data": "%f"'%gpu_temp)

	print('"id": "icaro-temp_max_cidade", "data": "%d"'%temp_max)
	print('"id": "icaro-temp_min_cidade", "data": "%d"'%temp_min)

	time.sleep(sleep)