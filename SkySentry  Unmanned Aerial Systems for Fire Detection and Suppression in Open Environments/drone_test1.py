from __future__ import print_function
import time
from dronekit import connect, VehicleMode, LocationGlobalRelative
from pymavlink import mavutil

# Set up option parsing to get connection string
import argparse
parser = argparse.ArgumentParser(description='Commands vehicle using vehicle.simple_goto.')
parser.add_argument('--connect', help="Vehicle connection target string. If not specified, SITL automatically started and used.")
args = parser.parse_args()

# no_waypoints = int(input("Enter the no of waypoints: "))

connection_string = args.connect
sitl = None


# Start SITL if no connection string specified
if not connection_string:
    import dronekit_sitl
    sitl = dronekit_sitl.start_default()
    connection_string = sitl.connection_string()


# Connect to the Vehicle
print('Connecting to vehicle on: %s' % connection_string)
vehicle = connect(connection_string, wait_ready=True)

def set_velocity_body(vehicle, vx, vy, vz):
    """ Remember: vz is positive downward!!!
http://ardupilot.org/dev/docs/copter-commands-in-guided-mode.html

Bitmask to indicate which dimensions should be ignored by the vehicle
(a value of 0b0000000000000000 or 0b0000001000000000 indicates that
none of the setpoint dimensions should be ignored). Mapping:
bit 1: x,  bit 2: y,  bit 3: z,
bit 4: vx, bit 5: vy, bit 6: vz,
bit 7: ax, bit 8: ay, bit 9:


"""
    msg = vehicle.message_factory.set_position_target_local_ned_encode(0,0, 0,mavutil.mavlink.MAV_FRAME_BODY_NED,
    0b0000111111000111,  # -- BITMASK -> Consider only the velocities
    0, 0, 0,  # -- POSITION
    vx, vy, vz,  # -- VELOCITY
    0, 0, 0,  # -- ACCELERATIONS
    0, 0)
    vehicle.send_mavlink(msg)
    vehicle.flush()

def arm_and_takeoff(aTargetAltitude):
    """
    Arms vehicle and fly to aTargetAltitude.
    """

    print("Basic pre-arm checks")
    # if vehicle.prearm_required:
    #     checks = vehicle.prearm_checks()
    #     for check in checks:
    #         if not check.passed:
    #             print("Pre-arm check failed:", check.name)
    # Don't try to arm until autopilot is ready
    vehicle.mode = VehicleMode('GUIDED')
    print(vehicle.mode)
    while not vehicle.is_armable:
        print("Waiting for vehicle to initialize...")
        time.sleep(2)

    vehicle.armed = True
    # vehicle.flush()
    print("Is Armed:% s" % vehicle.armed)


    while not vehicle.armed:
        print("Waiting for arming...Mode:% s" % vehicle.mode)
        print("Is Armed:% s" % vehicle.armed)
        vehicle.armed = True
        time.sleep(2)

    print("Taking off!")
    vehicle.simple_takeoff(aTargetAltitude)  # Take off to target altitude

    # Wait until the vehicle reaches a safe height before processing the goto
    #  (otherwise the command after Vehicle.simple_takeoff will execute
    #   immediately).
    while True:
        print(" Altitude: ", vehicle.location.global_relative_frame.alt)
        # Break and return from function just below target altitude.
        if vehicle.location.global_relative_frame.alt >= aTargetAltitude * 0.95:
            print("Reached target altitude")
            break
        time.sleep(1)

alt = int(input("Enter target altitude: "))
arm_and_takeoff(alt)

air_speed = int(input("Enter default air speed: "))

# print("Set default/target airspeed to 3")
vehicle.airspeed = air_speed
print("Taking off")
point1 = LocationGlobalRelative(9.992305054281223, 76.36492654999768, alt)
vehicle.simple_goto(point1)

# sleep so we can see the change in map
time.sleep(60)

point2 = LocationGlobalRelative(9.992133355256751, 76.36449739657034, alt)
vehicle.simple_goto(point2, groundspeed= 10)
# sleep so we can see the change in map
time.sleep(60)

point3 = LocationGlobalRelative(9.990231355755155, 76.36500367580396, alt)
vehicle.simple_goto(point3, groundspeed= 10)
# sleep so we can see the change in map
time.sleep(60)
point3 = LocationGlobalRelative(9.99198208356124, 76.36602322602678, alt)
vehicle.simple_goto(point3, groundspeed= 10)
# sleep so we can see the change in map
time.sleep(60)
print("Back to base")
point2 = LocationGlobalRelative(9.992305054281223, 76.36492654999768, alt)
vehicle.simple_goto(point2, groundspeed=air_speed)
# Close vehicle object before exiting script
vehicle.mode = VehicleMode("LAND")
while not vehicle.location.global_relative_frame.alt==0:
    if vehicle.location.global_relative_frame.alt < 2:
        set_velocity_body(vehicle,0,0,0.1)
print("Close vehicle object")
vehicle.close()

# Shut down simulator if it was started.
if sitl:
    sitl.stop()
