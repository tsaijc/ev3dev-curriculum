import mqtt_remote_method_calls as com
import robot_controller as robo
import ev3dev.ev3 as ev3
import time


def main():
    robot = robo.Snatch3r()
    robot.btn.on_up = handle_up_button
    mqtt_client = com.MqttClient(robot)
    mqtt_client.connect_to_pc()
    robot.loop_forever()  # Calls a function that has a while True: loop within it to avoid letting the program end.


def handle_up_button(button_state):

    if button_state:
        print("Up button is pressed")
        ev3.Sound.speak("Good  night!")
    else:
        print("Up button was released")
# ----------------------------------------------------------------------
# Calls  main  to start the ball rolling.
# ----------------------------------------------------------------------
main()
