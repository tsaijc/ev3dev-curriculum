"""
    The following are the code for CSSE 120 final project
    Author: Hyang Seo
    Class: CSSE 120
    Project name/theme: Puzzle Alarm Clock
"""

import mqtt_remote_method_calls as com
import rc_susie as robo

def main():
    robot = robo.Snatch3r()
    mqtt_client = com.MqttClient(robot)
    mqtt_client.connect_to_pc()
    robot.loop_forever()


main()
