#!/usr/bin/env python

# taken from https://github.com/jogleasonjr/midi2pi2mqtt
# fixed integers shoud not have quotes in json
# added receiving mqtt-messages and send as midi out
# added handling of missing values

# ======================== SETTINGS =============================

# settings for sending from device to mqtt, leave empty if you only want to listen to mqtt:
midi_in_device = 'UMC404HD 192k MIDI In 0'  
mqtt_publish_topic = 'midi/jorg'

# settings for listening on mqtt, leave empty if you only want to send from device to mqtt:
midi_out_device = 'Midi2mqtt 3'
mqtt_listen_topic = 'midi/*'

# mqtt server settings
mqtt_server = 'test.mosquitto.org'
mqtt_port = 1883     # no ssl!
mqtt_username = ''   # leave both empty if not required
mqtt_password = ''

# ========================+++++++++=============================

import mido
import paho.mqtt.client as mqtt
import struct
import json

print()
print("Discovered MIDI IN devices:")
print(mido.get_input_names())
print()
print("Discovered MIDI OUT devices:")
print(mido.get_output_names())



# Callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, reason_code, properties):
    print()
    print("Connected to mqtt server with result code " + str(reason_code))

    if midi_in_device and midi_in_device != '' and mqtt_publish_topic and mqtt_publish_topic != '':
        print()
        input_port = mido.open_input(midi_in_device)
        print ("Listening for midi on device", midi_in_device)  
        input_port.callback = publish_to_mqtt_topic
        print ("Sending midi to mqtt topic", mqtt_publish_topic)

    if mqtt_listen_topic and mqtt_listen_topic != '' and midi_out_device and midi_out_device != '':
        print()
        client.subscribe(mqtt_listen_topic)
        client.on_message = on_message
        print("Listening for midi on mqtt topic", mqtt_listen_topic)  
        output_port = mido.open_output(midi_out_device)
        print("Sending midi to device", midi_out_device)

# Callback for messages on the mqtt-topic
def on_message(client, userdata, msg):
    # print(msg.topic + " " + str(msg.payload))
    args = json.loads(msg.payload)
    event = args['event']
    del args['event']
    message = mido.Message(event, **args)
    if midi_out_device and midi_out_device != '':  
        output_port.send(message)


# Callback for messages on the MIDI-IN device
def publish_to_mqtt_topic(message):
    # output_port.send(message) # local echo
    kvps = ("event=" + str(message)).split(" ")    
    event = kvps[0]
    del(kvps[0])
    dict = {k: int(v) for kvp in kvps for k, v in (kvp.split("="),)}	
    dict['event'] = event.split('=')[1]	    
    if dict['event'] != 'clock':
        json_str = json.dumps(dict)
        #print(json_str)
        client.publish(mqtt_publish_topic, payload=json_str)  

# make mqtt connection
client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
if mqtt_username and mqtt_password and mqtt_username != '' and mqtt_password != '':
    client.username_pw_set(mqtt_username,mqtt_password)
client.on_connect = on_connect
client.connect(mqtt_server, mqtt_port, 60)
client.loop_forever()
