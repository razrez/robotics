#!/usr/bin/env pybricks-micropython

"""
Example LEGO® MINDSTORMS® EV3 Robot Educator Color Sensor Down Program
----------------------------------------------------------------------

This program requires LEGO® EV3 MicroPython v2.0.
Download: https://education.lego.com/en-us/support/mindstorms-ev3/python-for-ev3

Building instructions can be found at:
https://education.lego.com/en-us/support/mindstorms-ev3/building-instructions#robot
"""
import time
from pybricks.ev3devices import Motor, GyroSensor, ColorSensor, UltrasonicSensor
from pybricks.parameters import Port, Stop, Direction
from pybricks.tools import wait, StopWatch
from pybricks.robotics import DriveBase
from pybricks.hubs import EV3Brick
import math

ev3 = EV3Brick()
watch = StopWatch()

# Initialize the motors.
left_motor = Motor(Port.A)
right_motor = Motor(Port.D)

# Configure the gripper motor on Port A with default settings.
gripper_motor = Motor(Port.C)

# Initialize the Sensor.
gyro_sensor = GyroSensor(Port.S3)
color_sensor = ColorSensor(Port.S4)
sonar_sernsor = UltrasonicSensor(Port.S2)

gyro_sensor.reset_angle(0)

# Initialize the drive base.
robot = DriveBase(left_motor, right_motor, wheel_diameter=55.5, axle_track=119)

# Set the drive speed at 100 millimeters per second.
DRIVE_SPEED = 70

KP = 0.8

# rapid delta speed
KD = 0.15

# stability koef
KI = 119

SP = 45

err = 0
prev_err = 0
delta_err = 0
sum_int = 0
dt = 0

dist0 = 0
x, y = 0, 0

cups_detected = 0
cups_coordinates = []
cups_angles = []

gyro_sensor.reset_angle(0)

def PID():
    return -1 * (KP * err + KI * sum_int + KD * delta_err * dt)


def rotate(ang):
    set_point = gyro_sensor.angle() - ang
    rotation_err = 10
    delta_angle = 3

    while abs(rotation_err) > delta_angle:
        rotation_err = set_point - gyro_sensor.angle()

        turn_rate = 1.17 * rotation_err

        robot.drive(0, turn_rate)

    wait(100)
    robot.stop()


def moveToCup():
    set_point = 41
    distance_err = 10
    delta_distance = 4

    start_traveled = robot.distance()
    while abs(distance_err) > delta_distance:
        distance_err = set_point - sonar_sernsor.distance()

        # turn_rate = KP * abs(distance_err)

        robot.drive(70, 0)

    robot.stop()
    end_traveled = robot.distance() - start_traveled

    return end_traveled


def goBack(travel_distance):
    robot.straight(-travel_distance)
    robot.stop()


def release():
    # Initialize the gripper. First rotate the motor until it stalls.
    # Stalling means that it cannot move any further. This position
    # corresponds to the closed position. Then rotate the motor
    # by 90 degrees such that the gripper is open.
    gripper_motor.run_until_stalled(200, then=Stop.COAST, duty_limit=30)
    gripper_motor.reset_angle(0)


def grab():
    release()
    # gripper_motor.run_target(200, -90)

    # Close the gripper to grab the wheel stack.
    # ripper_motor.run_until_stalled(-500, then=Stop.HOLD, duty_limit=100)

    # Open the gripper to release the wheel stack.
    gripper_motor.run_target(1000, -2850)
    # ev3.speaker.beep()
    # print(gripper_motor.angle())


def clear_square():
    2


def fill_square():
    3


start_time = time.time()
while True:
    err = SP - gyro_sensor.angle()
    theta = gyro_sensor.angle()
    dist1 = robot.distance() / 10 #cm
    delta_dist = dist1 - dist0
    
    x += delta_dist * math.cos(theta / 57.29)
    y += delta_dist * math.sin(theta / 57.29)
    
    dist0 = dist1

    release()
    rotate_counter = 0
    # firstly, we need to find cups
    while cups_detected != 2:
        if sonar_sernsor.distance() > 500:
            rotate(45)
            rotate_counter += 1
        else:
            ev3.speaker.beep()
            cups_detected += 1

            rotate_counter += 1

            x_bootle = sonar_sernsor.distance() * math.cos(theta / 57.29)
            y_bottle = sonar_sernsor.distance() * math.sin(theta / 57.29)

            cups_coordinates.append(x_bootle)
            cups_coordinates.append(y_bottle)
            cups_angles.append(gyro_sensor.angle())

            if cups_detected == 1: 
                rotate(45)

    
    # turn_rate  = 0

    # ev3.screen.clear()
    # ev3.screen.print(int(gyro_sensor.angle()))

    # if robot.distance() > 10000 and math.sqrt(x ** 2 + y ** 2) < 30:
    #     break

    # go to second cup, grab and go back to the center
    travel1 = moveToCup()
    wait(10)
    grab()
    wait(10)
    goBack(travel1)

    # rotate to the first detected cup, put aside the second cup, rotate to the first again
    rotate(gyro_sensor.angle() - cups_angles[0])
    rotate(-45)
    robot.straight(200)
    release()
    robot.straight(-200)
    rotate(45)

    # go to the first cup, grab and go back to the center
    travel2 = moveToCup()
    wait(10)
    grab()
    wait(10)
    goBack(travel2)

    # rotate to the second cup's squre (to the left)
    rotate(cups_angles[0] - cups_angles[1])

    # go to the second cup's squre, fill and go back to the center
    robot.straight(travel1)
    release()
    robot.straight(-travel1)

    # first cup moved to the second cup's square

    # take the second cup, rotate to the first cup's squre (to the right) !!!!!!!!!!!!!!!!!!!
    rotate(gyro_sensor.angle() - cups_angles[0])
    rotate(-45)
    robot.straight(200)
    grab()
    robot.straight(-200)
    rotate(45)

    # go to the second cup's squre, fill and go back to the center
    robot.straight(travel2)
    release()
    robot.straight(-travel2)

    break

    # Set the drive base speed and turn rate.
    # robot.drive(DRIVE_SPEED, turn_rate)
    # grab()

    # You can wait for a short time or do other things in this loop.
    wait(10)