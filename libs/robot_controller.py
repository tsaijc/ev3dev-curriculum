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
import time
import math


class Snatch3r(object):
    """Commands for the Snatch3r robot that might be useful in many different programs."""

    def __init__(self):
        # Connect two large motors on output ports B and C
        self.left_motor = ev3.LargeMotor(ev3.OUTPUT_B)
        self.right_motor = ev3.LargeMotor(ev3.OUTPUT_C)
        self.arm_motor = ev3.MediumMotor(ev3.OUTPUT_A)
        self.touch_sensor = ev3.TouchSensor()
        self.running = 0
        self.ir_sensor = ev3.InfraredSensor()
        self.color_sensor = ev3.ColorSensor()
        self.pixy = ev3.Sensor(driver_name="pixy-lego")
        self.beacon_seeker = ev3.BeaconSeeker(channel=1)

        # Check that the motors are actually connected
        assert self.left_motor.connected
        assert self.right_motor.connected
        assert self.arm_motor.connected
        assert self.touch_sensor
        assert self.ir_sensor
        assert self.color_sensor
        assert self.pixy

    def drive_inches(self, inches_target, speed_deg_per_second):
        """Drives robot forwards or backwards using speed and inches to travel input"""
        self.left_motor.run_to_rel_pos(position_sp=(90 * inches_target), speed_sp=speed_deg_per_second,
                                       stop_action=ev3.Motor.STOP_ACTION_BRAKE)
        self.right_motor.run_to_rel_pos(position_sp=(90 * inches_target), speed_sp=speed_deg_per_second,
                                        stop_action=ev3.Motor.STOP_ACTION_BRAKE)
        self.left_motor.wait_while(ev3.Motor.STATE_RUNNING)
        self.right_motor.wait_while(ev3.Motor.STATE_RUNNING)

    def drive(self, left_speed, right_speed):
        self.left_motor.run_forever(speed_sp=left_speed)
        self.right_motor.run_forever(speed_sp=right_speed)

    def stop(self):
        self.right_motor.stop(stop_action=ev3.Motor.STOP_ACTION_BRAKE)
        self.left_motor.stop(stop_action=ev3.Motor.STOP_ACTION_BRAKE)

    def turn_degrees(self, degrees_to_turn, turn_speed_sp):
        """Turns robot the amount that you want using degrees to turn and turn speed"""
        self.left_motor.run_to_rel_pos(position_sp=(-degrees_to_turn*4.5), speed_sp=-turn_speed_sp,
                                       stop_action=ev3.Motor.STOP_ACTION_BRAKE)
        self.right_motor.run_to_rel_pos(position_sp=(degrees_to_turn*4.5), speed_sp=turn_speed_sp,
                                        stop_action=ev3.Motor.STOP_ACTION_BRAKE)

        self.left_motor.wait_while(ev3.Motor.STATE_RUNNING)
        self.right_motor.wait_while(ev3.Motor.STATE_RUNNING)

    def arm_calibration(self):
        """calibrates the robot arm by going up and then down and sets the down position as 0."""
        self.arm_motor.run_forever(speed_sp=900)
        while not self.touch_sensor.is_pressed:
            time.sleep(0.01)
        self.arm_motor.stop(stop_action=ev3.Motor.STOP_ACTION_BRAKE)
        ev3.Sound.beep().wait()  # Fun little beep

        arm_revolutions_for_full_range = 14.2
        self.arm_motor.run_to_rel_pos(position_sp=-arm_revolutions_for_full_range * 360)
        self.arm_motor.wait_while(ev3.Motor.STATE_RUNNING)
        ev3.Sound.beep().wait()  # Fun little beep

        self.arm_motor.position = 0  # Calibrate the down position as 0 (this line is correct as is).

    def arm_up(self):
        """moves the robot arm up."""
        self.arm_motor.run_forever(speed_sp=900)
        while not self.touch_sensor.is_pressed:
            time.sleep(0.01)
        self.arm_motor.stop(stop_action=ev3.Motor.STOP_ACTION_BRAKE)
        ev3.Sound.beep().wait()  # Fun little beep

    def arm_down(self):
        """moves the robot arm down."""
        self.arm_motor.run_to_abs_pos(position_sp=0)
        self.arm_motor.wait_while(ev3.Motor.STATE_RUNNING)  # Blocks until the motor finishes running
        ev3.Sound.beep().wait()  # Fun little beep

    def loop_forever(self):
        """run the robot forever until shutdown is performed"""
        self.running = True
        while self.running:
            time.sleep(0.1)  # Do nothing (except receive MQTT messages) until an MQTT message calls shutdown.

    def shutdown(self):
        # Modify a variable that will allow the loop_forever method to end. Additionally stop motors and set LEDs green.
        # The most important part of this method is given here, but you should add a bit more to stop motors, etc.
        self.running = False

    def seek_beacon(self):
        """
        Uses the IR Sensor in BeaconSeeker mode to find the beacon.  If the beacon is found this return True.
        If the beacon is not found and the attempt is cancelled by hitting the touch sensor, return False.
        """
        forward_speed = 300
        turn_speed = 100
        while not self.touch_sensor.is_pressed:
            current_heading = self.beacon_seeker.heading  # use the beacon_seeker heading
            current_distance = self.beacon_seeker.distance  # use the beacon_seeker distance
            if current_distance == -128:
                # If the IR Remote is not found just sit idle for this program until it is moved.
                print("IR Remote not found. Distance is -128")
                self.stop()
            else:
                if math.fabs(current_heading) < 2:
                    # Close enough of a heading to move forward
                    print("On the right heading. Distance: ", current_distance)
                    # You add more!
                    if current_distance > 1:
                        self.drive(forward_speed, forward_speed)
                    else:
                        self.stop()
                        self.drive_inches(3, 100)
                        return True

                if 2 < math.fabs(current_heading) < 10:
                    print("Adjusting Heading: ", current_heading)
                    if current_heading > 0:
                        self.drive(turn_speed, -turn_speed)
                    if current_heading < 0:
                        self.drive(-turn_speed, turn_speed)

                if math.fabs(current_heading) > 10:
                    print("Heading is too far off to fix: ", current_heading)
                    self.stop()

            time.sleep(0.2)

        # The touch_sensor was pressed to abort the attempt if this code runs.
        print("Abandon ship!")
        self.stop()
        return False