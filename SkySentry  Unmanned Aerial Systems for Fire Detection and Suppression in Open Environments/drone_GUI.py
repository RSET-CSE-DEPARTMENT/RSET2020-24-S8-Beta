from __future__ import print_function
import time
import socket
from dronekit import connect, VehicleMode, LocationGlobalRelative
from pymavlink import mavutil

# Set up option parsing to get connection string
import argparse
parser = argparse.ArgumentParser(description='Commands vehicle using vehicle.simple_goto.')
parser.add_argument('--connect', help="Vehicle connection target string. If not specified, SITL automatically started and used.")
args = parser.parse_args()

flag = 1
count = 0
no_waypoints = int(input("Enter no of waypoints: "))
def send_data(conn):
    global flag, count
    data = None
    if flag:
        server_data = str(no_waypoints)

        conn.sendall(server_data.encode())
        print("Server ack sent")
        flag = 0
    else:
        while data is not None:
            data = conn.recv(1024).decode()
        if data != '' and data is not None:
            print('Data recieved from client')
            print(data)
            lat, lng, count = map(float, data.split(','))
            print(data)
            data = None
            flag=1

#Get the waypoints

latitude = []
longitude = []

'''
Enter the server side socket creation part here

while(count<=no_waypoints):
In this loop the program should receive the coordinates and count value from the lat_return prgm and assign it to lists latitude and longitude
The no of values accepted should be such that the count value is less than or equal to no_waypoints
    data = client_socket.recv(1024).decode()
    lat, lng, count = map(int, data.split(','))
    latitude.append(lat)
    longitude.append(lng)
client_socket.close()
print(latitude)
print(longitude)
'''

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

#connecting to client program here right after connection with mission planner is established
host = socket.gethostname()
port = 2000

server_socket = socket.socket()
server_socket.bind((host, port))
server_socket.listen(2)

print(host + " Server started. Waiting for connections...")

client_socket, addr = server_socket.accept()
print("Connected with", addr)
while count<=no_waypoints:
        send_data(client_socket)


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

grnd_speed = int(input("Enter default groundspeed: "))

# print("Set default/target airspeed to 3")
vehicle.airspeed = grnd_speed

print("Going towards first point for 30 seconds ...")
point1 = LocationGlobalRelative(9.993417833741802, 76.35982370935227, alt)
vehicle.simple_goto(point1)

# sleep so we can see the change in map
time.sleep(30)

print("Going towards second point for 30 seconds (groundspeed set to 10 m/s) ...")
point2 = LocationGlobalRelative(9.993138604892893, 76.3599048769115, alt)
vehicle.simple_goto(point2, groundspeed= grnd_speed)
# sleep so we can see the change in map
time.sleep(30)

print("Back to base")
point2 = LocationGlobalRelative(9.99342442,76.3592990, alt)
vehicle.simple_goto(point2, groundspeed=grnd_speed)
print("Close vehicle object")
vehicle.close()

# Shut down simulator if it was started.
if sitl:
    sitl.stop()
