#!/usr/bin/env python

# taken from https://github.com/jogleasonjr/midi2pi2mqtt
# fixed integers shoud not have quotes in json
# added receiving mqtt-messages and send as midi out
# added handling of missing values

import mido
import paho.mqtt.client as mqtt
# import struct
import json
from settings import *

print()
print("Discovered MIDI IN devices:")
print(mido.get_input_names())
print()
print("Discovered MIDI OUT devices:")
print(mido.get_output_names())

# Callback when connected to mqtt server
def on_connect(client, userdata, flags, reason_code, properties):
    print()
    print("Connected to mqtt server with result code " + str(reason_code))
    print()

    if midi_in_device and midi_in_device != '' and mqtt_publish_topic and mqtt_publish_topic != '':
        if midi_in_device in mido.get_input_names():
            try:
                global input_port
                print()            
                input_port = mido.open_input(midi_in_device)
            except:
                print("Error connecting to midi IN device")
            else:
                print ("Listening for midi on device", midi_in_device)  
                input_port.callback = publish_to_mqtt_topic
                print ("Sending midi to mqtt topic", mqtt_publish_topic)
        else:
            print("Midi IN device in settings.py does not exist")
    else:
            print("No input device set in settings.py")

    if mqtt_listen_topic and mqtt_listen_topic != '' and midi_out_device and midi_out_device != '':
        if midi_out_device in mido.get_output_names():
            try:
                global output_port
                print()
                output_port = mido.open_output(midi_out_device, make_virtual_device)
            except:
                print("Error connecting to midi OUT device")
            else:
                client.subscribe(mqtt_listen_topic)
                client.on_message = on_message
                print("Listening for midi on mqtt topic", mqtt_listen_topic)  
            
            print("Sending midi to device", midi_out_device)
        else:
            print("Midi OUT device in settings.py does not exist")
    else:
        print("No output device set in settings.py")

# Callback for messages on the mqtt-topic
def on_message(client, userdata, msg):
    # print(msg.topic + " " + str(msg.payload))
    args = json.loads(msg.payload)
    event = args['event']
    del args['event']
    message = mido.Message(event, **args)
    output_port.send(message)


# Callback for messages on the MIDI-IN device
def publish_to_mqtt_topic(message):
    # print(message)
    # output_port.send(message) # local echo
    kvps = ("event=" + str(message)).split(" ")    
    event = kvps[0]    
    del(kvps[0])
    dict = {k: int(v) for kvp in kvps for k, v in (kvp.split("="),)}	
    dict['event'] = event.split('=')[1]	    
    if dict['event'] != 'clock' or send_clock_messages:
        #print(message)
        json_str = json.dumps(dict)
        #print(json_str)
        client.publish(mqtt_publish_topic, payload=json_str)  

# make mqtt connection
if (midi_in_device and midi_in_device != '' and midi_in_device in mido.get_input_names() and mqtt_publish_topic and mqtt_publish_topic != '') or (mqtt_listen_topic and mqtt_listen_topic != '' and midi_out_device and midi_out_device != '' and midi_out_device in mido.get_output_names()):
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
    if mqtt_username and mqtt_password and mqtt_username != '' and mqtt_password != '':
        client.username_pw_set(mqtt_username,mqtt_password)
    client.on_connect = on_connect
    try:
        client.connect(mqtt_server, mqtt_port, 60)
    except:
        print("Error connecting to mqtt server")
    else:
        client.loop_forever()
else:
    print()
    print ("No devices and mqtt-topics set in settings.py or device does not exist. Copy the name of the device from above.")
