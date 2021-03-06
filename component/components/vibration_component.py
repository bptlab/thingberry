from component import ObserverComponent
import logging
import RPi.GPIO as GPIO
import time
from utils import get_logger


class VibrationComponent(ObserverComponent):
    def __init__(self, device_id):
        self.logger = get_logger(__name__)
        ObserverComponent.__init__(self, device_id)

    def start_observe(self, **kwargs):
        channel = int(self.property_config["pin"])
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(channel, GPIO.IN)
        GPIO.add_event_detect(int(self.property_config["pin"]), GPIO.RISING, bouncetime=1000)
        logging.info("Add vibration detection on channel " + str(channel))
        super().start_observe(channel=channel)

    def observe(self, channel):
        while True:
            if GPIO.event_detected(channel):
                logging.info("Detected vibration" )
                self.update_property(self.get_timestamp())
            time.sleep(0.25)

    @staticmethod
    def configure_observer():
        print("Configuring Vibration Property:")
        pin = int(input("Which pin is the vibration sensor connected to? "))
        return {
            "pin": pin,
        }
