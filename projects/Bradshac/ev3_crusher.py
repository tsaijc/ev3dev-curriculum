import mqtt_remote_method_calls as com
import robot_controller as robo
import ev3dev.ev3 as ev3
import time

class MyDelegate(object):
    def __init__(self):
        self.robot = robo.Snatch3r()
        # self.list_of_colors = [red, blue, green]



    def certain_color(self, color):
        if color == 'red':

            if self.robot.color_sensor == ev3.ColorSensor.COLOR_RED:
                if self.robot.ir_sensor.proximity < 10:
                    ev3.Sound.beep()
                    ev3.Sound.speak("We need to crush")
                    self.robot.crush()
                    time.sleep(.01)
                    ev3.Sound.speak("Time to charge up")
                    self.robot.arm_calibration()

                    time.sleep(1.5)
                time.sleep(0.1)
        if color == 'blue':

            if self.robot.color_sensor == ev3.ColorSensor.COLOR_BLUE:
                if self.robot.ir_sensor.proximity < 10:
                    ev3.Sound.beep()
                    ev3.Sound.speak("Lift her up")
                    self.robot.arm_up()
                    self.robot.arm_down()
                    time.sleep(0.1)


def main():
    my_delegate = MyDelegate
    mqtt_client = com.MqttClient(my_delegate)
    mqtt_client.connect_to_pc()

    # while not robot.touch_sensor.is_pressed:
    #
    #     if robot.ir_sensor.proximity < 10:
    #         ev3.Sound.beep()
    #         ev3.Sound.speak("We need to crush")
    #
    #         time.sleep(1.5)
    #     time.sleep(0.1)

    my_delegate.robot.loop_forever()


# ----------------------------------------------------------------------
# Calls  main  to start the ball rolling.
# ----------------------------------------------------------------------
main()
