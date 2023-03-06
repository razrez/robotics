#!/usr/bin/env pybricks-micropython

"""
Example LEGO® MINDSTORMS® EV3 Robot Educator Color Sensor Down Program
----------------------------------------------------------------------

This program requires LEGO® EV3 MicroPython v2.0.
Download: https://education.lego.com/en-us/support/mindstorms-ev3/python-for-ev3

Building instructions can be found at:
https://education.lego.com/en-us/support/mindstorms-ev3/building-instructions#robot
"""

from pybricks.ev3devices import Motor, ColorSensor
from pybricks.parameters import Port
from pybricks.tools import wait
from pybricks.robotics import DriveBase
from pybricks.hubs import EV3Brick

ev3 = EV3Brick()

# Initialize the motors.
left_motor = Motor(Port.B)
right_motor = Motor(Port.C)

# Initialize the color sensor.
line_sensor = ColorSensor(Port.S3)

# Initialize the drive base.
robot = DriveBase(left_motor, right_motor, wheel_diameter=55.5, axle_track=104)

# Calculate the light threshold/SET_POINT. Choose values based on your measurements.
BLACK = 4
WHITE = 57
threshold = (BLACK + WHITE) / 2

# Set the drive speed at 100 millimeters per second.
DRIVE_SPEED = 70

# Set the gain of the proportional line controller. This means that for every
# percentage point of light deviating from the threshold, we set the turn
# rate of the drivebase to 1.2 degrees per second.

# For example, if the light value deviates from the threshold by 10, the robot
# steers at 10*1.2 = 12 degrees per second.
PROPORTIONAL_GAIN = 1.2


KP = 1.7

# rapid delta speed
KD = 40

# stability koef
KI = 0.03

prev_err = 0
sum_int = 0
# Start following the line endlessly.

while True:
    # Calculate the deviation from the threshold.
    err = threshold - line_sensor.reflection()
    sum_int += err

    delta_err = err - prev_err

    turn_rate = KP * err + KI * sum_int + KD * delta_err
    prev_err = err

    # if line_sensor.reflection() < 20 and line_sensor.reflection() > 10:
    #     # Calculate the turn rate.
    #     turn_rate = turn_rate = KP * err + KI * sum_int + KD * (err - prev_err) * (-1)
    # elif line_sensor.reflection() > 20:
    #     turn_rate = KP * err + KI * sum_int + KD * (err - prev_err)
    # elif line_sensor.reflection() < 10:
    #     turn_rate = KP * err + KI * sum_int + KD * (err - prev_err) * (-1)
    

    # ev3.screen.clear()
    # ev3.screen.draw_text(0, 0, turn_rate)
    # ev3.screen.draw_text(0, 0, line_sensor.reflection())
    # print(turn_rate)
    
    # don't let the robot spinning around
    if turn_rate < -200:
        #ev3.speaker.beep()
        prev_err = 0
        sum_int = 0
        turn_rate = 0
        # search the edge of line to follow
        while threshold - line_sensor.reflection() < 0:
            robot.drive(0, -50)

    if delta_err > -8 and delta_err < 8:
        DRIVE_SPEED = 100
    else:
        DRIVE_SPEED = 70
        
    # Set the drive base speed and turn rate.
    robot.drive(DRIVE_SPEED, turn_rate)

    # You can wait for a short time or do other things in this loop.
    # wait(10)