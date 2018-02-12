"""
    CSSE120 Final Project code.
    Author: Jocelyn Tsai
"""

import ev3dev.ev3 as ev3
import time
import robot_controller as robo
import tkinter
from tkinter import ttk
import mqtt_remote_method_calls as com


class MyDelegate(object):

    def __init__(self, label_to_display_messages_in):
        self.display_label = label_to_display_messages_in

    def button_pressed(self, button_name):
        print("Received: " + button_name)
        message_to_display = "{} was pressed.".format(button_name)
        self.display_label.configure(text=message_to_display)


class DataContainer(object):
    """ Helper class that might be useful to communicate between different callbacks."""

    def __init__(self):
        self.running = True


def main():
    root = tkinter.Tk()
    root.title("MQTT Remote")

    main_frame = ttk.Frame(root, padding=20, relief='raised')
    main_frame.grid()

    button_message = ttk.Label(main_frame, text="--")
    button_message.grid(row=7, column=1)

    my_delegate = MyDelegate(button_message)
    mqtt_client = com.MqttClient(my_delegate)
    mqtt_client.connect_to_ev3()

    left_speed_label = ttk.Label(main_frame, text="Left")
    left_speed_label.grid(row=0, column=0)
    left_speed_entry = ttk.Entry(main_frame, width=8)
    left_speed_entry.insert(0, "600")
    left_speed_entry.grid(row=1, column=0)

    right_speed_label = ttk.Label(main_frame, text="Right")
    right_speed_label.grid(row=0, column=2)
    right_speed_entry = ttk.Entry(main_frame, width=8, justify=tkinter.RIGHT)
    right_speed_entry.insert(0, "600")
    right_speed_entry.grid(row=1, column=2)

    forward_button = ttk.Button(main_frame, text="Forward")
    forward_button.grid(row=2, column=1)
    # forward_button and '<Up>' key is done for your here...
    forward_button['command'] = lambda: move_forward(mqtt_client, left_speed_entry, right_speed_entry)
    root.bind('<Up>', lambda event: move_forward(mqtt_client, left_speed_entry, right_speed_entry))

    left_button = ttk.Button(main_frame, text="Left")
    left_button.grid(row=3, column=0)
    # left_button and '<Left>' key
    left_button['command'] = lambda: turn_left(mqtt_client, left_speed_entry, right_speed_entry)
    root.bind('<Left>', lambda event: turn_left(mqtt_client, left_speed_entry, right_speed_entry))

    stop_button = ttk.Button(main_frame, text="Stop")
    stop_button.grid(row=3, column=1)
    # stop_button and '<space>' key (note, does not need left_speed_entry, right_speed_entry)
    stop_button['command'] = lambda: stop(mqtt_client)
    root.bind('<space>', lambda event: stop(mqtt_client))

    right_button = ttk.Button(main_frame, text="Right")
    right_button.grid(row=3, column=2)
    # right_button and '<Right>' key
    right_button['command'] = lambda: turn_right(mqtt_client, left_speed_entry, right_speed_entry)
    root.bind('<Right>', lambda event: turn_right(mqtt_client, left_speed_entry, right_speed_entry))

    back_button = ttk.Button(main_frame, text="Back")
    back_button.grid(row=4, column=1)
    # back_button and '<Down>' key
    back_button['command'] = lambda: move_back(mqtt_client, left_speed_entry, right_speed_entry)
    root.bind('<Down>', lambda event: move_back(mqtt_client, left_speed_entry, right_speed_entry))

    up_button = ttk.Button(main_frame, text="Up")
    up_button.grid(row=5, column=0)
    up_button['command'] = lambda: send_up(mqtt_client)
    root.bind('<u>', lambda event: send_up(mqtt_client))

    down_button = ttk.Button(main_frame, text="Down")
    down_button.grid(row=6, column=0)
    down_button['command'] = lambda: send_down(mqtt_client)
    root.bind('<j>', lambda event: send_down(mqtt_client))

    # Buttons for quit and exit
    q_button = ttk.Button(main_frame, text="Quit")
    q_button.grid(row=5, column=2)
    q_button['command'] = (lambda: quit_program(mqtt_client, False))

    e_button = ttk.Button(main_frame, text="Exit")
    e_button.grid(row=6, column=2)
    e_button['command'] = (lambda: quit_program(mqtt_client, True))

    root.mainloop()

    dc = DataContainer
    btn = ev3.Button()
    btn.on_backspace = lambda state: handle_shutdown(state, dc)


# Tkinter callbacks
def move_forward(mqtt_client, left_speed_entry, right_speed_entry):
    print('move forward')
    mqtt_client.send_message('drive', [int(left_speed_entry.get()), int(right_speed_entry.get())])


def move_back(mqtt_client, left_speed_entry, right_speed_entry):
    print('move backwards')
    mqtt_client.send_message('drive', [-int(left_speed_entry.get()), -int(right_speed_entry.get())])


def turn_left(mqtt_client, left_speed_entry, right_speed_entry):
    print('turn left')
    mqtt_client.send_message('drive', [-int(left_speed_entry.get()), int(right_speed_entry.get())])


def turn_right(mqtt_client, left_speed_entry, right_speed_entry):
    print('turn right')
    mqtt_client.send_message('drive', [int(left_speed_entry.get()), -int(right_speed_entry.get())])


def stop(mqtt_client):
    print('stop')
    mqtt_client.send_message('stop')


def send_up(mqtt_client):
    print("arm_up")
    mqtt_client.send_message("arm_up")


def send_down(mqtt_client):
    print("arm_down")
    mqtt_client.send_message("arm_down")


# Quit and Exit button callbacks
def quit_program(mqtt_client, shutdown_ev3):
    if shutdown_ev3:
        print("shutdown")
        mqtt_client.send_message("shutdown")
    mqtt_client.close()
    exit()


def handle_shutdown(button_state, dc):
    """ Hit back button on EV3 to exit the program."""
    if button_state:
        dc.running = False


# calls main to run program.
main()
