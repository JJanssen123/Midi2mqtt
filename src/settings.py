# ======================== SETTINGS =============================

# Settings for sending from device to mqtt, leave empty if you only want to listen to mqtt:
midi_in_device = ''  
mqtt_publish_topic = 'midi/j'

# Settings for listening on mqtt, leave empty if you only want to send from device to mqtt:
midi_out_device = ''  # on MacOS and Linux this can be a virtual device , see below
mqtt_listen_topic = 'midi/#'

# If you want to send the midi to a DAW instead of a device, you can make a virtual MIDI-device.
# However this only works on MacOS and Linux. On Windows, use a tool like loopMIDI from https://www.tobias-erichsen.de/software/loopmidi.html.
make_virtual_device = False

# Sending clock messages is not recommended because it takes heavy load on the mqtt connection and server, and mqtt is probably not fast enough, but you can try.
send_clock_messages = False

# mqtt server settings
mqtt_server = 'test.mosquitto.org'
mqtt_port = 1883     # no ssl!
mqtt_username = ''   # leave both empty if not required
mqtt_password = ''

# ========================+++++++++=============================