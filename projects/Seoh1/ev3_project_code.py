"""
    The following are the code for CSSE 120 final project
    Author: Hyang Seo
    Class: CSSE 120
    Project name/theme: Delivery System
"""

import ev3dev.ev3 as ev3
import datetime
from datetime import datetime
import threading
from threading import Timer
import time
import rc_susie as robo
import mqtt_remote_method_calls as com




def main():
    ev3.Sound.play("/home/robot/csse120/assets/sounds/Bike.wav")
    robot = robo.Snatch3r()
    mqtt_client = com.MqttClient(robot)
    mqtt_client.connect_to_pc()
    robot.loop_forever()

main()