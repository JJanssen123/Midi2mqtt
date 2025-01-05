# ======================== SETTINGS =============================

# settings for sending from device to mqtt, leave empty if you only want to listen to mqtt:
midi_in_device = ''  
mqtt_publish_topic = ''

# settings for listening on mqtt, leave empty if you only want to send from device to mqtt:
midi_out_device = 'Microsoft GS Wavetable Synth 0'
mqtt_listen_topic = 'midi/#'

# mqtt server settings
mqtt_server = 'test.mosquitto.org'
mqtt_port = 1883     # no ssl!
mqtt_username = 'jorg'   # leave both empty if not required
mqtt_password = ''

# ========================+++++++++=============================