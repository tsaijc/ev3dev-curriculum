"""
    CSSE120 Final Project code.
    Author: Jocelyn Tsai
"""

import ev3dev.ev3 as ev3
import time
import mqtt_remote_method_calls as com
import robot_controller as robo


def main():
    robot = robo.Snatch3r()
    mqtt_client = com.MqttClient(robot)
    mqtt_client.connect_to_pc()
    robot.loop_forever()


# Calls  main  to start the ball rolling.
main()
