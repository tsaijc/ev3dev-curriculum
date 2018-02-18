import tkinter
from tkinter import ttk

import mqtt_remote_method_calls as com


def main():
    # DONE: 2. Setup an mqtt_client.  Notice that since you don't need to receive any messages you do NOT need to have
    # a MyDelegate class.  Simply construct the MqttClient with no parameter in the constructor (easy).
    mqtt_client = com.MqttClient()
    mqtt_client.connect_to_ev3()

    root = tkinter.Tk()
    root.title("MQTT Remote")

    main_frame = ttk.Frame(root, padding=20, relief='raised')
    main_frame.grid()

    enter_emotion_entry = ttk.Entry(main_frame, width=8)
    enter_emotion_entry.grid(row=5, column=1)
    enter_emotion_button = ttk.Button(main_frame, text='Enter Emotion Color')
    enter_emotion_button.grid(row=6, column=1)
    enter_emotion_button['command'] = lambda: emotion(mqtt_client, enter_emotion_entry)

    slider_speed_left_label = ttk.Label(main_frame, text="Left Speed")
    slider_speed_left_label.grid(row=0, column=0)
    slider_speed_left= tkinter.Scale(main_frame, from_=0, to_=600, orient=tkinter.HORIZONTAL)
    slider_speed_left.grid(row=1, column=0)

    slider_speed_right_label = ttk.Label(main_frame, text="Right Speed")
    slider_speed_right_label.grid(row=0, column=2)
    slider_speed_right = tkinter.Scale(main_frame, from_=0, to_=600, orient=tkinter.HORIZONTAL)
    slider_speed_right.grid(row=1, column=2)

    forward_button = ttk.Button(main_frame, text="Forward")
    forward_button.grid(row=2, column=1)
    # forward_button and '<Up>' key is done for your here...
    forward_button['command'] = lambda: move_forward(mqtt_client, slider_speed_left, slider_speed_right)
    root.bind('<Up>', lambda event: move_forward(mqtt_client, slider_speed_left, slider_speed_right))

    left_button = ttk.Button(main_frame, text="Left")
    left_button.grid(row=3, column=0)
    # left_button and '<Left>' key
    left_button['command'] = lambda: turn_left(mqtt_client, slider_speed_left, slider_speed_right)
    root.bind('<Left>', lambda event: turn_left(mqtt_client, slider_speed_left, slider_speed_right))

    stop_button = ttk.Button(main_frame, text="Stop")
    stop_button.grid(row=3, column=1)
    # stop_button and '<space>' key (note, does not need left_speed_entry, right_speed_entry)
    stop_button['command'] = lambda: stop(mqtt_client)
    root.bind('<space>', lambda event: stop(mqtt_client))

    right_button = ttk.Button(main_frame, text="Right")
    right_button.grid(row=3, column=2)
    # right_button and '<Right>' key
    right_button['command'] = lambda: turn_right(mqtt_client, slider_speed_left, slider_speed_right)
    root.bind('<Right>', lambda event: turn_right(mqtt_client, slider_speed_left, slider_speed_right))

    back_button = ttk.Button(main_frame, text="Back")
    back_button.grid(row=4, column=1)
    # back_button and '<Down>' key
    back_button['command'] = lambda: move_back(mqtt_client, slider_speed_left, slider_speed_right)
    root.bind('<Down>', lambda event: move_back(mqtt_client, slider_speed_left, slider_speed_right))

    up_button = ttk.Button(main_frame, text="Up")
    up_button.grid(row=5, column=0)
    up_button['command'] = lambda: send_up(mqtt_client)
    root.bind('<h>', lambda event: send_up(mqtt_client))

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

    c_button = ttk.Button(main_frame, text="Crush")
    c_button.grid(row=7, column=2)
    c_button['command'] = (lambda: grab(mqtt_client))
    root.bind('<c>', lambda event: grab(mqtt_client))

    c_button = ttk.Button(main_frame, text="Calibrate")
    c_button.grid(row=7, column=0)
    c_button['command'] = (lambda: cali(mqtt_client))
    root.bind('<c>', lambda event: cali(mqtt_client))

    root.mainloop()


def move_forward(mqtt_client, left_speed_entry, right_speed_entry):
    print('move forward')
    mqtt_client.send_message('drive', [int(left_speed_entry.get()), int(right_speed_entry.get())])


def move_back(mqtt_client, left_speed_entry, right_speed_entry):
    print('move backwards')
    mqtt_client.send_message('drive', [-int(left_speed_entry.get()), -int(right_speed_entry.get())])


def turn_left(mqtt_client, left_speed_entry, right_speed_entry):
    print('turn left')
    mqtt_client.send_message('drive', [-int(left_speed_entry.get()/6), int(right_speed_entry.get()/6)])


def turn_right(mqtt_client, left_speed_entry, right_speed_entry):
    print('turn right')
    mqtt_client.send_message('drive', [int(left_speed_entry.get()/6), -int(right_speed_entry.get()/6)])


def stop(mqtt_client):
    print('stop')
    mqtt_client.send_message('stop')


# Arm command callbacks
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

def cali(mqtt_client):
    print("Calibrating")
    mqtt_client.send_message("arm_calibration")

def grab(mqtt_client):
    print("crush")
    mqtt_client.send_message("crush")


def emotion(mqtt_client, enter_emotion_entry):
    print('hello')
    mqtt_client.send_message('certain_color', [enter_emotion_entry.get()])


main()
