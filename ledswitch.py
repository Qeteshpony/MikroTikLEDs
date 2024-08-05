import requests
import logging
from os import environ
from requests.auth import HTTPBasicAuth

devices = environ['MT_DEVICES'].split(",")  # expects comma seperated list of domains or IPs
auth = HTTPBasicAuth(environ["MT_USERNAME"], environ["MT_PASSWORD"])
proto = "https://" if environ["MT_SSL"].lower() == "true" else "http://"

def switch_leds(set_disabled: bool) -> None:
    for device in devices:
        logging.debug(f"Switching LEDs for {device}")
        apiurl = proto + device + "/rest/system/leds"
        session = requests.Session()
        # get the list of LEDs from device
        leds = session.get(
            url=apiurl,
            auth=auth,
            timeout=2
        )
        if leds.status_code == 200:
            leds = leds.json()
            logging.debug(f"Found {len(leds)} LEDs")
            for led in leds:
                # get current state of the LED and switch it of not the desired state
                status = True if led.get("disabled").lower() == "true" else False
                if status != set_disabled:
                    logging.debug(f"Switching LED {led.get('.id')} to disabled={set_disabled}")

                    # Workaround for assumed bug found in RouterOS 7.15
                    # The devices returns the desired status for the LED and the LED stops blinking on activity but
                    # it sometimes stays on instead of off.
                    # Sending the disabled=true command twice turns all LEDs off reliably
                    repeats = 2 if set_disabled else 1
                    for _ in range(repeats):
                        patch = session.patch(
                            url=apiurl + "/" + led.get(".id"),
                            auth=auth,
                            json={"disabled": set_disabled},
                            timeout=2
                        )
                        if patch.status_code != 200:
                            logging.error(f"Failed to switch LED: {led.get('.id')}"
                                          f" with status {patch.status_code}, content: {patch.text}")
                else:
                    logging.debug(f"LED {led.get('.id')} already set to disabled={set_disabled}")
        else:
            logging.error(f"Request to {apiurl} failed with status {leds.status_code}, content: {leds.text}")
        session.close()
