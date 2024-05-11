import socket
import folium as fl
#from pynput import mouse
from streamlit_folium import st_folium
import time
import streamlit as st
import sys
'''
Here create a client side socket part
The client will be sending the values to another prgm in the same system, so you can keep the connection to localhost or something

'''
connection_flag = 0
flag = 1
waypoints = 90
geodata = ()
client_socket = socket.socket(2)
count = 0

m = fl.Map()
m.add_child(fl.LatLngPopup())
map = st_folium(m, height=350, width=700)
def send_data():
    global flag
    global geodata
    global waypoints
    if flag == 1:
       data = client_socket.recv(1024).decode()
       data = int(data)
       print("Ack received from server")
       if data is not None:
           waypoints= data
           print(waypoints)
           flag =0
       left = True
       # Parse the received coordinates
       #x, y, w, h, restart = map(int, data.split(','))
       # Acquire the data lock to update the hand coordinates
       # with server_hand_coordinates_lock:
       #server_hand_coordinates = (x, y, w, h)
    else:
       client_socket.sendall(geodata.encode())
       print("Data sent from client")
       print(geodata)
       flag =1

def get_pos(lat,lng):
    return lat, lng

def return_loc():
    global count
    global waypoints
    global geodata


    if map.get("last_clicked"):
        geodata = get_pos(map["last_clicked"]["lat"], map["last_clicked"]["lng"])
        count = count + 1

    if geodata:
        data1 = str(geodata[0])+',' + str(geodata[1])
        geodata = data1 + ',' + str(count)
        send_data()
        print("If geodata condition")
        print(geodata)


print("About to request connection")
port =2000
host = socket.gethostname()
try:
    if connection_flag == 0:
        client_socket.connect((host, port))
        print('Connection request sent')
        data = client_socket.recv(1024).decode()
        print("data: " + data)
        data = int(data)

        print("Ack received from server")
        if data is not None:
            waypoints = data
            print(waypoints)
            flag = 0
        else:
            print("Nothing received")
        connection_flag = 1
except Exception as e:
    print('Error')
while waypoints>count:
    return_loc()

sys.exit()
