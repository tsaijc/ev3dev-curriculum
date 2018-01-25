"""
  Library of EV3 robot functions that are useful in many different applications. For example things
  like arm_up, arm_down, driving around, or doing things with the Pixy camera.

  Add commands as needed to support the features you'd like to implement.  For organizational
  purposes try to only write methods into this library that are NOT specific to one tasks, but
  rather methods that would be useful regardless of the activity.  For example, don't make
  a connection to the remote control that sends the arm up if the ir remote control up button
  is pressed.  That's a specific input --> output task.  Maybe some other task would want to use
  the IR remote up button for something different.  Instead just make a method called arm_up that
  could be called.  That way it's a generic action that could be used in any task.
"""

import ev3dev.ev3 as ev3
import math
import time
import robot_controller as robo

class Snatch3r(object):
    """Commands for the Snatch3r robot that might be useful in many different programs."""

    def drive_inches(self):
        print("--------------------------------------------")
        print(" Drive inches")
        print("--------------------------------------------")
        ev3.Sound.speak("Drive inches").wait()
        robot = robo.Snatch3r()

        while True:
            speed_deg_per_second = int(input("Speed (0 to 900 dps): "))
            if speed_deg_per_second == 0:
                break
            inches_target = int(input("Distance (inches): "))
            if inches_target == 0:
                break

            robot.drive_inches(inches_target, speed_deg_per_second)
            ev3.Sound.beep().wait()  # Fun little beep

        print("Goodbye!")
        ev3.Sound.speak("Goodbye").wait()
