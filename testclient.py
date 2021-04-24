# 
# Simple script to send a single sound to the topic farmietalkie/message/test
#

import paho.mqtt.client as mqtt

def generate_test_sound() -> bytearray: 
	f = open("assets/testsound.wav", "rb")
	test_file = f.read()
	f.close()
	byteArray = bytearray(test_file)
	return byteArray

def on_connect(client, userdata, flags, rc):
	c.publish("farmietalkie/message/test", payload=generate_test_sound())

c = mqtt.Client()
c.on_connect = on_connect
c.connect("vps.esdy.io", 16805)
c.loop_forever()