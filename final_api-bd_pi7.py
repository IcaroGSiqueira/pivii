import datetime
import paho.mqtt.client as mqtt
import psycopg2
import socket
import json
import time
import mqtt_pass
import requests
import warnings
warnings.filterwarnings("ignore")

id_pel = "4314407"

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

def on_connect(client, userdata, flags, rc):
	print("Conectado, com o seguinte retorno do Broker: "+str(rc))
	client.subscribe("PI-V-B/#")

def on_message(client, userdata, msg):

	print(msg.topic+" "+str(msg.payload))

	temp_max, temp_min = buscar_dados(id_pel)

	dados_python = json.loads(msg.payload)

	sensor = dados_python['id']
	value = dados_python['data']

	data = datetime.datetime.now().strftime("%d/%m/%Y")
	hora = datetime.datetime.now().timestamp()
	print (data)

	message = sensor + " " + value + " " + str(int(time.time())) + "\n"
	print ('Enviando ao BD Graphite: %s' % message)

	server_ip = '127.0.0.1'
	server_port = 2003

	sock = socket.socket()
	sock.connect((server_ip, server_port))
	sock.sendall(message.encode('utf-8'))
	sock.close()

	con = psycopg2.connect(host='localhost', database='postgres', user='projeto', password=mqtt_pass.passpost)
	cur = con.cursor()
	insertline = """INSERT INTO icaro (id, name,  sens_val,  prev_min, prev_max, time_pub, date_pub) VALUES (%s, %s, %s, %s, %s, %s, %s);"""

	if (sensor == "PROJ-INT"):
		w_sensor_id = 1
	elif (sensor == "PROJ-INT-2"):
		w_sensor_id = 2

	values = (w_sensor_id, sensor, value, temp_min, temp_max, hora, data)

	cur.execute(insertline, values)

	con.commit()
	con.close()


client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.username_pw_set("proj7", mqtt_pass.passw)
client.connect("142.47.103.158", 1883)
client.loop_forever()
