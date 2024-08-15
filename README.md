# Switch the Interface LEDs on a MikroTik RouterOS device 

This script uses the REST API of MikroTik RouterOS devices to turn the interface LEDs on or off, 
controlled by an MQTT topic on the local network.

I run this on my docker host but the python script can be easily adapted to work on its own.

### Usage
- Create a user with _full_ permissions on each of the devices and give it a strong password
- Copy the ledswitch.example.env file to ledswitch.env 
- Edit the ledswitch.env file and fill in your data
- Build and start the container by running `docker compose up -d`

### Not all MikroTik devices support this 
I am using this on a _CRS309-1G-8S+IN_ and a _CRS326-24G-2S+RM_ which both support switching all Interface LEDs.
If the interface LEDs are listed unter /system/leds the chances are good that you can switch them.
Some devices only support switching some of their LEDs, e.g. the _hEX S_ can only switch the LED for the SFP-Port off.
