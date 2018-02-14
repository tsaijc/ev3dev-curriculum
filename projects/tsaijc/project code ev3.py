"""
    CSSE120 Final Project code.
    Author: Jocelyn Tsai
"""

import ev3dev.ev3 as ev3
import time
import mqtt_remote_method_calls as com


class MyDelegate(object):
    def __init__(self):
        self.running = True


def main():
    my_delegate = MyDelegate()
    mqtt_client = com.MqttClient(my_delegate)
    mqtt_client.connect_to_pc()

    btn = ev3.Button()
    btn.on_up = lambda state: handle_button_press(state, mqtt_client, "Up")
    btn.on_down = lambda state: handle_button_press(state, mqtt_client, "Down")
    btn.on_left = lambda state: handle_button_press(state, mqtt_client, "Left")
    btn.on_right = lambda state: handle_button_press(state, mqtt_client, "Right")
    btn.on_backspace = lambda state: handle_shutdown(state, my_delegate)

    while my_delegate.running:
        btn.process()
        time.sleep(0.01)

    ev3.Sound.speak("Goodbye").wait()


def handle_button_press(button_state, mqtt_client, button_name):
    """Handle IR / button event."""
    if button_state:
        print("{} button was pressed".format(button_name))
        mqtt_client.send_message('button_pressed', [button_name])


def handle_shutdown(button_state, dc):
    """ Hit back button on EV3 to exit the program."""
    if button_state:
        dc.running = False


# Calls  main  to start the ball rolling.
main()
