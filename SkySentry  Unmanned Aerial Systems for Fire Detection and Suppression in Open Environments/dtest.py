import time
from dronekit import connect, VehicleMode, LocationGlobalRelative, Command, LocationGlobal
from pymavlink import mavutil

def arm_and_takeoff(altitude):
    while not vehicle.is_armable:
        print("Waiting to armable")
        time.sleep(1)
    print("Arming motors")
    vehicle.mode = VehicleMode("GUIDED")
    vehicle.armed=True

    while not vehicle.armed: time.sleep(1)

    print("Taking OFF")
    vehicle.simple_takeoff(altitude)
    while True:
        v_alt = vehicle.location.global_relative_frame.alt
        print(">> Altitude = %.1f m"%v_alt)
        if v_alt >= altitude -1.0:
            print("Target altitude reached")
            break
        time.sleep(1)

def clear_mission(vehicle):
    cmds=vehicle.commands
    cmds.clear()
    vehicle.flush()

    download_mission(vehicle)

def download_mission(vehicle):
    cmds = vehicle.commands
    cmds.download()
    cmds.wait_ready()

def get_current_mission(vehicle):
    print('Downloading the mission')
    # Download and retrieve mission commands
    download_mission(vehicle)
    missionList = []
    n_wp = 0

    try:
        for wp in vehicle.commands:
            print("Entered append for loop")
            missionList.append(wp)
            n_wp += 1
    except Exception as e:
        print("Error:", e)

    return n_wp, missionList
"""
    # Change vehicle mode to GUIDED if it's not already in GUIDED or AUTO mode
    if vehicle.mode.name not in ['GUIDED', 'AUTO']:
        print("Changing vehicle mode to GUIDED")
        vehicle.mode = VehicleMode("GUIDED")
        time.sleep(2)  # Allow some time for the mode change to take effect

    # Wait until the vehicle is in the GUIDED mode
    while vehicle.mode.name != 'GUIDED':
        print("Current mode:", vehicle.mode.name)
        print("Waiting for vehicle to enter GUIDED mode...")
        time.sleep(1)

    print("Vehicle mode is suitable for retrieving mission commands")
"""
    


def add_last_waypoint_to_mission(vehicle,lat,long,alt):
    download_mission()
    cmds = vehicle.commands

    missionList = []
    for wp in cmds:
        missionList.append(wp)
    wp_last =  Command(0,0,0,mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT,mavutil.mavlink.MAV_CMD_NAV_WAYPOINT, 0, 0, 0, 0, 0, 0,lat, long,alt)
    missionList.append(wp_last)
    cmds.clear()

    for wp in missionList:
        cmds.add(wp)
    
    cmds.upload()
    return(cmds.count)

def ChangeMode(vehicle  ,mode):
    while vehicle.mode !=  VehicleMode(mode):
        vehicle.mode= VehicleMode(mode)
        time.sleep(0.5)

    return True

gnd_speed=10
mode ='GROUND'

vehicle = connect('udp:127.0.0.1:14550')

while True:
    if mode == 'GROUND':
        n_wp,missionList=get_current_mission(vehicle)
        time.sleep(2)

        if n_wp >0:
            print("A valid mission has been uploaded: takeoff")
            mode = 'TAKEOFF'
    elif mode == 'TAKEOFF':
        add_last_waypoint_to_mission(vehicle,vehicle.location.global_relative_frame.lat,vehicle.location.global_relative_frame.lon,vehicle.location.global_relative_frame.alt)
        print('Final waypoint added  to the current mission')
        time.sleep(1)
        arm_and_takeoff(10)
        ChangeMode(vehicle,"AUTO")
        vehicle.groundspeed =gnd_speed
        mode='MISSION'
        print("Switch to MISSION mode")

    elif mode =='MISSION':
        print('Current WP: %d of %d'%(vehicle.commands.next,vehicle.commands.count))
        if(vehicle.commands.next == vehicle.commands.count):
            print("Final wp reached: go back home")

            clear_mission(vehicle)
            print("Mission deletedd")
            ChangeMode(vehicle,"RTL")
            mode ="BACK"
    elif mode == "BACK":
        if vehicle.location.global_relative_frame.alt<1.0:
            print("vehicle landed,back to GROUND")
            mode = "GROUND"
    
    time.sleep(0.5)     