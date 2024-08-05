# Switch the LEDs on a MikroTik RouterOS device 

This script uses the REST API of MikroTik RouterOS devices to turn the port LEDs on or off, 
controlled by an MQTT topic on the local network.

I run this on my docker host (`docker compose up -d`) but the python script can be easily adapted to work on its own. 
