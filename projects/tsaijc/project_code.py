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


class DataContainer(object):
    """ Helper class that might be useful to communicate between different callbacks."""
    def __init__(self):
        self.running = True


def main():

    control_ev3_movements()


def control_ev3_movements():
    """
    Builds TKinter GUI.
    Sets up buttons on TKinter GUI.
        Is for driving robot in all directions, sending messages from EV3 to PC and displaying on
        the GUI.
    """
    root = tkinter.Tk()
    root.title("MQTT Remote")

    main_frame = ttk.Frame(root, padding=20, relief='raised')
    main_frame.grid()

    mqtt_client = com.MqttClient()
    mqtt_client.connect_to_ev3()

    left_speed_label = ttk.Label(main_frame, text="Left Speed")
    left_speed_label.grid(row=0, column=0)
    left_speed_entry = ttk.LabeledScale(main_frame, from_=0, to=600)
    # left_speed_entry.insert(0, "600")
    left_speed_entry.grid(row=1, column=0)

    right_speed_label = ttk.Label(main_frame, text="Right Speed")
    right_speed_label.grid(row=0, column=2)
    right_speed_entry = ttk.LabeledScale(main_frame, from_=0, to=600)
    # right_speed_entry.insert(0, "600")
    right_speed_entry.grid(row=1, column=2)

    forward_button = ttk.Button(main_frame, text="Forward")
    forward_button.grid(row=10, column=1)
    # forward_button and '<Up>' key
    forward_button['command'] = lambda: move_forward(mqtt_client, left_speed_entry, right_speed_entry)
    root.bind('<Up>', lambda event: move_forward(mqtt_client, left_speed_entry, right_speed_entry))

    left_button = ttk.Button(main_frame, text="Left")
    left_button.grid(row=11, column=0)
    # left_button and '<Left>' key
    left_button['command'] = lambda: turn_left(mqtt_client, left_speed_entry, right_speed_entry)
    root.bind('<Left>', lambda event: turn_left(mqtt_client, left_speed_entry, right_speed_entry))

    stop_button = ttk.Button(main_frame, text="Stop")
    stop_button.grid(row=11, column=1)
    # stop_button and '<space>' key (note, does not need left_speed_entry, right_speed_entry)
    stop_button['command'] = lambda: stop(mqtt_client)
    root.bind('<space>', lambda event: stop(mqtt_client))

    right_button = ttk.Button(main_frame, text="Right")
    right_button.grid(row=11, column=2)
    # right_button and '<Right>' key
    right_button['command'] = lambda: turn_right(mqtt_client, left_speed_entry, right_speed_entry)
    root.bind('<Right>', lambda event: turn_right(mqtt_client, left_speed_entry, right_speed_entry))

    back_button = ttk.Button(main_frame, text="Back")
    back_button.grid(row=12, column=1)
    # back_button and '<Down>' key
    back_button['command'] = lambda: move_back(mqtt_client, left_speed_entry, right_speed_entry)
    root.bind('<Down>', lambda event: move_back(mqtt_client, left_speed_entry, right_speed_entry))

    up_button = ttk.Button(main_frame, text="Up")
    up_button.grid(row=13, column=0)
    up_button['command'] = lambda: send_up(mqtt_client)
    root.bind('<u>', lambda event: send_up(mqtt_client))

    down_button = ttk.Button(main_frame, text="Down")
    down_button.grid(row=14, column=0)
    down_button['command'] = lambda: send_down(mqtt_client)
    root.bind('<j>', lambda event: send_down(mqtt_client))

    tools = ttk.Label(main_frame, text="Tools To Use:")
    tools.grid(row=15, column=1)

    move_button = ttk.Button(main_frame, text="Navigate Maze")
    move_button.grid(row=16, column=0)
    move_button['command'] = lambda: drive_to_color(mqtt_client)
    root.bind('<a>', lambda event: drive_to_color(mqtt_client))

    color_button = ttk.Button(main_frame, text="Pick Up Prize")
    color_button.grid(row=16, column=2)
    color_button['command'] = lambda: pick_up_prize(mqtt_client)
    root.bind('<s>', lambda event: pick_up_prize(mqtt_client))

    beacon_find = ttk.Button(main_frame, text="Find Prize")
    beacon_find.grid(row=16, column=1)
    beacon_find['command'] = lambda: find_prize(mqtt_client)
    root.bind('<d>', lambda event: find_prize(mqtt_client))

    # Buttons for quit and exit
    q_button = ttk.Button(main_frame, text="Quit")
    q_button.grid(row=13, column=2)
    q_button['command'] = (lambda: quit_program(mqtt_client, False))

    e_button = ttk.Button(main_frame, text="Exit")
    e_button.grid(row=14, column=2)
    e_button['command'] = (lambda: quit_program(mqtt_client, True))

    root.mainloop()

    # code for exiting program when back button on EV3 is pressed.
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


def send_message(mqtt_client):
    print("send_message")
    mqtt_client.send_message(("send_message"))


def drive_to_color(mqtt_client):
    print("drive_to_color")
    mqtt_client.send_message("drive_to_color")


def pick_up_prize(mqtt_client):
    print("pick_up_prize")
    mqtt_client.send_message("pick_up_prize")


def find_prize(mqtt_client):
    print("find_prize")
    mqtt_client.send_message("find_prize")


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
