import logging
import paho.mqtt.client as mqttclient
from os import environ
from ledswitch import switch_leds

logging.basicConfig(level=environ.get('LOGLEVEL', 'INFO').upper(),
                    format='%(asctime)s %(levelname)s %(module)s: %(message)s')

mqtt = mqttclient.Client(mqttclient.CallbackAPIVersion.VERSION2)

def on_connect(_client, _userdata, _flags, rc, _properties):
    logging.info("MQTT connected with result code "+str(rc))
    mqtt.subscribe(environ["MQTT_TOPIC"])

def on_message(_client, _userdata, msg):
    logging.debug(msg.topic+" "+msg.payload.decode("utf-8"))
    if msg.topic == environ["MQTT_TOPIC"]:
        if msg.payload.decode("utf-8").lower() == "on":
            switch_leds(set_disabled=False)
        if msg.payload.decode("utf-8").lower() == "off":
            switch_leds(set_disabled=True)

if __name__ == '__main__':
    mqtt.connect(environ["MQTT_URL"])
    mqtt.on_connect = on_connect
    mqtt.on_message = on_message
    try:
        mqtt.loop_forever()
    except KeyboardInterrupt:
        mqtt.disconnect()
