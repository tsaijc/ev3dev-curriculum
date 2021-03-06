"""
    The following are the code for CSSE 120 final project
    Author: Hyang Seo
    Class: CSSE 120
    Project name/theme: Delivery System
"""

"""The ideal function of this code:
    The code on the pc part will activate upon certain scheduled time,
    Once the code runs, the first thing it does is to upon up a browser at indicated URL, in this project, it's a song on Youtube. 
    The tkinter dui will pop up when the code is activated to provide human input commands to the robot.
    The robot will be able to find the deliverable (beacon) when the "search for deliverable" button is pressed on dui
    The user than can manually deliver the object to wanted destination.
    """

import ev3dev.ev3 as ev3
import datetime
from datetime import datetime
import threading
from threading import Timer
import time
import rc_susie as robo
import os
import tkinter
from tkinter import ttk
import mqtt_remote_method_calls as com
import traceback

#The time schedule modifier
x=datetime.today()
y = x.replace(day=x.day, hour=0, minute=17, second=10, microsecond=0)
delta_t = y-x

secs = delta_t.seconds+1


def main():

    os.system("start https://www.youtube.com/watch?v=3pR-8cM-aVs") #The website indicated to start when the code starts
    manual_command_screen()


def manual_command_screen():
    #Manual delivery system tkinter dui
    mqtt_client = com.MqttClient()
    mqtt_client.connect_to_ev3()

    root = tkinter.Tk()
    root.title("Delivery System")

    main_frame = ttk.Frame(root, padding=20, relief='raised')
    main_frame.grid()

    manual_drive_label = ttk.Label(main_frame, text="Manual Drive System")
    manual_drive_label.grid(row=0, column=1)


    left_speed_label = ttk.Label(main_frame, text="Left")
    left_speed_label.grid(row=1, column=0)
    left_speed_entry = ttk.Entry(main_frame, width=8, justify=tkinter.RIGHT)
    left_speed_entry.insert(0, "600")
    left_speed_entry.grid(row=2, column=0)

    right_speed_label = ttk.Label(main_frame, text="Right")
    right_speed_label.grid(row=1, column=2)
    right_speed_entry = ttk.Entry(main_frame, width=8, justify=tkinter.RIGHT)
    right_speed_entry.insert(0, "600")
    right_speed_entry.grid(row=2, column=2)

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

    shake_hands = ttk.Button(main_frame, text="Search for Deliverable")
    shake_hands.grid(row=3, column=5)
    shake_hands['command'] = lambda: beacon_searching(mqtt_client)
    root.bind('<s>', lambda event: beacon_searching(mqtt_client))


    root.mainloop()

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

def beacon_searching(mqtt_client):
    print("find beacon")
    mqtt_client.send_message("seek_beacon")


t = Timer(secs, main)
t.start()



